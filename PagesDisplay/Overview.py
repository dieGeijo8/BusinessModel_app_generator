import streamlit as st
from Configuration.Configuration import return_model_ovw_descriptor_copy
from SessionState.Session_state_variables import Session_state_variables
class Overview:

    @staticmethod
    def display_overview():
        # update the ovw values
        Session_state_variables.initialize_company_overview_session_state()
        # get the ovw part that doesn't change
        df_ovw = return_model_ovw_descriptor_copy()


        df_ovw['Current'] = [st.session_state['overview']['Current'][tab] for tab in st.session_state['overview']['Current'].keys()]
        df_ovw['Plan'] = [st.session_state['overview']['Plan'][tab] for tab in st.session_state['overview']['Plan'].keys()]

        #reorder columns
        df_ovw = df_ovw[['Section', 'Code', 'Description', 'NCode', 'Current', 'Plan', 'Weight']]

        #display the df
        st.experimental_data_editor(df_ovw, key='data_editor_ovw')

