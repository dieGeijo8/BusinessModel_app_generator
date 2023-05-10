import streamlit as st
from DataManagement.DataManagement import DataManagement
from Extensions.Standard_extensions.Checkbox import Checkbox
from Extensions.Standard_extensions.Percentages import Percentages
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Ideas import Ideas
from Extensions.Standard_extensions.Weights import Weights_per_tab, Weights_per_page

class StandardExtensions_configuration:

    @staticmethod
    def extension_form():
        st.checkbox('Plan extension', value=st.session_state.default_activate_plan, key='plan_extension')
        st.checkbox('Percentage extension', value=st.session_state.default_activate_percentages, key='percentage_extension')
        st.checkbox('Checkbox extension', value=st.session_state.default_activate_checkbox, key='checkbox_extension')
        st.checkbox('Ideas extension', value=st.session_state.default_activate_ideas, key='ideas_extension')

        if st.session_state.default_activate_tab_weights == True:
            st.checkbox('Tab weights extension', value=st.session_state.default_activate_tab_weights, key='tab_weights_extension')

        if st.session_state.default_activate_page_weights == True:
            st.checkbox('Page weights extension', value=st.session_state.default_activate_page_weights, key='page_weights_extension')

    @staticmethod
    def set_extension_config():
        configuration = dict(zip([Plan.name, Percentages.name, Checkbox.name, Ideas.name],
                                 [st.session_state['plan_extension'], st.session_state['percentage_extension'],
                                  st.session_state['checkbox_extension'], st.session_state['ideas_extension']]))

        if st.session_state.default_activate_tab_weights == True:
            configuration[Weights_per_tab.name] = st.session_state['tab_weights_extension']

        if st.session_state.default_activate_page_weights == True:
            configuration[Weights_per_page.name] = st.session_state['page_weights_extension']

        DataManagement.set_company_configuration(st.session_state.textinput_value, configuration)

    @staticmethod
    def get_extension_config():
        configuration = DataManagement.get_company_configuration()

        st.session_state.activate_plan = configuration[Plan.name]
        st.session_state.activate_percentages = configuration[Percentages.name]
        st.session_state.activate_checkbox = configuration[Checkbox.name]
        st.session_state.activate_ideas = configuration[Ideas.name]

        if st.session_state.default_activate_tab_weights == True:
            st.session_state.activate_tab_weights = configuration[Weights_per_tab.name]

        if st.session_state.default_activate_page_weights == True:
            st.session_state.activate_page_weights = configuration[Weights_per_page.name]