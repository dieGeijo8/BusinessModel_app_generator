import time
import streamlit as st
from SessionState.Session_state_variables import Session_state_variables
from DataManagement.DataManagement import DataManagement
from Thread_safety.ThreadSafety import ThreadSafety
from Extensions.Standard_extensions.StandardExtensions_configuration import StandardExtensions_configuration
from Checks.Checks import Checks
from UsersManagement.Users import Users

#add the written company to the company list to make it selectable from the select box
# def callback_textinput():
#
#     st.session_state.company_list.append(st.session_state.textinput_value)
#
#     ThreadSafety.add_company_to_lock(st.session_state.textinput_value)
#
#     st.session_state.textinput_value = ''
#     st.session_state.first_textinput_value = ''

#change session state company - delete if needed and initialize
def callback_selectbox():

    if st.session_state.company != '':
        Session_state_variables.delete_company_session_state()
        Session_state_variables.delete_company_overview_session_state()

        ThreadSafety.unlock_company()

    if st.session_state.selectbox_value != ' ':

        st.session_state.company = st.session_state.selectbox_value
        st.session_state.first_selectbox_value = st.session_state.company_list.index(st.session_state.company)

        ThreadSafety.lock_company()

        #get company configuration
        StandardExtensions_configuration.get_extension_config()

        #intialize session state
        Session_state_variables.initialize_company_session_state()
        Session_state_variables.initialize_company_overview_session_state()


def company_registration_form():
    with st.form('company_registration_form', clear_on_submit=True):

        st.text_input('Write the name of the company you want to register', key='textinput_value')

        StandardExtensions_configuration.extension_form()

        registered = st.form_submit_button('Register company')

        if registered:

            if Checks.check_if_company_valid(st.session_state.textinput_value) == True:

                #make the new company selectable
                st.session_state.company_list.append(st.session_state.textinput_value)

                ThreadSafety.add_company_to_lock(st.session_state.textinput_value)

                #set the configuration
                StandardExtensions_configuration.set_extension_config()

                #needed to update the company list
                st.experimental_rerun()

            else:

                st.warning('Invalid company')

def callback_logout():

    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.clear()


if __name__ == "__main__":

    if 'webapp_initialized' not in st.session_state:
        st.session_state.webapp_initialized = 1
        Session_state_variables.initialize_webapp_sessionstate()

    aut = Users.user_authentication()
    authenticator, authentication_status, name, username = aut[0], aut[1], aut[2], aut[3]

    st.session_state.authentication_status = authentication_status

    if authentication_status == True:

        st.write('Welcome to the home page')

        st.selectbox('Select the company you want to analyze.', options=st.session_state.company_list,
                     index=st.session_state.first_selectbox_value,
                     on_change=callback_selectbox, key='selectbox_value')

        with st.expander('Do you want to register a new company?'):

                company_registration_form()



        st.button('Submit data', on_click=DataManagement.submit_button, disabled=st.session_state.dont_display_data)

        ThreadSafety.lock_warning_display()

        st.button(label='Logout', on_click=callback_logout)

    elif authentication_status == None:

        st.warning('Please enter your username and password.')

    elif authentication_status == False:

        st.error('Username or password is incorrect.')

