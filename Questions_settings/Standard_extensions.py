import pandas as pd
import streamlit as st
from Configuration.Configuration import pages

class Checkbox:

    name = 'Checkbox'
    activate_checkbox = True # this is what controls if activate the checkbox or not

    #decorator to check if activate the checkbox or not
    @staticmethod
    def checkbox_decorator(func):
        def wrapper(*args, **kwargs):
            if Checkbox.activate_checkbox == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper

    #support method
    @staticmethod
    def get_full_question_code(page, tab, question_code):
        return str(page) + '_' + str(tab) + '_' + str(question_code)



    #for first setting
    @checkbox_decorator
    @staticmethod
    def set_checkbox(company_data, page, tab, question_code):
        st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)] = \
            company_data[page][tab][question_code][Checkbox.name]

    #for deleting
    @checkbox_decorator
    @staticmethod
    def del_checkbox(page, tab, question_code):
        del st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]




    #append checkbox to the names of the values collected per each question
    @checkbox_decorator
    @staticmethod
    def append_checkbox_value_name(values_names_list):
        values_names_list.append(Checkbox.name)


    #add the checkbox value to the values collected per each question
    @checkbox_decorator
    @staticmethod
    def add_checkbox_value(question_data_values_dict, page, tab, question_code):
        question_data_values_dict[Checkbox.name] = \
            st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]

    #aad the checkbox value to the first values registered per each question
    @checkbox_decorator
    @staticmethod
    def first_checkbox_value(first_question_data_values_dict):
        first_question_data_values_dict[Checkbox.name] = False




    #display checkbox per each question + callback
    @checkbox_decorator
    @staticmethod
    def checkbox_callback(page, tab, question_code):
        st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)] = \
            st.session_state['checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]

    @checkbox_decorator
    @staticmethod
    def display_checkbox(page, tab, question_code):
        st.checkbox('Question not relevant to my assessment, dont\'t consider it',
                                    value=st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab,question_code)],
                                    on_change=Checkbox.checkbox_callback, args=(page, tab, question_code),
                                    key='checkbox' + Checkbox.get_full_question_code(page, tab, question_code)
                                    )

    @staticmethod
    def checkbox_disable_othervalues(page, tab, question_code):
        if Checkbox.activate_checkbox == True:

            return st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]
        else:
            return False


class Weights:

    name = 'Weight'
    activate_weights = False

    #this is just here to give a value to weights, in the real case they will be set from the configuration file
    df = pd.read_excel('Configuration/15M.xlsx', sheet_name='Overview', skiprows=3, usecols='A:D,L')
    df.columns = ['Tab', 'Code', 'Description', 'NCode', 'Weight']
    df = df.astype({'Tab': str})
    df = df.dropna(subset=['NCode'])

    weights_list = df['Weight'].to_list()


    #decorator to check if the variable activate weights is set to false or true
    @staticmethod
    def weights_decorator(func):
        def wrapper(*args, **kwargs):
            if Weights.activate_weights == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper


    #add 'Weight' to the column list
    @weights_decorator
    @staticmethod
    def add_weights_to_columnslist(columns_list):
        columns_list.append(Weights.name)

    #add the weights column to the overview dataframe
    @weights_decorator
    @staticmethod
    def add_weights_column(df_ovw):
        df_ovw[Weights.name] = Weights.weights_list

    #returns a dict with the following structure: page(key) - Current(key): average value, Plan(key): average value, weighted just if setted
    @staticmethod
    def get_weighted_current_and_plan_by_page(df_ovw):

        ovw_aggregated_by_page = {}

        if Weights.name in df_ovw.columns:

            weights_index = 0

            for page in pages:

                tabs_current_values = []
                tabs_plan_values = []
                tabs_weights = []

                for tab in st.session_state['overview']['Current'].keys():
                    if tab[:1] == page:

                        tabs_current_values.append(
                            st.session_state['overview']['Current'][tab] * Weights.weights_list[weights_index])
                        tabs_plan_values.append(
                            st.session_state['overview']['Plan'][tab] * Weights.weights_list[weights_index])
                        tabs_weights.append(Weights.weights_list[weights_index])
                        weights_index += 1

                ovw_aggregated_by_page[page] = {'Current': sum(tabs_current_values) / sum(tabs_weights),
                                                'Plan': sum(tabs_plan_values) / sum(tabs_weights)}

        else:

            for page in pages:

                tabs_current_values = []
                tabs_plan_values = []

                for tab in st.session_state['overview']['Current'].keys():
                    if tab[:1] == page:

                        tabs_current_values.append(st.session_state['overview']['Current'][tab])
                        tabs_plan_values.append(st.session_state['overview']['Plan'][tab])

                ovw_aggregated_by_page[page] = {'Current': sum(tabs_current_values) / len(tabs_current_values),
                                                'Plan': sum(tabs_plan_values) / len(tabs_plan_values)}

        return ovw_aggregated_by_page.copy()

