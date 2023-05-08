import pandas as pd
import streamlit as st
from Configuration.Configuration import pages
from Extensions.Standard_extensions.Plan import Plan

class Weights_per_tab:

    name = 'Weight'
    activate_tab_weights = False

    #this is just here to give a value to weights, in the real case they will be set from the configuration file
    df = pd.read_excel('Configuration/15M.xlsx', sheet_name='Overview', skiprows=3, usecols='A:D,L')
    df.columns = ['Tab', 'Code', 'Description', 'NCode', 'Weight']
    df = df.astype({'Tab': str})
    df = df.dropna(subset=['NCode'])

    tab_weights_list = df['Weight'].to_list()


    #decorator to check if the variable activate weights is set to false or true
    @staticmethod
    def weights_decorator(func):
        def wrapper(*args, **kwargs):
            if Weights_per_tab.activate_tab_weights == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper


    #add 'Weight' to the column list
    @weights_decorator
    @staticmethod
    def add_weights_to_columnslist(columns_list):
        columns_list.append(Weights_per_tab.name)

    #add the weights column to the overview dataframe
    @weights_decorator
    @staticmethod
    def add_weights_column(df_ovw):
        df_ovw[Weights_per_tab.name] = Weights_per_tab.tab_weights_list




    #returns a dict with the following structure: page(key) - Current(key): average value, Plan(key): average value, weighted just if setted
    @staticmethod
    def __aggregation_with_weights():

        ovw_aggregated_by_page = {}

        weights_index = 0

        for page in pages:

            tabs_current_values = []
            tabs_plan_values = []
            tabs_weights = []

            for tab in st.session_state['overview']['Current'].keys():
                if tab[:1] == page:
                    tabs_current_values.append(
                        st.session_state['overview']['Current'][tab] * Weights_per_tab.tab_weights_list[weights_index])

                    # standard extension
                    Plan.plan_by_page_first_method(tabs_plan_values, tab, Weights_per_tab.tab_weights_list, weights_index)

                    tabs_weights.append(Weights_per_tab.tab_weights_list[weights_index])

                    weights_index += 1

            ovw_aggregated_by_page[page] = {'Current': round(sum(tabs_current_values) / sum(tabs_weights), 2)}

            # standard extension
            Plan.plan_by_page_second_method(page, ovw_aggregated_by_page, tabs_plan_values, tabs_weights)

        return ovw_aggregated_by_page.copy()

    @staticmethod
    def __aggregation_no_weights():

        ovw_aggregated_by_page = {}

        for page in pages:

            tabs_current_values = []
            tabs_plan_values = []

            for tab in st.session_state['overview']['Current'].keys():
                if tab[:1] == page:
                    tabs_current_values.append(st.session_state['overview']['Current'][tab])

                    # standard extension
                    Plan.plan_by_page_first_method_noweights(tabs_plan_values, tab)

            ovw_aggregated_by_page[page] = {'Current': round(sum(tabs_current_values) / len(tabs_current_values), 2)}

            # standard extension
            Plan.plan_by_page_second_method_noweights(page, ovw_aggregated_by_page, tabs_plan_values)

        return ovw_aggregated_by_page.copy()

    @staticmethod
    def get_eventual_weighted_scores_by_page():

        if Weights_per_tab.activate_tab_weights == True:

            aggr_dict = Weights_per_tab.__aggregation_with_weights()
            return aggr_dict

        else:

            aggr_dict = Weights_per_tab.__aggregation_no_weights()
            return aggr_dict


class Weights_per_page:

    activate_page_weights = True
    pages_weights_list = dict(zip(pages, [0.25, 0.25, 0.25, 0.10, 0.15]))

    @staticmethod
    def page_weights_decorator(func):
        def wrapper(*args, **kwargs):
            if Weights_per_page.activate_page_weights == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper


    #methods for per page ovw display
    @staticmethod
    def display_page_weights_first_method(columns_number):
        if Weights_per_page.activate_page_weights == True:

            columns_number = columns_number + 1
            return columns_number
        else:
            return columns_number


    @page_weights_decorator
    @staticmethod
    def display_page_weights_second_method(scores_per_page_dict, page):
        scores_per_page_dict[page]['Weight'] = Weights_per_page.pages_weights_list[page]


    @page_weights_decorator
    @staticmethod
    def display_page_weights_third_method(metrics_titles):
        metrics_titles['Weight'] = 'Page weight'


    #method to get the eventual per page weighted overall overview score
    @staticmethod
    def get_eventual_weighted_scores_overall():

        scores_per_page_dict = Weights_per_tab.get_eventual_weighted_scores_by_page()

        current_per_page_list = []
        plan_per_page_list = []
        weights_per_page = []

        for page in pages:

            if Weights_per_page.activate_page_weights == True:

                current_per_page_list.append(scores_per_page_dict[page]['Current']*Weights_per_page.pages_weights_list[page])

                if Plan.activate_plan == True:
                   plan_per_page_list.append(scores_per_page_dict[page][Plan.name]*Weights_per_page.pages_weights_list[page])

                weights_per_page.append(Weights_per_page.pages_weights_list[page])

            else:

                current_per_page_list.append(scores_per_page_dict[page]['Current'])

                if Plan.activate_plan == True:
                    plan_per_page_list.append(scores_per_page_dict[page][Plan.name])


        if Weights_per_page.activate_page_weights == True:

            current_score = round(sum(current_per_page_list) / sum(weights_per_page), 2)
            plan_score = round(sum(plan_per_page_list) / sum(weights_per_page), 2)

            return {'Current': current_score, 'Plan': plan_score}

        else:

            current_score = round(sum(current_per_page_list) / len(current_per_page_list), 2)
            plan_score = round(sum(plan_per_page_list) / len(plan_per_page_list), 2)

            return {'Current': current_score, 'Plan': plan_score}



