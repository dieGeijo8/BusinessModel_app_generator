import streamlit as st
from rake_nltk import Rake
from Configuration.Configuration import return_model_descriptor_copy, pages
from DataManagement.DataManagement import DataManagement

class Ideas:

    name = 'Ideas'

    @staticmethod
    def set():

        if 'default_activate_ideas' not in st.session_state:
            st.session_state.default_activate_ideas = False

        if 'activate_ideas' not in st.session_state:
            st.session_state.activate_ideas = False

    # very simple support method for divider display
    @staticmethod
    def return_activated_ideas():
        if st.session_state.activate_ideas == True:

            return True
        else:

            return False

    @staticmethod
    def ideas_decorator(func):
        def wrapper(*args, **kwargs):
            if st.session_state.activate_ideas == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper

    @ideas_decorator
    @staticmethod
    def initialize_ideas(ovw):
        ovw[Ideas.name] = DataManagement.get_company_overview_ideas()

    @ideas_decorator
    @staticmethod
    def add_ideas_to_column_list(ordered_columns_list):
        ordered_columns_list.append(Ideas.name)

    @ideas_decorator
    @staticmethod
    def add_ideas_to_ovw(df_ovw):
        #ensure right order
        local_model_descriptor = return_model_descriptor_copy()
        tabs = []
        for page in local_model_descriptor.keys():
            tabs = tabs + list(local_model_descriptor[page].keys())

        df_ovw[Ideas.name] = [st.session_state['overview'][Ideas.name][tab] for tab in tabs]



    @staticmethod
    def __get_ideas_page_keywords(page):

        page_text = ''

        for tab in st.session_state['overview']['Ideas'].keys():
            if tab[:1] == page:

                page_text += st.session_state['overview']['Ideas'][tab]

                page_text += ' '

        r =Rake()
        r.extract_keywords_from_text(page_text)

        keywords = r.get_ranked_phrases()

        if len(keywords) >= 3:

            return keywords[:3]
        else:

            return ['not enough words']

    @ideas_decorator
    @staticmethod
    def ideas_keywords_by_page_visualization():
        st.subheader('Ideas keywords by page')

        col1, col2 = st.columns([1, 4])

        with col1:
            page_selected = st.selectbox(label='Choose a page.', options=pages, key='selectbox_ideas_visualization')
        with col2:
            st.write('')

        keywords = Ideas.__get_ideas_page_keywords(page_selected)

        if len(keywords) == 3:

            st.markdown(
                """<hr style="height:5px;border:none;color:#42A7B3;background-color:#42A7B3;"><hr style="height:3px;border:none;color:#FFC000;background-color:#FFC000;">""",
                unsafe_allow_html=True)


            col1, col2, col3 = st.columns(3)
            st.markdown("""
                            <style>
                            .big-font {
                                font-size:25px !important;
                                text-align:center;
                            }
                            </style>
                            """, unsafe_allow_html=True)

            with col1:

                st.write('')
                st.markdown('<p class="big-font">'+keywords[0]+'</p>', unsafe_allow_html=True)
                #st.metric(label='kw1', value=keywords[0], label_visibility='hidden')

            with col2:

                st.write('')
                st.markdown('<p class="big-font">' + keywords[1] + '</p>', unsafe_allow_html=True)
                #st.metric(label='kw2', value=keywords[1], label_visibility='hidden')
            with col3:

                st.write('')
                st.markdown('<p class="big-font">' + keywords[2] + '</p>', unsafe_allow_html=True)
                #st.metric(label='kw3', value=keywords[2], label_visibility='hidden')


            st.markdown(
                """<hr style="height:3px;border:none;color:##FFC000;background-color:#FFC000;"><hr style="height:5px;border:none;color:#42A7B3;background-color:#42A7B3;">""",
                unsafe_allow_html=True)

        else:

            st.warning('Not enough keywords')

        with st.expander('Keywords explanation'):
            st.write('The Ideas you wrote for each tab of the page are grouped in a single text from which 3 keywords are extracted using the Rapid Automatic Keyword Extraction algorithm.')



    @ideas_decorator
    @staticmethod
    def textbox_ideas_callback(tab):
        st.session_state['overview'][Ideas.name][tab] = st.session_state[tab + '_ideas_textarea']

    @ideas_decorator
    @staticmethod
    def print_textarea(tab):
        st.subheader('Ideas')

        st.markdown(
            """<style>
            div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
            font-size: 17px;
            </style>
            """, unsafe_allow_html=True)

        st.text_area('Write the ideas for this tab.',
                  disabled=st.session_state.dont_display_data,
                  value=st.session_state['overview'][Ideas.name][tab],
                  on_change=Ideas.textbox_ideas_callback, args=(tab,), key=tab + '_ideas_textarea')