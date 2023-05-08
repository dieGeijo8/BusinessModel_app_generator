import streamlit as st
from SessionState.Session_state_variables import Session_state_variables
from Firestore.FirestoreAPI import FirestoreAPI
from Thread_safety.ThreadSafety import ThreadSafety

#add the written company to the company list to make it selectable from the select box
def callback_textinput():

    st.session_state.company_list.append(st.session_state.textinput_value)

    st.session_state.textinput_value = ''
    st.session_state.first_textinput_value = ''

#change session state company - delete if needed and initialize
def callback_selectbox():

    if st.session_state.company != '':
        Session_state_variables.delete_company_session_state()
        Session_state_variables.delete_company_overview_session_state()

        ThreadSafety.unlock_company()

    st.session_state.company = st.session_state.selectbox_value
    st.session_state.first_selectbox_value = st.session_state.company_list.index(st.session_state.company)

    ThreadSafety.lock_company()

    Session_state_variables.initialize_company_session_state()
    Session_state_variables.initialize_company_overview_session_state()



if __name__ == "__main__" :

    st.write('Welcome to the home page')

    if 'webapp_initialized' not in st.session_state:

        st.session_state.webapp_initialized = 1
        Session_state_variables.initialize_webapp_sessionstate()



    st.selectbox('Select the company you want to analyze.', options=st.session_state.company_list,
                 index=st.session_state.first_selectbox_value,
                 on_change=callback_selectbox, key='selectbox_value')

    with st.expander('Do you want to register a new company?'):
        st.text_input('Write the name of the company and submit. After that you can select it from the dedicated scrollable menu.',
                      value=st.session_state.first_textinput_value,
                      on_change=callback_textinput, key='textinput_value')

    st.button('Submit', on_click=FirestoreAPI.submit_button, disabled=st.session_state.dont_display_data)

    ThreadSafety.lock_warning_display()

