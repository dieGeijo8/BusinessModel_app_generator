import streamlit as st
from Configuration_file.Configuration import max_stage
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Weights import Weights_per_tab


class Percentages:

    name = 'Percentages'

    @staticmethod
    def set():

        if 'default_activate_percentages' not in st.session_state:
            st.session_state.default_activate_percentages = True

        if 'activate_percentages' not in st.session_state:
            st.session_state.activate_percentages = True

    #activate_percentages = st.session_state.activate_percentages

    @staticmethod
    def percentages_decorator(func):
        def wrapper(*args, **kwargs):
            if st.session_state.activate_percentages == False:

                a = 0  # just to do something

            else:

                func(*args, **kwargs)

        return wrapper



    #conversion from number from 1 to 5 to percentage
    @staticmethod
    def __conversion_function(x):

        new_x = 0 + (100 - 0) * (x - 1) / (max_stage - 1)

        return round(new_x, 2)



    #conversion of current and Plan column for display
    @percentages_decorator
    @staticmethod
    def ovw_as_percentage(df_ovw):

        df_ovw['Current'] = [str(Percentages.__conversion_function(x)) + '%' for x in df_ovw['Current'].to_list()]

        Weights_per_tab.weights_per_tab_as_percentages(df_ovw)

        Plan.plan_ovw_as_percentage(df_ovw)

    @staticmethod
    def overall_as_percentage(scores_overall_dict, key):

        if st.session_state.activate_percentages == True:

            if key == 'Plan - Current':

                value = str(round(Percentages.__conversion_function(scores_overall_dict[Plan.name])\
                        - Percentages.__conversion_function(scores_overall_dict['Current']), 2)) + '%'
            else:

                value = str(Percentages.__conversion_function(scores_overall_dict[key])) + '%'
        else:

            value = str(scores_overall_dict[key])

        return value

    @staticmethod
    def page_print_overall(scores_per_page_dict, page, key, metrics_titles, metric_title):
        if st.session_state.activate_percentages == True:

            if metric_title == 'Weight':
                value = str(round(100 * scores_per_page_dict[page][key], 2))

            elif metric_title == 'Plan - Current':

                value = str(Percentages.__conversion_function(scores_per_page_dict[page][Plan.name])\
                        - Percentages.__conversion_function(scores_per_page_dict[page]['Current']))

            else:
                value = str(Percentages.__conversion_function(scores_per_page_dict[page][key]))

            st.metric(label=metrics_titles[metric_title], value=value + '%')
        else:

            st.metric(label=metrics_titles[metric_title], value=str(scores_per_page_dict[page][key]))



    @percentages_decorator
    @staticmethod
    def percentages_for_visualizations_firstmethod(df):

        for column in df.columns:

            if isinstance(df[column].tolist()[0], (int, float)) == True:

                df[column] = [Percentages.__conversion_function(x) for x in df[column].tolist()]

    @percentages_decorator
    @staticmethod
    def percentages_for_visualizations_secondmethod(fig):

        fig.update_layout(yaxis_range=[0, 100.5])
        tickvals = [0, 20, 40, 60, 80, 100]

        fig.update_yaxes(ticktext=[str(x) + '%' for x in tickvals], tickvals=tickvals)
        fig.update_layout(bargap=0.5)

    @staticmethod
    def percentages_for_visualizations_thirdmethod():
        if st.session_state.activate_percentages == True:
            return 2.5
        else:
            return 0.5

    @percentages_decorator
    @staticmethod
    def percentages_for_visualizations_fourthmethod(fig):

        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100.5])), showlegend=True)

        tickvals = [0, 20, 40, 60, 80, 100]
        fig.update_layout(polar=dict(radialaxis=dict(tickvals=tickvals, tickangle=45, ticktext=[str(x) + '%' for x in tickvals])))

        fig.update_polars(angularaxis_linewidth=0.1)