from Configuration.Configuration import return_model_full_descriptor_copy, tab_subs_titles
from Questions_settings.Questions_settings import Questions_settings
from PagesDisplay.Visualizations import Visualizations
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Ideas import Ideas
import streamlit as st

class Page_display:

    @staticmethod
    def __dashboard_display(page):
        st.header(st.session_state.company + ' - ' + 'page ' + page)
        # lineplot
        st.subheader('Stage value by question')

        lp = Visualizations.stages_line_plot(page)

        st.plotly_chart(lp, theme="streamlit", use_container_width=True)

        with st.expander('Line plot description'):
            st.write('The line plot above shows the stage value for each question of the page. The color of the line indicates the tab of the question.')

        st.write('')
        st.write('')

        # barplot
        st.subheader('Average stage value by tab')

        bp = Visualizations.stages_barplot(page)

        st.plotly_chart(bp, theme="streamlit", use_container_width=True)

        with st.expander('Bar plot description'):
            st.write('The bar plot above shows the average stage value per each tab of the page.')

        st.write('')
        st.write('')

        # wordlocud
        st.subheader('Remarks most frequent words')

        wc = Visualizations.remarks_wordcloud(page)

        if isinstance(wc, str):

            st.warning(wc)
        else:
            st.write('')

            st.image(wc)

            with st.expander('Word cloud explanation'):
                st.write('The Remarks of each question of the page are grouped into a single text that is used to produce this word cloud. It shows the most frequent words and the size of the word is proportional to the relative frequency.')

    #method to display a page - the way the tab subsection titles are printed should change when switching to configuration file
    @staticmethod
    def display_page(page):
        local_model_full_descriptor = return_model_full_descriptor_copy()

        page_tabs = list(local_model_full_descriptor[page].keys())
        page_tabs.append('Dashboard')
        tabs = st.tabs(page_tabs)

        for tab, tab_widget in zip(local_model_full_descriptor[page].keys(), tabs[:-1]):
            with tab_widget:

                col1, col2 = st.columns(2)
                with col1:
                    st.write('')
                with col2:
                    st.warning('The company selected is: ' + st.session_state.company)

                if Plan.return_activated_plan() or Ideas.return_activated_ideas():
                    st.write('---')

                Plan.print_slider(tab)

                Ideas.print_textarea(tab)

                if Plan.return_activated_plan() or Ideas.return_activated_ideas():
                    st.write('---')

                i = 0
                question_codes = list(local_model_full_descriptor[page][tab].keys())
                for question_code, question_code_index in zip( question_codes, range(len(question_codes)) ):

                    if question_code_index == 0:

                        st.subheader(tab_subs_titles[i])
                        i += 1

                    if question_code_index != 0 and question_code[:2] != question_codes[question_code_index - 1][:2] and i <= (len(tab_subs_titles) - 1):

                        st.subheader(tab_subs_titles[i])
                        i += 1

                    Questions_settings.display_question(local_model_full_descriptor, page, tab, question_code)
                    st.write(' ')
                    st.write(' ')

        with tabs[-1]:

            Page_display.__dashboard_display(page)

