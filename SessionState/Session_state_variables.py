import streamlit as st
from Configuration_file.Configuration import return_model_descriptor_copy
from DataManagement.DataManagement import DataManagement
from Questions_settings.Questions_settings import Questions_settings
from Extensions.Standard_extensions.Checkbox import Checkbox
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Ideas import Ideas

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
            st.session_state['company_list'] = DataManagement.get_company_list()

        if 'dont_display_data' not in st.session_state:
            st.session_state['dont_display_data'] = False


    # initialize the session state variables containing the data for the session state company
    @staticmethod
    def initialize_company_session_state():
        local_model_descriptor = return_model_descriptor_copy()

        company_data = DataManagement.get_company_data()

        for page in local_model_descriptor.keys():
            for tab in local_model_descriptor[page].keys():
                for question_code in local_model_descriptor[page][tab]:

                    Questions_settings.sessionstate_set_question_data_values(company_data, page, tab, question_code)

    # delete the session state variables containing the data for the session state company
    @staticmethod
    def delete_company_session_state():
        local_model_descriptor = return_model_descriptor_copy()

        for page in local_model_descriptor.keys():
            for tab in local_model_descriptor[page].keys():
                for question_code in local_model_descriptor[page][tab]:

                    Questions_settings.sessionstate_delete_question_data_values(page, tab, question_code)


    # initialize the session state variable overview - dictionary with the following structure: 'Current' - tab: score, and if setted 'Plan' - tab: score
    @staticmethod
    def initialize_company_overview_session_state():
        local_model_descriptor = return_model_descriptor_copy()

        scores_per_tab = {}

        for page in local_model_descriptor.keys():
            for tab in local_model_descriptor[page].keys():
                tab_score = []

                for question_code in local_model_descriptor[page][tab]:

                    if Checkbox.checkbox_disable_othervalues(page, tab, question_code) != True:  # related to checkbox standard extension

                        question_values = Questions_settings.get_question_data_values(page, tab, question_code)
                        tab_score.append(question_values['Stage'])

                scores_per_tab[tab] = round(sum(tab_score) / len(tab_score), 1)


        ovw = {}
        ovw['Current'] = scores_per_tab

        #standard extensions
        Plan.initialize_plan(ovw)

        Ideas.initialize_ideas(ovw)

        print(ovw)
        st.session_state['overview'] = ovw


    # update the current values of the session state ovw dictionary
    @staticmethod
    def update_company_overview_session_state():
        local_model_descriptor = return_model_descriptor_copy()

        scores_per_tab = {}

        for page in local_model_descriptor.keys():
            for tab in local_model_descriptor[page].keys():
                tab_score = []

                for question_code in local_model_descriptor[page][tab]:

                    if Checkbox.checkbox_disable_othervalues(page, tab, question_code) != True:  # related to checkbox standard extension

                        question_values = Questions_settings.get_question_data_values(page, tab, question_code)
                        tab_score.append(question_values['Stage'])

                scores_per_tab[tab] = round(sum(tab_score) / len(tab_score), 1)



        st.session_state['overview']['Current'] = scores_per_tab


    # delete the session state variable overview
    @staticmethod
    def delete_company_overview_session_state():
        del st.session_state['overview']