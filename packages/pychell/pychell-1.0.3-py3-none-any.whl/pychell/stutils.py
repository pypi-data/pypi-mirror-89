import streamlit as st
import numpy as np

# Run the specified action
# Max like
if comps["optim_button"]:
    
    # Run optimize
    opt_result = optprob.optimize()
    
    # Set pars
    optprob.set_pars(opt_result['pbest'])
    
    # Display Results
    st.markdown('# Optimize Results')
    opt_result['pbest'].pretty_print()
    st.text(repr(opt_result['pbest']))
    st.markdown('## Function calls: ' + str(opt_result['fcalls']))
    st.markdown('## ln(L): ' + str(-1 * opt_result['fbest']))
    
    # Full RV plot
    st.markdown('## Full RV Plot')
    figfull = optprob.rv_plot(opt_result=opt_result, n_model_pts=5000)
    st.plotly_chart(figfull)
    figfull.write_html(star_name.replace(' ', '_') + '_rvs_full_' + pcutils.gendatestr(True) + '.html')
    
    # Phased rv plot
    st.markdown('## Phased Planets')
    for planet in planets_dict:
        figplanet = optprob.rv_phase_plot(planet_index=planet, opt_result=opt_result)
        st.plotly_chart(figplanet)
    
else:
    opt_result = None
    
    

class StreamlitComponent:
    
    def __init__(self, label="", *args, **kwargs):
        self.label = label
        
    def write(self, *args, **kwargs):
        pass

class DataSelector(StreamlitComponent):
    
    def __init__(self, data):
        super().__init__(label="data_selector")
        self.data = data
        return self.write()
        
    def write(self):
        self.comps = {}
        # Use or ignore any instruments as st checkboxes.
        for data in self.data.values():
            self.comps["use_" + data.label] = st.checkbox(label=data.label + " " + str(len(data.t)), value=True)
            if not use_data:
                del self.data[inst]
        return self.comps
    
    
class RVActions(StreamlitComponent):
    
    def __init__(self, optprob):
        super().__init__(label="data_selector")
        self.data = data
        return self.write()
        
    def write(self):
        self.comps = {}
        
        # Primary actions
        st.markdown('## Actions')
        self.comps["optim_button"] = st.button(label='Run Max Like')
        self.comps["sample_button"] = st.button(label='Run MCMC')
        self.comps["model_comp_button"] = st.button(label='Model Comparison')
        self.comps["period_search_button"] = st.button('Period Search')
        
        # Period search options
        st.markdown('## Period Search Options:')
        st.markdown('### Periodogram Type:')
        self.comps["persearch_kind_input"] = st.radio(label="", options=["GLS", "Brute Force"])
        self.comps["persearch_remove"] = {}
        st.markdown('### Remove Planets:')
        remove_planets_pgram = []
        for planet_index in self.optprob.planets_dict:
            self.comps["persearch_remove"][planet_index] = st.checkbox(label=str(planet_index))
            if self.comps["persearch_remove"][planet_index]:
                remove_planets_pgram.append(planet_index)
    
        self.comps["remove_planet_inputs"] = remove_planets_pgram
        pgcols = st.beta_columns(2)
        self.comps["persearch_min_input"] = pgcols[0].text_input(label='Period min', value=1.1)
        self.comps["persearch_max_input"] = pgcols[1].text_input(label='Period max', value=100)
        return self.comps