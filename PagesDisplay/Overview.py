import pandas as pd
import streamlit as st
from SessionState.Session_state_dataframes import Session_state_dataframes
from SessionState.Session_state_variables import Session_state_variables
from PagesDisplay.Visualizations import Visualizations
from Configuration.Configuration import pages, pages_names
from Extensions.Standard_extensions.Weights import Weights_per_tab, Weights_per_page

class Overview:

    @staticmethod
    def display_overall_total():
        st.header('Overall scores')

        scores_overall_dict = Weights_per_page.get_eventual_weighted_scores_overall()

        if len(scores_overall_dict.keys()) == 1:

            columns = st.columns(len(scores_overall_dict.keys()))
        else:

            scores_overall_dict['Plan - Current'] = round(scores_overall_dict['Plan'] - scores_overall_dict['Current'], 2)
            columns = st.columns(len(scores_overall_dict.keys()) + 1)

        metrics_titles = {'Current': 'Overall current'}

        if len(columns) > 1:
            metrics_titles['Plan'] = 'Overall plan'
            metrics_titles['Plan - Current'] = 'Overall plan - current'


        for key, column_widget, metric_title in zip(scores_overall_dict.keys(), columns, metrics_titles.keys()):

            with column_widget:
                st.metric(label=metrics_titles[metric_title], value=str(scores_overall_dict[key]))




    @staticmethod
    def display_overall_page(page):

        scores_per_page_dict = Weights_per_tab.get_eventual_weighted_scores_by_page()

        if len(scores_per_page_dict[page].keys()) == 1:

            columns = st.columns(len(scores_per_page_dict[page].keys()))
        else:

            scores_per_page_dict[page]['Plan - Current'] = round(scores_per_page_dict[page]['Plan'] - scores_per_page_dict[page]['Current'], 2)
            columns = st.columns(len(scores_per_page_dict[page].keys()) + 1)

        metrics_titles = {'Current': 'Overall page current'}

        if len(columns) > 1:
            metrics_titles['Plan'] = 'Overall page plan'
            metrics_titles['Plan - Current'] = 'Overall page plan - current'


        for key, column_widget, metric_title in zip(scores_per_page_dict[page].keys(), columns, metrics_titles.keys()):

            with column_widget:
                st.metric(label=metrics_titles[metric_title], value=str(scores_per_page_dict[page][key]))


    @staticmethod
    def display_overview():

        #get an updated copy of the ovw df
        Session_state_variables.update_company_overview_session_state()
        df_ovw = Session_state_dataframes.get_ovw_df_copy()

        tabs = st.tabs(['Data', 'Dashboard'])

        with tabs[0]:

            Overview.display_overall_total()

            start = 0
            pages_titles_index = 0

            for j in range(len(df_ovw)):

                if j == 0:
                    # first iteration - always print a header
                    st.header(pages_names[pages_titles_index])

                    Overview.display_overall_page(pages[pages_titles_index])

                    pages_titles_index += 1

                    # if the tab is different from the tab of the previous row I am changing page so
                    # I print the correspondant df part and the next part header
                elif df_ovw.loc[j, 'Tab'][:1] != df_ovw.loc[j - 1, 'Tab'][:1]:

                    st.dataframe(df_ovw.iloc[start:j])

                    start = j

                    if pages_titles_index <= (len(pages) - 1):

                        st.header(pages_names[pages_titles_index])

                        Overview.display_overall_page(pages[pages_titles_index])

                        pages_titles_index += 1

                    # last df part
                elif j == len(df_ovw) - 1:

                    st.dataframe(df_ovw.iloc[start:j+1])

        with tabs[1]:

            bp = Visualizations.overview_barplot()

            st.plotly_chart(bp, theme="streamlit", use_container_width=True)

