from Configuration.Configuration import return_model_full_descriptor_copy, tab_subs_titles
from Questions_settings.Questions_settings import Questions_settings
import streamlit as st

class Page_display:

    #save the new value in the reendering session state variable
    @staticmethod
    def stage_callback(page, tab, question_code):

        st.session_state['reendering_stage' + str(page) + '_' + str(tab) + '_' + str(question_code)] = \
            int(st.session_state['stage' + str(page) + '_' + str(tab) + '_' + str(question_code)])

    #method to display a page - the way the tab subsection titles are printed should change when switching to configuration file
    @staticmethod
    def display_page(page):
        local_model_full_descriptor = return_model_full_descriptor_copy()
        tabs = st.tabs(local_model_full_descriptor[page].keys())

        for tab, tab_widget in zip(local_model_full_descriptor[page].keys(), tabs):
            with tab_widget:

                i = 0
                question_codes = list(local_model_full_descriptor[page][tab].keys())
                for question_code, question_code_index in zip( question_codes, range(len(question_codes)) ):

                    if question_code_index == 0:

                        st.header(tab_subs_titles[i])
                        i += 1

                    if question_code_index != 0 and question_code[:2] != question_codes[question_code_index - 1][:2] and i <= 3:

                        st.header(tab_subs_titles[i])
                        i += 1

                    Questions_settings.display_question(local_model_full_descriptor, page, tab, question_code)

