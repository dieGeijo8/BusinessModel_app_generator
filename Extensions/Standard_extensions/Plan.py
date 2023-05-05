import streamlit as st
from Firestore.FirestoreAPI import FirestoreAPI

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

    @plan_decorator
    @staticmethod
    def initialize_plan(ovw):

        ovw['Plan'] = FirestoreAPI.get_company_overview_plan()


    @plan_decorator
    @staticmethod
    def add_plan_to_column_list(ordered_columns_list):
        ordered_columns_list.append(Plan.name)

    @plan_decorator
    @staticmethod
    def add_plan_to_ovw(df_ovw):
        df_ovw[Plan.name] = [st.session_state['overview'][Plan.name][tab] for tab in
                          st.session_state['overview'][Plan.name].keys()]




    #methods for ovw df aggregated by page - they are called in the Weights class
    @plan_decorator
    @staticmethod
    def plan_by_page_first_method(tabs_plan_values, tab, weights_list, weights_index):
        tabs_plan_values.append(st.session_state['overview'][Plan.name][tab] * weights_list[weights_index])

    @plan_decorator
    @staticmethod
    def plan_by_page_first_method_noweights(tabs_plan_values, tab):
        tabs_plan_values.append(st.session_state['overview'][Plan.name][tab])

    @plan_decorator
    @staticmethod
    def plan_by_page_second_method(page, ovw_aggregated_by_page, tabs_plan_values, tabs_weights):
        ovw_aggregated_by_page[page][Plan.name] = round(sum(tabs_plan_values) / sum(tabs_weights), 2)

    @plan_decorator
    @staticmethod
    def add_plan_to_df_for_vis(ovw_df_aggregated_by_page, return_df):
        return_df[Plan.name] = [ovw_df_aggregated_by_page[page][Plan.name] for page in ovw_df_aggregated_by_page.keys()]

    @plan_decorator
    @staticmethod
    def plan_by_page_second_method_noweights(page, ovw_aggregated_by_page, tabs_plan_values):
        ovw_aggregated_by_page[page][Plan.name] = round(sum(tabs_plan_values) / len(tabs_plan_values), 2)




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
        st.header('Plan')

        st.slider('Set the plan value to reach for this tab:', min_value=1, max_value=5,
                  value=st.session_state['overview'][Plan.name][tab],
                  on_change=Plan.slider_plan_callback, args=(tab,), key=tab + '_plan_slider')