import streamlit as st
from Configuration import return_model_descriptor_copy, return_model_full_descriptor_copy
from FirestoreAPI import FirestoreAPI
from Questions_settings import Questions_settings

class Session_state_variables:

    #initialize the session state variables needed for loading the web app
    @staticmethod
    def initialize_webapp_sessionstate():

        if 'company' not in st.session_state:
            st.session_state.company = ''

        if 'first_selectbox_value' not in st.session_state:
            st.session_state['first_selectbox_value'] = 0

        if 'first_textinput_value' not in st.session_state:
            st.session_state['first_textinput_value'] = ''

        if 'company_list' not in st.session_state:
            st.session_state['company_list'] = FirestoreAPI.get_company_list()

    #initialize the session state variables containing the data for the session state company
    @staticmethod
    def initialize_company_session_state():
        local_model_descriptor = return_model_descriptor_copy()

        company_data = FirestoreAPI.get_company_data()

        for page in local_model_descriptor.keys():
            for tab in local_model_descriptor[page].keys():
                for question_code in local_model_descriptor[page][tab]:

                    Questions_settings.sessionstate_set_question_data_values(company_data, page, tab, question_code)

    #delete the session state variables containing the data for the session state company
    @staticmethod
    def delete_company_session_state():
        local_model_descriptor = return_model_descriptor_copy()

        for page in local_model_descriptor.keys():
            for tab in local_model_descriptor[page].keys():
                for question_code in local_model_descriptor[page][tab]:

                    Questions_settings.sessionstate_delete_question_data_values(page, tab, question_code)
