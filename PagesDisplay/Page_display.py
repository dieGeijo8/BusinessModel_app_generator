from Configuration.Configuration import return_model_full_descriptor_copy, tab_subs_titles
from Questions_settings.Questions_settings import Questions_settings
from PagesDisplay.Visualizations import Visualizations
from Questions_settings.Standard_extensions import Plan
import streamlit as st

class Page_display:


    #method to display a page - the way the tab subsection titles are printed should change when switching to configuration file
    @staticmethod
    def display_page(page):
        local_model_full_descriptor = return_model_full_descriptor_copy()

        page_tabs = list(local_model_full_descriptor[page].keys())
        page_tabs.append('Dashboard')
        tabs = st.tabs(page_tabs)

        for tab, tab_widget in zip(local_model_full_descriptor[page].keys(), tabs[:-1]):
            with tab_widget:

                Plan.print_slider(tab)

                i = 0
                question_codes = list(local_model_full_descriptor[page][tab].keys())
                for question_code, question_code_index in zip( question_codes, range(len(question_codes)) ):

                    if question_code_index == 0:

                        st.header(tab_subs_titles[i])
                        i += 1

                    if question_code_index != 0 and question_code[:2] != question_codes[question_code_index - 1][:2] and i <= (len(tab_subs_titles) - 1):

                        st.header(tab_subs_titles[i])
                        i += 1

                    Questions_settings.display_question(local_model_full_descriptor, page, tab, question_code)

        with tabs[-1]:
            # lineplot
            lp = Visualizations.stages_line_plot(page)

            st.plotly_chart(lp, theme="streamlit", use_container_width=True)

            #barplot
            bp = Visualizations.stages_barplot(page)

            st.plotly_chart(bp, theme="streamlit", use_container_width=True)
