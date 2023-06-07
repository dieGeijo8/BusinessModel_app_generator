import time
import streamlit as st
from Configuration_file.Configuration import get_page_title, get_page_text
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

    # if the previous selected company was null there's nothing to delete or unlock
    if st.session_state.company != '' and st.session_state.history != '':

        ThreadSafety.unlock_company()

    # set the new company whatever is null or not
    st.session_state.company = st.session_state.selectbox_value
    st.session_state.first_selectbox_value = st.session_state.company_list.index(st.session_state.company)

    # if the new company selected is null there's nothing to lock or get configuration for
    if st.session_state.company != '':

        ThreadSafety.lock_company()

        #get company configuration
        StandardExtensions_configuration.get_extension_config()

    # if the new company is not null get the versions avalaibles and set the version to not selected
    if st.session_state.company != '':

        st.session_state.company_history = DataManagement.get_history_for_company()
        st.session_state.history = ''

    # otherwise not display any selection option
    else:

        st.session_state.company_history = ['']
        st.session_state.history = ''



def callback_selectbox_history():

    # there was a previous selection
    if st.session_state.company != '' and st.session_state.history != '':

        Session_state_variables.delete_company_session_state()
        Session_state_variables.delete_company_overview_session_state()

    st.session_state.history = st.session_state.history_select_box_value

    # if there's a company selected do this
    if st.session_state.company != '' and st.session_state.history != '':

        #intialize session state
        Session_state_variables.initialize_company_session_state()
        Session_state_variables.initialize_company_overview_session_state()

    if st.session_state.history == 'New compilation':

        st.session_state.selected_mode = 1

    # otherwise do nothing


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


def set_company(company):

    st.session_state.company = company

    st.session_state.company_history = DataManagement.get_history_for_company()

    if 'company_locked' not in st.session_state:

        st.session_state.company_locked = 1
        ThreadSafety.lock_company()

    StandardExtensions_configuration.set_extensions()

    # get company configuration
    StandardExtensions_configuration.get_extension_config()

    # if st.session_state.history != '':
    #
    #     # initialize session state
    #     Session_state_variables.initialize_company_session_state()
    #     Session_state_variables.initialize_company_overview_session_state()

def callback_submit_button():

    # submit company data
    DataManagement.submit_button()

    # reset company to no selection - especially to release the lock
    st.session_state.first_selectbox_value = st.session_state.company_list.index('')

    st.experimental_rerun()

def callback_logout():

    if st.session_state.company != '':

        ThreadSafety.unlock_company()

    #st.session_state.clear()
    st.session_state.company = ''
    st.session_state.authentication_status  = None


    st.cache_data.clear()
    st.cache_resource.clear()


def callback_mode():

    if st.session_state.history == 'New compilation':

        st.session_state.selected_mode = 1

    else:

        options = ['Overwrite', 'Save as new']

        st.session_state.selected_mode = options.index(st.session_state.mode_selectbox)




if __name__ == "__main__":

    try:

        if 'webapp_initialized' not in st.session_state:
            st.session_state.webapp_initialized = 1
            Session_state_variables.initialize_webapp_sessionstate()

        aut = Users.user_authentication()
        authenticator, authentication_status, name, username = aut[0], aut[1], aut[2], aut[3]

        st.session_state.authentication_status = authentication_status

        if authentication_status == True:

            col1, col2 = st.columns([3, 1])

            with col1:

                st.header(get_page_title('Home'))
            with col2:

                st.image('Configuration_file/sc_logo.png', use_column_width=True)


            st.button(label='Logout', on_click=callback_logout)

            st.markdown(get_page_text('Home'), unsafe_allow_html=True)

            user_rights = Users.get_user_rights(username)


            if user_rights == 'admin':

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.selectbox('Select a company.', options=st.session_state.company_list,
                                 index=st.session_state.first_selectbox_value,
                                 on_change=callback_selectbox, key='selectbox_value')

                with col2:

                    st.selectbox('Explore an old assessment?', options=st.session_state.company_history,
                                 index=st.session_state.company_history.index(st.session_state.history),
                                 on_change=callback_selectbox_history, key='history_select_box_value')

                with col3:

                    st.selectbox('Overwrite or save as new?', options=['Overwrite', 'Save as new'],
                                 index=st.session_state.selected_mode,
                                 on_change=callback_mode, key='mode_selectbox')

                with st.expander('Do you want to register a new company?'):

                        company_registration_form()

            elif user_rights == 'normal':

                user_company = Users.get_user_company(username)

                set_company(user_company)

                col1, col2 = st.columns(2)

                with col1:

                    st.selectbox('Explore an old assessment?', options=st.session_state.company_history,
                                 index=st.session_state.company_history.index(st.session_state.history),
                                 on_change=callback_selectbox_history, key='history_select_box_value')

                with col2:

                    st.selectbox('Overwrite or save as new?', options=['Overwrite', 'Save as new'],
                                 index=st.session_state.selected_mode,
                                 on_change=callback_mode, key='mode_selectbox')



            st.button('Submit data', on_click=callback_submit_button, disabled=st.session_state.dont_display_data)

            ThreadSafety.lock_warning_display()

        elif authentication_status == None:

            st.warning('Please enter your username and password.')

        elif authentication_status == False:

            st.error('Username or password is incorrect.')

    except:

        st.warning('An error occured. Please go back to the home page and reload the web app.')