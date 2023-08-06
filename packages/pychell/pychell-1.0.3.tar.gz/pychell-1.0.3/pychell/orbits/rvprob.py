import optimize.scores as optscore
import optimize.kernels as optnoisekernels
import optimize.optimizers as optimizers
import optimize.knowledge as optknow
import optimize.frameworks as optframeworks
import plotly.subplots
import pychell.orbits.gls as gls
import tqdm
import plotly.graph_objects
from itertools import chain, combinations
from joblib import Parallel, delayed
import numpy as np
from numba import jit, njit
import matplotlib.pyplot as plt
import copy
import abc
import pychell.orbits.rvmodels as pcrvmodels
import optimize.kernels as optkernels
import pychell.orbits.rvkernels as pcrvkernels
import pychell.utils as pcutils
PLOTLY_COLORS = pcutils.PLOTLY_COLORS
import os
import pychell
plt.style.use(os.path.dirname(pychell.__file__) + os.sep + "gadfly_stylesheet.mplstyle")

class ExoProblem(optframeworks.OptProblem):
    
    def __init__(self, *args, star_name=None, likes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.star_name = 'Star' if star_name is None else star_name
        self.scorer = likes
        gen_latex_labels(self.p0, self.planets_dict)
    
    def rv_phase_plot(self, planet_index, opt_result=None):
        """Creates a phased rv plot for a given planet with the model on top.

        Args:
            planet_index (int): The planet index
            opt_result (dict, optional): The optimization or sampler result to use. Defaults to None, and uses the initial parameters.

        Returns:
            plotly.figure: A plotly figure containing the plot.
        """
        
        # Resolve which pars to use
        if opt_result is None:
            pars = self.p0
        else:
            pars = opt_result["pbest"]
            
        # Creat a figure
        fig = plotly.subplots.make_subplots(rows=1, cols=1)
        
        # Alias
        per = pars['per' + str(planet_index)].value
        tc = pars['tc' + str(planet_index)].value
        
        # Create the phased model, high res
        t_hr = np.linspace(0, per, num=500)
        phases_hr = self.get_phases(t_hr, per, tc)
        like0 = next(iter(self.scorer.values()))
        planet_model_phased = like0.model.build_planet(pars, t_hr, planet_index)
        
        # Loop over likes
        color_index = 0
        for like in self.scorer.values():
            
            # Create a data rv vector where everything is removed except this planet
            if like.model.has_gp:
                residuals = like.residuals_after_kernel(pars)
            else:
                residuals = like.residuals_before_kernel(pars)
            
            # Compute error bars
            errors = like.model.kernel.compute_data_errors(pars)
            
            # Loop over instruments and plot each
            for data in like.data.values():
                _errors = errors[like.model.data_inds[data.label]]
                _data = residuals[like.model.data_inds[data.label]] + like.model.build_planet(pars, data.t, planet_index)
                phases_data = self.get_phases(data.t, per, tc)
                _yerr = dict(array=_errors)
                fig.add_trace(plotly.graph_objects.Scatter(x=phases_data, y=_data, name=data.label, error_y=_yerr, mode='markers', marker=dict(color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)])))
                color_index += 1

        # Plot the model on top
        ss = np.argsort(phases_hr)
        fig.add_trace(plotly.graph_objects.Scatter(x=phases_hr[ss], y=planet_model_phased[ss], line=dict(color='black', width=2)))
        
        # Labels
        fig.update_xaxes(title_text='<b>Phase</b>')
        fig.update_yaxes(title_text='<b>RVs [m/s]</b>')
        fig.update_yaxes(title_text='<b>Residual RVs [m/s]</b>')
        fig.update_layout(title='<b>' + self.star_name + ' ' + like0.model.planets_dict[planet_index]["label"] + '</b>')
        fig.update_layout(template="ggplot2")
        
        # Return fig
        return fig

    def rv_plot(self, opt_result, n_model_pts=5000, time_offset=2450000, kernel_sampling=10):
        """Creates an rv plot for the full dataset and rv model.

        Args:
            opt_result (dict, optional): The optimization or sampler result to use. Defaults to None, and uses the initial parameters.
            show (bool, optional): Whether to show or return the figure. Defaults to True.
            n_rows (int, optional): The number of rows to split the plot into. Defaults to 1.

        Returns:
            plotly.figure: A Plotly figure.
        """
        
        # Resolve which pars to use
        if opt_result is None:
            pars = self.p0
        else:
            pars = opt_result["pbest"]
            
        # Create a figure
        fig = plotly.subplots.make_subplots(rows=2, cols=1)
        
        # Create the full planet model, high res.
        # Use a different time grid for the gp since det(K)~ O(n^3)
        t_data_all = self.data.get_vec('t')
        t_start, t_end = np.nanmin(t_data_all), np.nanmax(t_data_all)
        dt = t_end - t_start
        t_hr = np.linspace(t_start - dt / 100, t_end + dt / 100, num=n_model_pts)
        
        # Create hr planet model
        like0 = next(iter(self.scorer.values()))
        model_arr_hr = like0.model._builder(pars, t_hr)

        # Plot the planet model
        fig.add_trace(plotly.graph_objects.Scatter(x=t_hr - time_offset, y=model_arr_hr, line=dict(color='black', width=2)), row=1, col=1)
        
        # Add a zero line for the residuals
        fig.add_shape(type='line', x0=0, y0=0, x1=1, y1=0, line=dict(color='Black'), xref='paper', yref='paper', row=2, col=1)
        
        # Loop over likes and:
        # 1. Create high res GP
        # 2. Plot high res GP and data
        color_index = 0
        for like in self.scorer.values():
            
            # Data errors
            errors = like.model.kernel.compute_data_errors(pars)
            
            # RV Color
            if isinstance(like.model.kernel, pcrvkernels.RVColor):
                
                # Generate the residuals
                residuals_with_noise = like.residuals_before_kernel(pars)
                residuals_no_noise = like.residuals_after_kernel(pars)
                
                # Plot a GP for each instrument
                for data in like.data.values():
                    
                    # Time array
                    t_hr_gp = np.array([], dtype=float)
                    for i in range(data.t.size):
                        t_hr_gp = np.concatenate((t_hr_gp, np.linspace(data.t[i] - pars['gp_per'].value / 2, data.t[i] + pars['gp_per'].value / 2, num=kernel_sampling)))
                    t_hr_gp = np.sort(t_hr_gp)
                    
                    # Realize the GP
                    gpmu, gpstddev = like.model.kernel.realize(pars, residuals=residuals_with_noise[like.model.data_inds[data.label]], xpred=t_hr_gp, return_unc=True, instname=data.label)
                    
                    # Plot the GP
                    fig.add_trace(plotly.graph_objects.Scatter(x=t_hr_gp - time_offset, y=gpmu, line=dict(width=1, color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)]), name='GP ' + data.label), row=1, col=1)
                    
                    # Plot the data and residuals
                    data_arr_offset = data.rv - pars['gamma_' + data.label].value
                    _errors = errors[like.model.data_inds[data.label]]
                    _residuals = residuals_no_noise[like.model.data_inds[data.label]]
                    _yerr = dict(array=_errors)
                    fig.add_trace(plotly.graph_objects.Scatter(x=data.t - time_offset, y=data_arr_offset, name=data.label, error_y=_yerr, mode='markers', marker=dict(color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)])), row=1, col=1)
                    fig.add_trace(plotly.graph_objects.Scatter(x=data.t - time_offset, y=_residuals, error_y=_yerr, mode='markers', marker=dict(color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)]), showlegend=False), row=2, col=1)
                    color_index += 1
                    
            # Standard GP
            elif isinstance(like.model.kernel, optkernels.GaussianProcess):
                
                # Make hr array for GP
                if 'gp_per' in pars:
                    s = pars['gp_per'].value
                elif 'gp_decay' in pars:
                    s = pars['gp_decay'].value / 10
                else:
                    s = 10
                t_hr_gp = np.array([], dtype=float)
                for i in range(like.data_t.size):
                    t_hr_gp = np.concatenate((t_hr_gp, np.linspace(like.data_t[i] - s, like.data_t[i] + s, num=kernel_sampling)))
                t_hr_gp = np.sort(t_hr_gp)
                
                # Generate the residuals and realize the GP
                residuals_with_noise = like.residuals_before_kernel(pars)
                residuals_no_noise = like.residuals_after_kernel(pars)
                gpmu, gpstddev = like.model.kernel.realize(pars, xpred=t_hr_gp, residuals=residuals_with_noise, return_unc=True)
                
                # Plot the GP
                fig.add_trace(plotly.graph_objects.Scatter(x=t_hr_gp - time_offset, y=gpmu, line=dict(width=1, color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)]), name=like.label), row=1, col=1)
                
                # For each instrument, plot
                for data in like.data.values():
                    data_arr_offset = data.rv - pars['gamma_' + data.label].value
                    _errors = errors[like.model.data_inds[data.label]]
                    _residuals = residuals_no_noise[like.model.data_inds[data.label]]
                    _yerr = dict(array=_errors)
                    fig.add_trace(plotly.graph_objects.Scatter(x=data.t - time_offset, y=data_arr_offset, name=data.label, error_y=_yerr, mode='markers', marker=dict(color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)])), row=1, col=1)
                    fig.add_trace(plotly.graph_objects.Scatter(x=data.t - time_offset, y=_residuals, error_y=_yerr, mode='markers', marker=dict(color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)]), showlegend=False), row=2, col=1)
                    color_index += 1
                
            # White noise
            else:
                residuals_no_noise = like.residuals_after_kernel(pars)
                
                # For each instrument, plot
                for data in like.data.values():
                    data_arr_offset = data.rv - pars['gamma_' + data.label].value
                    _errors = errors[like.model.data_inds[data.label]]
                    _residuals = residuals_no_noise[like.model.data_inds[data.label]]
                    _yerr = dict(array=_errors)
                    fig.add_trace(plotly.graph_objects.Scatter(x=data.t - time_offset, y=data_arr_offset, name=data.label, error_y=_yerr, mode='markers', marker=dict(color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)])), row=1, col=1)
                    fig.add_trace(plotly.graph_objects.Scatter(x=data.t - time_offset, y=_residuals, error_y=_yerr, mode='markers', marker=dict(color=PLOTLY_COLORS[color_index%len(PLOTLY_COLORS)]), showlegend=False), row=2, col=1)
                    color_index += 1
                
        # Labels
        fig.update_xaxes(title_text='BJD - ' + str(time_offset), row=2, col=1)
        fig.update_yaxes(title_text='RVs [m/s]', row=1, col=1)
        fig.update_yaxes(title_text='Residual RVs [m/s]', row=2, col=1)
        fig.update_yaxes(title_text=self.star_name + ' RVs', row=1, col=1)
            
        # Limits
        fig.update_xaxes(range=[t_start - dt / 10 - time_offset, t_end + dt / 10 - time_offset], row=1, col=1)
        fig.update_xaxes(range=[t_start - dt / 10 - time_offset, t_end + dt / 10 - time_offset], row=2, col=1)
        fig.update_layout(template="ggplot2")
        
        # Return the figure for saving or showing
        return fig
        
    def gls_periodogram(self, pars=None, pmin=None, pmax=None, apply_gp=True, remove_planets=None):
        
        # Resolve parameters
        if pars is None:
            pars = self.p0
            
        # Resolve which planets to remove by default
        if remove_planets is None:
            remove_planets = {}
        
        # Resolve period min and period max
        if pmin is None:
            pmin = 1.1
        if pmax is None:
            times = self.data.get_vec('x')
            pmax = np.max(times) - np.min(times)
        if pmax <= pmin:
            raise ValueError("Pmin is less than Pmax")
            
        # Arrays for periodogram
        data_times = np.array([], dtype=float)
        data_rvs = np.array([], dtype=float)
        data_errors = np.array([], dtype=float)
        
        # Loop over likes and add to above arrays
        for like in self.scorer.values():
            
            # Add times and errors
            data_times = np.concatenate((data_times, like.data.get_vec('x')))
            data_errors = np.concatenate((data_errors, like.model.kernel.compute_data_errors(pars)))
            
            # Remove GP from data first
            if like.model.has_gp and apply_gp:
                
                # Copy original parameters, optimizer, and planets dict
                p0cp = copy.deepcopy(self.p0)
                p0_mod = copy.deepcopy(self.p0)
                planets_dict_cp = copy.deepcopy(like.model.planets_dict)
                optimizercp = copy.deepcopy(self.optimizer)
                
                # Loop over planets and remove from parameters
                for planet in planets_dict_cp:
                    if planet in remove_planets:
                        self.remove_planet_pars(p0_mod, planet)
                    
                # Set the new parameters without planets
                self.set_pars(p0_mod)
                self.optimizer = optimizers.NelderMead(scorer=self.optimizer.scorer)
                
                # Set the planets dict to be what's left (difference of two dicts)
                like.model.planets_dict = pcutils.dict_diff(planets_dict_cp, remove_planets)
                
                # Optimize without some planets
                opt_result = self.optimize()
                
                # Alias pbest
                pbest = opt_result['pbest']
                
                # Add to data vec
                data_rvs = np.concatenate((data_rvs, like.residuals_after_kernel(pbest)))
                
                # Set pars, planets dict, and optimizer back to original
                self.set_pars(p0cp)
                like.model.planets_dict = planets_dict_cp
                self.optimizer = optimizercp
                
            else:
                
                # Copy original parameters, optimizer, and planets dict
                p0cp = copy.deepcopy(self.p0)
                p0_mod = copy.deepcopy(self.p0)
                planets_dict_cp = copy.deepcopy(like.model.planets_dict)
                optimizercp = copy.deepcopy(self.optimizer)
                
                # Loop over planets and remove from parameters
                for planet in planets_dict_cp:
                    if planet in remove_planets:
                        self.remove_planet_pars(p0_mod, planet_dict)
                    
                # Set the new parameters without planets
                self.set_pars(p0_mod)
                self.optimizer = optimizers.NelderMead(scorer=self.optimizer.scorer)
                
                # Set the planets dict to be what's left (difference of two dicts)
                like.model.planets_dict = pcutils.dict_diff(planets_dict_cp, remove_planets)
                
                # Optimize without some planets
                opt_result = self.optimize()
                
                # Alias pbest
                pbest = opt_result['pbest']
                
                # Add to data vec
                data_rvs = np.concatenate((data_rvs, like.residuals_after_kernel(pbest)))
                
                # Set pars, planets dict, and optimizer back to original
                self.set_pars(p0cp)
                like.model.planets_dict = planets_dict_cp
                self.optimizer = optimizercp
        
        # Call GLS
        pgram = gls.Gls((data_times, data_rvs, data_errors), Pbeg=pmin, Pend=pmax)
        fig = plotly.subplots.make_subplots(rows=1, cols=1)
        fig.add_trace(plotly.graph_objects.Scatter(x=1 / pgram.f, y=pgram.power, line=dict(color='black', width=1)), row=1, col=1)
        fig.update_xaxes(title_text='Period [days]', row=1, col=1)
        fig.update_yaxes(title_text='Power', row=1, col=1)
        fig.update_layout(template="ggplot2")
        return fig
        

    def rv_period_search(self, pars=None, pmin=None, pmax=None, n_periods=None, n_threads=1, planet_index=None):
        
        # Resolve parameters
        if pars is None:
            pars = self.p0
            
        if planet_index is None:
            planet_index = 1
        
        # Resolve period min and period max
        if pmin is None:
            pmin = 1.1
        if pmax is None:
            times = self.data.get_vec('x')
            pmax = np.max(times) - np.min(times)
        if pmax <= pmin:
            raise ValueError("Pmin is less than Pmax")
        if n_periods is None:
            n_periods = 500
        
        # Periods array    
        periods = np.geomspace(pmin, pmax, num=n_periods)
        args_pass = []
        
        # Construct all args
        for i in range(n_periods):
            args_pass.append((self, periods[i], planet_index))
        
        # Run in parallel
        opt_results = Parallel(n_jobs=n_threads, verbose=0, batch_size=2)(delayed(self._rv_period_search_wrapper)(*args_pass[i]) for i in tqdm.tqdm(range(n_periods)))
        
        lnLs = np.array([-1 * opt_result["fbest"] for opt_result in opt_results])
        
        # Create a plot and return results
        fig = plotly.subplots.make_subplots(rows=1, cols=1)
        fig.add_trace(plotly.graph_objects.Scatter(x=periods, y=lnLs, line=dict(color='black', width=1)), row=1, col=1)
        fig.update_xaxes(title_text='Period [days]', row=1, col=1)
        fig.update_yaxes(title_text='ln(L)', row=1, col=1)
        
        return fig, opt_results
    
    def sample(self, *args, **kwargs):
        self.scorer.redchi2s = []
        sampler_result = super().sample(*args, **kwargs)
        sampler_result["redchi2s"] = self.scorer.redchi2s
        return sampler_result
        

    @staticmethod
    def get_phases(t, per, tc):
        """Given input times, a period, and time of conjunction, returns the phase [0, 1] at each time t.

        Args:
            t (np.ndarray): The times.
            per (float): The period of the planet
            tc (float): The time of conjunction (time of transit).

        Returns:
            np.ndarray: The phases between 0 and 1
        """
        alpha = tc - per / 2
        phases = (t - alpha) % per
        phases /= np.nanmax(phases)
        return phases
    
    @staticmethod
    def generate_all_planet_dicts(planets_dict):
        pset = pcutils.powerset(planets_dict.items())
        planet_dicts = []
        for item in pset:
            pdict = {}
            for subitem in item:
                pdict[subitem[0]] = subitem[1]
            planet_dicts.append(pdict)
        return planet_dicts
    
    @property
    def planets_dict(self):
        return self.scorer.like0.model.planets_dict
    
    def model_comparison(self, do_planets=True, do_gp=False):
        
        model_comp_results: Union[None, list] = None
        
        # Go through every permutation of planet dicts
        if do_planets:
            
            model_comp_results = []
            
            like0 = self.scorer.like0
            
            # Get all combos
            planet_dicts = self.generate_all_planet_dicts(like0.model.planets_dict)
            
            # Loop over combos
            for i, planets_dict in enumerate(planet_dicts):
                
                # Copy self
                _optprob = copy.deepcopy(self)
                
                # Alias pars
                p0 = _optprob.p0
                
                # Remove all other planets except this combo.
                for like in _optprob.scorer.values():
                    like.model.planets_dict = planets_dict
                
                # Pars
                _optprob.set_pars(p0)
                
                # Reset the optimizer
                _optprob.optimizer = optimizers.NelderMead(scorer=_optprob.optimizer.scorer)

                # Run the max like
                opt_result = _optprob.optimize()
                pbest = opt_result['pbest']
                lnL = -1 * opt_result['fbest']
                
                # Run the BIC
                bic = _optprob.optimizer.scorer.compute_bic(pbest)
                
                # Run the AICc
                aicc = _optprob.optimizer.scorer.compute_aicc(pbest)
                
                # Store
                model_comp_results.append({'planets_dict': planets_dict, 'lnL': lnL, 'bic': bic, 'aicc': aicc, 'pbest': pbest})
                
                del _optprob
                
            aicc_vals = np.array([model_comp_result['aicc'] for model_comp_result in model_comp_results], dtype=float)
            ss = np.argsort(aicc_vals)
            model_comp_results = [model_comp_results[ss[i]] for i in range(len(ss))]
            aicc_diffs = np.abs(aicc_vals[ss] - np.nanmin(aicc_vals)) # NOTE: 
            for i, model_comp_result in enumerate(model_comp_results):
                model_comp_result['delta_aicc'] = aicc_diffs[i]
            
        return model_comp_results
        
    @staticmethod
    def _rv_period_search_wrapper(optprob, period, planet_index):
        p0 = optprob.p0
        p0['per' + str(planet_index)].value = period
        optprob.set_pars(p0)
        opt_result = optprob.optimize()
        return opt_result
    
    
class SessionState:
    
    def __init__(self, fname, data=None):
        if data is not None:
            self.data = data
            self.fname = fname
        if os.path.exists(fname) and data is None:
            self = self.load(fname)
        
    def save(self):
        with open(self.fname, 'wb') as f:
            pickle.dump(self, f)
            
    def load(self):
        with open(self.fname, 'wb') as f:
            return pickle.load(f)
    
    def __getitem__(self, key):
        if key == "fname":
            return self.fname
        if key in self.data:
            return self.data[key]
        else:
            return super().__getitem__(key)

def gen_latex_labels(pars, planets_dict):
    """Default Settings for latex labels for orbit fitting. Any GP parameters must be set manually via parameter.latex_str = "$latexname$"

    Args:
        pars (Parameters): The parameters to generate labels for
    
    Returns:
        dict: Keys are parameter names, values are latex labels.
    """
    
    for pname in pars:
        
        # Planets (per, tc, k, ecc, w, sqecosw, sqesinw, other bases added later if necessary)
        if pname.startswith('per') and pname[3:].isdigit():
            pars[pname].latex_str = "$P_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('tc') and pname[2:].isdigit():
            pars[pname].latex_str = "$Tc_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('ecc') and pname[3:].isdigit():
            pars[pname].latex_str = "$e_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('w') and pname[1:].isdigit():
            pars[pname].latex_str = "$\omega_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('k') and pname[1:].isdigit():
            pars[pname].latex_str = "$K_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('sqecosw') and pname[7:].isdigit():
            pars[pname].latex_str = "$\sqrt{e} \cos{\omega}_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('sqesinw') and pname[7:].isdigit():
            pars[pname].latex_str = "$\sqrt{e} \sin{\omega}_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('cosw') and pname[7:].isdigit():
            pars[pname].latex_str = "$\cos{\omega}_{" + planets_dict[int(pname[-1])]["label"] + "}$"
        elif pname.startswith('sinw') and pname[7:].isdigit():
            pars[pname].latex_str = "$\sin{\omega}_{" + planets_dict[int(pname[-1])]["label"] + "}$"
            
        # Gammas
        elif pname.startswith('gamma') and not pname.endswith('dot'):
            pars[pname].latex_str = "$\gamma_{" + pname.split('_')[-1] + "}$"
        elif pname.startswith('gamma') and pname.endswith('_dot'):
            pars[pname].latex_str = "$\dot{\gamma}$"
        elif pname.startswith('gamma') and pname.endswith('_ddot'):
            pars[pname].latex_str = "$\ddot{\gamma}$"
        
        # Jitter
        elif pname.startswith('jitter'):
            pars[pname].latex_str = "$\sigma_{" + pname.split('_')[-1] + "}$"