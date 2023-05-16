import streamlit as st
from Configuration_settings.ParseConfigFile import ParseConfigFile


pages = ParseConfigFile.get_pages_list()
pages_names = ParseConfigFile.get_pages_names_list()

stages = ParseConfigFile.get_stages_list()
max_stage = ParseConfigFile.get_max_stage()


#GLOBAL VARIABLES - define the model
model_descriptor = ParseConfigFile.get_numeric_model_descriptor()#excel_get_model_description()
model_full_descriptor = ParseConfigFile.get_numeric_model_full_descriptor()#excel_get_full_model_description()
model_ovw_descriptor = ParseConfigFile.get_model_ovw_descriptor()#excel_get_overview_description()


#methods to get copies of global variables
@st.cache_data
def return_model_descriptor_copy():
    #for NEW model
    #return excel_get_model_description_2()
    return model_descriptor.copy()

@st.cache_data
def return_model_full_descriptor_copy():
    #for NEW model
    #return excel_get_full_model_description_2()
    return model_full_descriptor.copy()

@st.cache_data
def return_model_ovw_descriptor_copy():
    return model_ovw_descriptor.copy()
