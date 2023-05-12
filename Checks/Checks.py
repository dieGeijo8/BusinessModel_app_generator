import streamlit as st

class Checks:

    @staticmethod
    def check_if_company_valid(company_name):

        if company_name in st.session_state.company_list or company_name == '':

            return False
        else:

            return True