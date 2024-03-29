import streamlit as st
import plotly.graph_objects as go
from DataManagement.DataManagement import DataManagement
from Configuration_file.Configuration import return_model_descriptor_copy, max_stage

class Plan:

    name = 'Plan'

    @staticmethod
    def set():

        if 'default_activate_plan' not in st.session_state:
            st.session_state.default_activate_plan = False

        if 'activate_plan' not in st.session_state:
            st.session_state.activate_plan = False


    #very simple support method for divider display
    @staticmethod
    def return_activated_plan():
        if st.session_state.activate_plan == True:

            return True
        else:

            return False

    #decorator to check if the variable activate plan is set to false or true
    @staticmethod
    def plan_decorator(func):
        def wrapper(*args, **kwargs):
            if st.session_state.activate_plan == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper

    @plan_decorator
    @staticmethod
    def initialize_plan(ovw):
        ovw[Plan.name] = DataManagement.get_company_overview_plan()


    @plan_decorator
    @staticmethod
    def add_plan_to_column_list(ordered_columns_list):
        ordered_columns_list.append(Plan.name)

    @plan_decorator
    @staticmethod
    def add_plan_to_ovw(df_ovw):
        #ensure right order
        local_model_descriptor = return_model_descriptor_copy()
        tabs = []
        for page in local_model_descriptor.keys():
            tabs = tabs + list(local_model_descriptor[page].keys())

        df_ovw[Plan.name] = [st.session_state['overview'][Plan.name][tab] for tab in tabs]



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


    @staticmethod
    def __conversion_function(x):

        new_x = 0 + (100 - 0) * (x - 1) / (max_stage - 1)

        return round(new_x, 2)

    @plan_decorator
    @staticmethod
    def plan_ovw_as_percentage(df_ovw):
        df_ovw[Plan.name] = [str(Plan.__conversion_function(x)) + '%' for x in df_ovw[Plan.name].to_list()]


    #methods for the visualization of the aggregated ovw df - they are called in the visualization class
    @plan_decorator
    @staticmethod
    def ovw_barplot_plan_lines(fig, df, annotation_y):
        plan_avg = sum(df[Plan.name].tolist()) / len(df[Plan.name].tolist())
        fig.add_shape(type="line", line_color='black', line_width=2, opacity=0.5, line_dash="dot",
                      x0=0, x1=1, xref="paper", y0=plan_avg, y1=plan_avg, yref="y")
        fig.add_annotation(text='Avg. planned value', x=df['Page'].tolist()[len(df['Page'].tolist()) - 1],
                      y=plan_avg + annotation_y, showarrow=False)

    @plan_decorator
    @staticmethod
    def ovw_radarchart_plan(fig, subset_df_ovw):
        fig.add_trace(go.Scatterpolar(r=subset_df_ovw['Plan'].tolist(), theta=subset_df_ovw['Section number'].tolist(), name='Plan',
                                      customdata=subset_df_ovw['Section name'].tolist(),
                                      fill='toself',
                                      line_color='#FFC000'))




    #methods for the overall ovw per page display and for the overall ovw display
    @staticmethod
    def ovw_per_page_display_first_method():
        if st.session_state.activate_plan == True:

            return 3
        else:

            return 1
    @plan_decorator
    @staticmethod
    def ovw_per_page_display_second_method(scores_per_page_dict, page):
        scores_per_page_dict[page]['Plan - Current'] = round(scores_per_page_dict[page]['Plan'] - scores_per_page_dict[page]['Current'], 2)

    @plan_decorator
    @staticmethod
    def ovw_per_page_display_third_method(metrics_titles):

        metrics_titles['Plan'] = 'Overall page plan'
        metrics_titles['Plan - Current'] = 'Overall page plan - current'

    @plan_decorator
    @staticmethod
    def ovw_overall_display_second_method(scores_dict):
        scores_dict['Plan - Current'] = round(scores_dict['Plan'] - scores_dict['Current'], 2)

    @plan_decorator
    @staticmethod
    def ovw_overall_display_third_method(metrics_titles):

        metrics_titles['Plan'] = 'Overall plan'
        metrics_titles['Plan - Current'] = 'Overall plan - current'






    #methods to show the slider and set the plan values with the callback - called in page display
    @plan_decorator
    @staticmethod
    def slider_plan_callback(tab):
        st.session_state['overview'][Plan.name][tab] = st.session_state[tab + '_plan_slider']

    @plan_decorator
    @staticmethod
    def print_slider(tab):
        st.subheader('Plan')

        st.markdown(
            """<style>
            div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
            font-size: 17px;
            </style>
            """, unsafe_allow_html=True)

        st.slider('Set the plan value to reach for this tab:', min_value=1, max_value=max_stage,
                  disabled=st.session_state.dont_display_data,
                  value=st.session_state['overview'][Plan.name][tab],
                  on_change=Plan.slider_plan_callback, args=(tab,), key=tab + '_plan_slider')