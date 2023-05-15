import pandas as pd
import streamlit as st
import math
from SessionState.Session_state_dataframes import Session_state_dataframes
from SessionState.Session_state_variables import Session_state_variables
from PagesDisplay.Visualizations import Visualizations
from Configuration.Configuration import pages, pages_names
from Extensions.Standard_extensions.Weights import Weights_per_tab, Weights_per_page
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Percentages import Percentages
from Extensions.Standard_extensions.Ideas import Ideas


class Overview:

    @staticmethod
    def display_overall_total():
        st.subheader('Overall scores')

        scores_overall_dict = Weights_per_page.get_eventual_weighted_scores_overall()

        # standard extension
        columns_number = Plan.ovw_per_page_display_first_method()

        columns = st.columns(columns_number)

        # standard extension
        Plan.ovw_overall_display_second_method(scores_overall_dict)

        metrics_titles = {'Current': 'Overall current'}

        # standard extension
        Plan.ovw_overall_display_third_method(metrics_titles)

        for key, column_widget, metric_title in zip(scores_overall_dict.keys(), columns, metrics_titles.keys()):

            with column_widget:

                value = Percentages.overall_as_percentage(scores_overall_dict, key)

                st.metric(label=metrics_titles[metric_title], value=value)



    @staticmethod
    def display_overall_page(page):

        scores_per_page_dict = Weights_per_tab.get_eventual_weighted_scores_by_page()

        #standard extensions
        columns_number = Plan.ovw_per_page_display_first_method()

        columns_number = Weights_per_page.display_page_weights_first_method(columns_number)


        columns = st.columns(columns_number)

        #standard extensions
        Plan.ovw_per_page_display_second_method(scores_per_page_dict, page)

        Weights_per_page.display_page_weights_second_method(scores_per_page_dict, page)


        metrics_titles = {'Current': 'Overall page current'}

        #standard extensions
        Plan.ovw_per_page_display_third_method(metrics_titles)

        Weights_per_page.display_page_weights_third_method(metrics_titles)


        for key, column_widget, metric_title in zip(scores_per_page_dict[page].keys(), columns, metrics_titles.keys()):

            with column_widget:

                Percentages.page_print_overall(scores_per_page_dict, page, key, metrics_titles, metric_title)


    @staticmethod
    def display_overview():

        #get an updated copy of the ovw df
        Session_state_variables.update_company_overview_session_state()
        df_ovw = Session_state_dataframes.get_ovw_df_copy()

        if all(x == '' for x in df_ovw['Description'].tolist()):
            df_ovw = df_ovw.drop('Description', axis=1)

        #standard extension
        Percentages.ovw_as_percentage(df_ovw)


        tabs = st.tabs(['Data', 'Dashboard'])

        with tabs[0]:
            st.header(st.session_state.company + ' overview')

            Overview.display_overall_total()

            start = 0
            pages_titles_index = 0

            for j in range(len(df_ovw)):

                if j == 0:
                    # first iteration - always print a header
                    st.subheader(str(pages_titles_index + 1) + ' - ' + pages_names[pages_titles_index])

                    Overview.display_overall_page(pages[pages_titles_index])

                    pages_titles_index += 1

                    # if the tab is different from the tab of the previous row I am changing page so
                    # I print the correspondant df part and the next part header
                elif df_ovw.loc[j, 'Tab number'][:1] != df_ovw.loc[j - 1, 'Tab number'][:1]:

                    st.dataframe(df_ovw.iloc[start:j])

                    start = j

                    if pages_titles_index <= (len(pages) - 1):

                        st.subheader(str(pages_titles_index + 1) + ' - ' + pages_names[pages_titles_index])

                        Overview.display_overall_page(pages[pages_titles_index])

                        pages_titles_index += 1

                    # last df part
                elif j == len(df_ovw) - 1:

                    st.dataframe(df_ovw.iloc[start:j+1])

        with tabs[1]:

            st.header(st.session_state.company + ' overview')


            st.subheader('Average score by page')

            bp = Visualizations.overview_barplot()

            st.plotly_chart(bp, theme="streamlit", use_container_width=True)
            with st.expander('Barplot description'):
                st.write('The above graph shows the average current and plan(if selected) score per each page of the model. The horizontal lines displayed indicate the average current and plan values across all the pages.')


            st.write('')
            st.write('')

            st.subheader('Average score by tab')

            col1, col2 = st.columns([1, 4])

            with col1:
                page_selected = st.selectbox(label='Choose a page.', options=pages)
            with col2:
                st.write('')

            rc = Visualizations.overview_radarchart(page_selected)

            st.plotly_chart(rc, theme="streamlit", use_container_width=True)

            with st.expander('Radar chart description'):
                st.write('The above graph shows the average current and plan(if selected) score per each tab of the model. By selecting the page through the scrollable menu on the left you can explore all the tabs of the model by page.')

            st.write('')
            st.write('')

            Ideas.ideas_keywords_by_page_visualization()