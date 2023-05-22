import pandas as pd
import streamlit as st
from streamlit_authenticator.authenticate import Authenticate
import yaml
from yaml import SafeLoader


class Users:

    @staticmethod
    def user_authentication():

        with open('UsersManagement/credentials.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        authenticator = Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )

        name, authentication_status, username = authenticator.login('Login', 'main')

        return authenticator, authentication_status, name, username

    @staticmethod
    def get_user_rights(username):

        df = pd.read_csv('UsersManagement/Users_registered.csv')
        rights = df['Rights'][(df['Username'] == username)].tolist()[0]

        return rights

    @staticmethod
    def get_user_company(username):

        df = pd.read_csv('UsersManagement/Users_registered.csv')
        company = df['Company'][(df['Username'] == username)].tolist()[0]

        return company