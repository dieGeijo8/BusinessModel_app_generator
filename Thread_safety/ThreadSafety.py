import threading
import streamlit as st
from DataManagement.DataManagement import DataManagement


#global variables - visible to all processes
lock = threading.Lock()
locks_companies = dict(zip(DataManagement.get_company_list(), len(DataManagement.get_company_list()) * [0]))

class ThreadSafety:

    @staticmethod
    def add_company_to_lock(company_name):
        if company_name not in locks_companies.keys():

            locks_companies[company_name] = 0


    @staticmethod
    def force_lock_company():

        locks_companies[st.session_state.company] = 0

        if st.session_state.company != '':

            lock.acquire()

            if locks_companies[st.session_state.company] == 1: # company taken

                st.session_state.dont_display_data = True
                st.session_state.right_to_unlock = 0

            else: # company free

                st.session_state.dont_display_data = False
                st.session_state.right_to_unlock = 1

                locks_companies[st.session_state.company] = 1

            lock.release()


    @staticmethod
    def lock_company():

        if st.session_state.company != '':

            lock.acquire()

            if locks_companies[st.session_state.company] == 1: # company taken

                st.session_state.dont_display_data = True
                st.session_state.right_to_unlock = 0

            else: # company free

                st.session_state.dont_display_data = False
                st.session_state.right_to_unlock = 1

                locks_companies[st.session_state.company] = 1

            lock.release()

    @staticmethod
    def unlock_company():
        if st.session_state.right_to_unlock == 1:

            lock.acquire()

            locks_companies[st.session_state.company] = 0
            st.session_state.right_to_unlock = 0

            lock.release()

    @staticmethod
    def lock_warning_display():
        if 'dont_display_data' in st.session_state:
            if st.session_state.dont_display_data == True:

                st.warning('The company you selected is being used by another user at the moment or has not been closed correctly. For safety reasons you can see the data but you can not modify it.'
                           ' If you are sure that you are working in a safe environment and you want to modify the data anyways click on continue.')

                st.button('Continue anyways', on_click=ThreadSafety.force_lock_company())


