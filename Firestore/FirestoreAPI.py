import google.cloud.firestore
import streamlit as st
from Configuration.Configuration import return_model_descriptor_copy
from Questions_settings.Questions_settings import Questions_settings

class FirestoreAPI:

    #support method - object to connect with a collection of the db
    @staticmethod
    def get_company_collection():
        db = google.cloud.firestore.Client.from_service_account_json("Firestore/firestore_key.json")

        company_collection = db.collection(st.session_state.company)
        return company_collection

    #support method - used in the web app initialization to obtain the starting set of available companies
    @staticmethod
    def get_company_list():
        collections_names = ['']
        db = google.cloud.firestore.Client.from_service_account_json("Firestore/firestore_key.json")

        for collection in db.collections():

            collections_names.append(collection.id)

        return collections_names

    #'main' method
    #returns a dictionary with the following structure page(key) - tab(key) - question code(key) - {'Stage': value, 'Remarks': value}
    @staticmethod
    def get_company_data():
        company_collection = FirestoreAPI.get_company_collection()

        if len(company_collection.get()) > 0:

            local_model_descriptor = return_model_descriptor_copy()
            company_data = {}

            for page in local_model_descriptor.keys():

                company_document = company_collection.document(page)
                company_data[page] = company_document.get().to_dict()

            return company_data

        else:

            local_model_descriptor = return_model_descriptor_copy()
            company_data = {}

            #set the values to collect for each question
            for page in local_model_descriptor.keys():

                page_data = {}
                for tab in local_model_descriptor[page].keys():

                    tab_data = {}
                    for question_code in local_model_descriptor[page][tab]:

                        tab_data[question_code] = Questions_settings.get_first_question_data_values()

                    page_data[tab] = tab_data

                company_data[page] = page_data

            #set the data in the firestore db
            for page in local_model_descriptor.keys():
                company_document = company_collection.document(page)

                company_document.set(company_data[page])

            return company_data

    #'main' method
    #it submits to the firestore db the company data contained in the session state variables
    @staticmethod
    def submit_company_data():
        company_collection = FirestoreAPI.get_company_collection()

        local_model_descriptor = return_model_descriptor_copy()
        company_data = {}

        # set the values to collect for each question
        for page in local_model_descriptor.keys():

            page_data = {}
            for tab in local_model_descriptor[page].keys():

                tab_data = {}
                for question_code in local_model_descriptor[page][tab]:

                    tab_data[question_code] = Questions_settings.get_question_data_values(page, tab, question_code)

                page_data[tab] = tab_data

            company_data[page] = page_data

        # set the data in the firestore db
        for page in local_model_descriptor.keys():
            company_document = company_collection.document(page)

            company_document.set(company_data[page])



    #get the plan values of the ovw
    @staticmethod
    def get_company_overview_plan():
        company_collection = FirestoreAPI.get_company_collection()

        company_ovw_document = company_collection.document('overview')

        local_model_descriptor = return_model_descriptor_copy()

        try:
            ovw_plan_values = company_ovw_document.get().to_dict()

            return ovw_plan_values['Plan']

        except:
            tabs = []

            for page in local_model_descriptor.keys():
                for tab in local_model_descriptor[page].keys():
                    tabs.append(tab)

            return dict(zip(tabs, [0]*len(tabs)))

    #submit the current value of the session state variable ovw
    @staticmethod
    def submit_company_overview():
        company_collection = FirestoreAPI.get_company_collection()

        company_ovw_document = company_collection.document('overview')
        company_ovw_document.set(st.session_state['overview'])



    #function for submit button
    @staticmethod
    def submit_button():
        FirestoreAPI.submit_company_data()

        FirestoreAPI.submit_company_overview()