import pandas as pd
import streamlit as st
from Questions_settings.Questions_settings import Questions_settings
from Configuration_file.Configuration import return_model_descriptor_copy, return_model_ovw_descriptor_copy
from Extensions.Standard_extensions.Checkbox import Checkbox
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Weights import Weights_per_tab
from Extensions.Standard_extensions.Ideas import Ideas


class Session_state_dataframes:

    #get all the data registered for the questions of the page as a df with columns values [Tab plus question codes, tab, ... values ...]
    @staticmethod
    def get_df_page_visualizations(page):
        #get the local model descriptor to iterate
        local_model_descriptor = return_model_descriptor_copy()

        #create the dict, to transform then in df, including all the needed keys
        values_names = Questions_settings.get_question_values_name()

        page_data = {key: [] for key in values_names}


        tabs = []
        tab_plus_question_codes = []

        for tab in local_model_descriptor[page].keys():
            for question_code in local_model_descriptor[page][tab]:

                if Checkbox.checkbox_disable_othervalues(page, tab, question_code) != True:  # related to checkbox standard extension
                    # save the tab
                    tabs.append(tab)
                    # save the tab plus question code
                    tab_plus_question_codes.append(str(tab) + '_' + str(question_code))


                    # get current values of the question
                    question_data = Questions_settings.get_question_data_values(page, tab, question_code)

                    for value_name in values_names:
                        page_data[value_name].append(question_data[value_name])


        page_data['Code'] = tab_plus_question_codes
        page_data['Tab'] = tabs

        return pd.DataFrame.from_dict(page_data)

    #get the updated ovw df with the following columns - 'Tab', 'Description', 'Current', 'Plan', and eventually 'Weight'
    @staticmethod
    def get_ovw_df_copy():
        # get the ovw part that doesn't change - tab + description
        df_ovw = return_model_ovw_descriptor_copy()

        # standard extensions
        Weights_per_tab.add_weights_column(df_ovw)

        df_ovw['Current'] = [st.session_state['overview']['Current'][tab] for tab in
                             st.session_state['overview']['Current'].keys()]

        # standard extensions
        Plan.add_plan_to_ovw(df_ovw)

        Ideas.add_ideas_to_ovw(df_ovw)

        # reorder columns
        ordered_columns_list = ['Tab number', 'Tab', 'Description', 'Current']

        # standard extensions
        Plan.add_plan_to_column_list(ordered_columns_list)
        Ideas.add_ideas_to_column_list(ordered_columns_list)
        Weights_per_tab.add_weights_to_columnslist(ordered_columns_list)

        df_ovw = df_ovw[ordered_columns_list]

        return df_ovw.copy()

    #uses a dict with the following structure: page(key) - Current(key): average value, Plan(key): average value, weighted just if setted
    #and returns a df with the following columns: page - plan - current
    @staticmethod
    def get_ovw_df_aggregated_by_page_copy():

        #standard extension
        ovw_dict_aggregated_by_page = Weights_per_tab.get_eventual_weighted_scores_by_page()

        return_df = pd.DataFrame({})

        return_df['Page'] = ovw_dict_aggregated_by_page.keys()
        return_df['Page'] = return_df['Page'].astype(str)

        return_df['Current'] = [ovw_dict_aggregated_by_page[page]['Current'] for page in ovw_dict_aggregated_by_page.keys()]

        #standard extension
        Plan.add_plan_to_df_for_vis(ovw_dict_aggregated_by_page, return_df)

        return return_df.copy()



