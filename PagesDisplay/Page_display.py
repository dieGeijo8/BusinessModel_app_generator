import streamlit as st
from Configuration_file.Configuration import return_model_full_descriptor_copy, pages_names, get_page_title, get_page_text
from Configuration_file.ParseConfigFile import ParseConfigFile
from Questions_settings.Questions_settings import Questions_settings
from PagesDisplay.Visualizations import Visualizations
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Ideas import Ideas


class Page_display:

    @staticmethod
    def __dashboard_display(page):
        st.header(st.session_state.company + ' - ' + 'page ' + page)
        # lineplot
        st.subheader('Stage value by question')

        lp = Visualizations.stages_line_plot(page)

        st.plotly_chart(lp, theme="streamlit", use_container_width=True)

        with st.expander('Line plot description'):
            st.write('The line plot above shows the stage value for each question of the page. The questions are identified with a code that has the following structure: Tab number-Initials of the name of the subsection-Question number inside the subsection. The color of the line indicates the tab of the question.')

        st.write('')
        st.write('')

        # barplot
        st.subheader('Average stage value by section')

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
        if st.session_state.authentication_status == True:

            if st.session_state.company != '' and st.session_state.history != '':

                local_model_full_descriptor = return_model_full_descriptor_copy()

                page_dict = ParseConfigFile.get_page_dictionary()
                tab_dict = ParseConfigFile.get_tab_dictionary()

                page_tabs = list(local_model_full_descriptor[page].keys())
                page_tabs.insert(0, 'Intro')
                page_tabs.append('Dashboard')

                tabs = st.tabs(page_tabs)

                with st.sidebar:
                    st.write('Company: ***' + st.session_state.company + '***')
                    st.write('Version: ***' + st.session_state.history + '***')
                    st.image('Configuration_file/sc_logo.png', use_column_width=True)

                with tabs[0]:

                    st.header(get_page_title(pages_names[int(page) - 1]))
                    st.markdown(get_page_text(pages_names[int(page) - 1]), unsafe_allow_html=True)

                for tab, tab_widget in zip(local_model_full_descriptor[page].keys(), tabs[1:-1]):
                    with tab_widget:

                        if isinstance(ParseConfigFile.get_tab_dictionary()[tab], str) == True:
                            st.subheader(ParseConfigFile.get_tab_dictionary()[tab])

                        if Plan.return_activated_plan() or Ideas.return_activated_ideas():
                            st.write('---')

                        Plan.print_slider(tab)

                        Ideas.print_textarea(tab)

                        if Plan.return_activated_plan() or Ideas.return_activated_ideas():
                            st.write('---')

                        i = 0
                        question_codes = list(local_model_full_descriptor[page][tab].keys())

                        tab_subsections = ParseConfigFile.get_subsections_by_tab(page_dict[page], tab_dict[tab])

                        for question_code, question_code_index in zip(question_codes, range(len(question_codes))):

                            if question_code_index == 0 and isinstance(tab_subsections[0], str) == True:

                                st.subheader(tab_subsections[i])
                                i += 1

                            if question_code_index != 0 \
                                    and question_code[:question_code.find('_') + 1] != question_codes[question_code_index - 1][:question_codes[question_code_index - 1].find('_') + 1] \
                                    and i <= (len(tab_subsections) - 1):

                                st.subheader(tab_subsections[i])
                                i += 1

                            Questions_settings.display_question(local_model_full_descriptor, page, tab, question_code)
                            st.write(' ')
                            st.write(' ')

                with tabs[-1]:

                    Page_display.__dashboard_display(page)

            else:

                st.warning('You have to select a company and a version.')

        else:

            st.warning('You have to authenticate.')

