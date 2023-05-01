import pandas as pd
import streamlit as st
from Questions_settings.Questions_settings import Questions_settings
from Configuration.Configuration import return_model_descriptor_copy
class Session_state_dataframes:

    #get all the data registered for the questions of the page as a df with columns values [Tab plus question codes, tab, ... values ...]
    @staticmethod
    def df_page_visualizations(page):
        #get the local model descriptor to iterate
        local_model_descriptor = return_model_descriptor_copy()

        #create the dict, to transform then in df, including all the needed keys
        values_names = Questions_settings.get_question_values_name()

        page_data = {key: [] for key in values_names}


        tabs = []
        tab_plus_question_codes = []

        for tab in local_model_descriptor[page].keys():
            for question_code in local_model_descriptor[page][tab]:

                #save the tab
                tabs.append(tab)
                # save the tab plus question code
                tab_plus_question_codes.append(str(tab) + '_' + str(question_code))

                #get current values of the question
                question_data = Questions_settings.get_question_data_values(page, tab, question_code)

                for value_name in values_names:
                    page_data[value_name].append(question_data[value_name])


        page_data['Code'] = tab_plus_question_codes
        page_data['Tab'] = tabs

        return pd.DataFrame.from_dict(page_data)


