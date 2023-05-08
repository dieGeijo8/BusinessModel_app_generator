import threading
import streamlit as st
from Firestore.FirestoreAPI import FirestoreAPI


#global variables - visible to all process
lock = threading.Lock()
#at the moment on new companies the check is not performed, cause they are added after the selection to the company list in the db
#so if 2 users add the same company in the same moment I don't have thread safety
#intializing this variable later cause problems
#NOW MAYBE THIS PROBLEM IS SOLVED, I RE INTITIALIZE THE VARIABLE AFTER INITIALIZING SESSION STATE
locks_companies = dict(zip(FirestoreAPI.get_company_list(), len(FirestoreAPI.get_company_list())*[0]))

class ThreadSafety:

    @staticmethod
    def reinitialize_lock_companies():
        locks_companies = dict(zip(st.session_state.company_list, len(st.session_state.company_list)*[0]))

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

                st.warning('The company you selected is being used by another user at the moment. For safety reasons you can see the data but you can not modify it. Try to reselect the company in a bit.')


