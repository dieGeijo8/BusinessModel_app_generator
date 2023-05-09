from DataManagement.Firestore.Firestore_API import Firestore_API

class DataManagement:

    #support method - object to connect with a collection of the db
    @staticmethod
    def get_company_collection():
        company_collection = Firestore_API.Firestore_get_company_collection()

        return company_collection

    #support method - used in the web app initialization to obtain the starting set of available companies
    @staticmethod
    def get_company_list():
        collections_names = Firestore_API.Firestore_get_company_list()

        return collections_names



    #'main' method
    #returns a dictionary with the following structure page(key) - tab(key) - question code(key) - {'Stage': value, 'Remarks': value}
    @staticmethod
    def get_company_data():
        company_data = Firestore_API.Firestore_get_company_data()

        return company_data

    #'main' method
    #it submits to the firestore db the company data contained in the session state variables
    @staticmethod
    def submit_company_data():

        Firestore_API.Firestore_submit_company_data()



    #get the plan values of the ovw
    @staticmethod
    def get_company_overview_plan():
        ovw_plan = Firestore_API.Firestore_get_company_overview_plan()

        return ovw_plan

    #submit the current value of the session state variable ovw
    @staticmethod
    def submit_company_overview():

        Firestore_API.Firestore_submit_company_overview()



    #function for submit button
    @staticmethod
    def submit_button():

        Firestore_API.Firestore_submit_button()


    #function for configuration info
    @staticmethod
    def set_company_configuration(company, config_dict):

        Firestore_API.Firestore_set_company_configuration(company, config_dict)

    @staticmethod
    def get_company_configuration():

        company_configuration = Firestore_API.Firestore_get_company_configuration()

        return company_configuration

