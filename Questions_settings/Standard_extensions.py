import pandas as pd
import streamlit as st
import google.cloud.firestore
from Configuration.Configuration import pages, return_model_descriptor_copy

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
    activate_weights = True

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
            print(pages)
            for page in pages:

                tabs_current_values = []
                tabs_plan_values = []
                tabs_weights = []

                for tab in st.session_state['overview']['Current'].keys():
                    if tab[:1] == page:

                        tabs_current_values.append(
                            st.session_state['overview']['Current'][tab] * Weights.weights_list[weights_index])

                        #standard extension
                        Plan.plan_by_page_first_method(tabs_plan_values, tab, weights_index)
                        # tabs_plan_values.append(
                        #     st.session_state['overview']['Plan'][tab] * Weights.weights_list[weights_index])
                        tabs_weights.append(Weights.weights_list[weights_index])
                        weights_index += 1

                ovw_aggregated_by_page[page] = {'Current': sum(tabs_current_values) / sum(tabs_weights)}

                #standard extension
                Plan.plan_by_page_second_method(page, ovw_aggregated_by_page, tabs_plan_values, tabs_weights)
                                                #'Plan': sum(tabs_plan_values) / sum(tabs_weights)}

        else:

            for page in pages:

                tabs_current_values = []
                tabs_plan_values = []

                for tab in st.session_state['overview']['Current'].keys():
                    if tab[:1] == page:

                        tabs_current_values.append(st.session_state['overview']['Current'][tab])

                        #standard extension
                        Plan.plan_by_page_first_method_noweights(tabs_plan_values, tab)
                        # tabs_plan_values.append(st.session_state['overview']['Plan'][tab])

                ovw_aggregated_by_page[page] = {'Current': sum(tabs_current_values) / len(tabs_current_values)}

                #standard extension
                Plan.plan_by_page_second_method_noweights(page, ovw_aggregated_by_page, tabs_plan_values)
                                               # 'Plan': sum(tabs_plan_values) / len(tabs_plan_values)}

        return ovw_aggregated_by_page.copy()


class Plan:

    name = 'Plan'
    activate_plan = True

    #decorator to check if the variable activate plan is set to false or true
    @staticmethod
    def plan_decorator(func):
        def wrapper(*args, **kwargs):
            if Plan.activate_plan == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper


    # initialize the plan values, set in the overview by the corresponding method in session state variables module
    @plan_decorator
    @staticmethod
    def initialize_plan(ovw):
        db = google.cloud.firestore.Client.from_service_account_json("Firestore/firestore_key.json")

        company_collection = db.collection(st.session_state.company)

        company_ovw_document = company_collection.document('overview')

        local_model_descriptor = return_model_descriptor_copy()

        try:
            ovw_plan_values = company_ovw_document.get().to_dict()

            ovw[Plan.name] = ovw_plan_values[Plan.name]

        except:
            tabs = []

            for page in local_model_descriptor.keys():
                for tab in local_model_descriptor[page].keys():
                    tabs.append(tab)

            plans_per_tab = dict(zip(tabs, [1]*len(tabs)))

            ovw[Plan.name] = plans_per_tab



    #methods for ovw df - they are called in the Session state dataframes class
    @plan_decorator
    @staticmethod
    def add_plan_to_column_list(ordered_columns_list):
        ordered_columns_list.append(Plan.name)

    @plan_decorator
    @staticmethod
    def add_plan_to_ovw(df_ovw):
        df_ovw[Plan.name] = [st.session_state['overview'][Plan.name][tab] for tab in
                          st.session_state['overview'][Plan.name].keys()]




    #methods for ovw df aggregated by page - they are called in the Session state dataframes class
    @plan_decorator
    @staticmethod
    def plan_by_page_first_method(tabs_plan_values, tab, weights_index):
        tabs_plan_values.append(st.session_state['overview'][Plan.name][tab] * Weights.weights_list[weights_index])

    @plan_decorator
    @staticmethod
    def plan_by_page_first_method_noweights(tabs_plan_values, tab):
        tabs_plan_values.append(st.session_state['overview'][Plan.name][tab])

    @plan_decorator
    @staticmethod
    def plan_by_page_second_method(page, ovw_aggregated_by_page, tabs_plan_values, tabs_weights):
        ovw_aggregated_by_page[page][Plan.name] = sum(tabs_plan_values) / sum(tabs_weights)

    @plan_decorator
    @staticmethod
    def add_plan_to_df_for_vis(ovw_df_aggregated_by_page, return_df):
        return_df[Plan.name] = [ovw_df_aggregated_by_page[page][Plan.name] for page in ovw_df_aggregated_by_page.keys()]

    @plan_decorator
    @staticmethod
    def plan_by_page_second_method_noweights(page, ovw_aggregated_by_page, tabs_plan_values):
        ovw_aggregated_by_page[page][Plan.name] = sum(tabs_plan_values) / len(tabs_plan_values)




    #methods for the visualization of the aggregated ovw df - they are called in the visualization class
    @plan_decorator
    @staticmethod
    def ovw_barplot_plan_lines(fig, df):
        plan_avg = sum(df[Plan.name].tolist()) / len(df[Plan.name].tolist())
        fig.add_shape(type="line", line_color='black', line_width=2, opacity=0.5, line_dash="dot",
                      x0=0, x1=1, xref="paper", y0=plan_avg, y1=plan_avg, yref="y")
        fig.add_annotation(text='Avg. planned stage', x='5', y=plan_avg + 0.1, showarrow=False)




    #methods to show the slider and set the plan values with the callback - called in page display
    @plan_decorator
    @staticmethod
    def slider_plan_callback(tab):
        st.session_state['overview'][Plan.name][tab] = st.session_state[tab + '_plan_slider']

    @plan_decorator
    @staticmethod
    def print_slider(tab):
        st.slider('Set the plan value to reach for this tab:', min_value=1, max_value=5,
                  value=st.session_state['overview'][Plan.name][tab],
                  on_change=Plan.slider_plan_callback, args=(tab,), key=tab + '_plan_slider')
