import pandas as pd
import re
import streamlit as st

excel_file_directory = 'Configuration/15M.xlsx' #this is now the 'configuration file'

#pages - here it is manually, it should be via input
pages = ['1', '2', '3', '4', '5']
pages_names = ['Procurement Framework Strategy', 'Category strategies', 'Supplier strategies',
               'Process strategies', 'Procurement performance management']

stages = ('1', '2', '3', '4', '5')
# ovw_as_percentage = True

#tab subsections titles - here it is manually, it should be via input
tab_subs_titles = ['Integrated assessment', 'Concept excellence', 'Process Excellence', 'Implementation']



#support method for get model description
def excel_get_question_codes_per_tab():
    # get the sheets list to iterate over them
    xls = pd.ExcelFile(excel_file_directory)
    tabs = xls.sheet_names[5:-1]

    question_codes_per_tab = {}

    for tab in tabs:
        df = pd.read_excel(excel_file_directory, sheet_name=tab, skiprows=8)

        #get the list from where to obtain the needed information
        quest = df['Questions'].dropna().to_list()  #list the question column
        quest = [q for q in quest if q != 'Fragen']
        quest = [q for q in quest if q != 'Questions']  #drop the value 'Question'

        #extract the number of questions for each subsection from the list
        number_questions_ia = quest.index('Concept Excellence') - 0
        ia = ['ia' + str(i + 1) for i in range(number_questions_ia)]

        number_questions_ce = (quest.index('Process Excellence') - quest.index('Concept Excellence')) - 1
        ce = ['ce' + str(i + 1) for i in range(number_questions_ce)]

        number_questions_pe = (quest.index('Implementation') - quest.index('Process Excellence')) - 1
        pe = ['pe' + str(i + 1) for i in range(number_questions_pe)]

        number_questions_i = (quest.index('Definition') - quest.index('Implementation')) - 1
        i = ['i' + str(i + 1) for i in range(number_questions_i)]

        question_codes_per_tab[tab] = ia + ce + pe + i

    return question_codes_per_tab

#returns a dictionary with the following structure: page(key) - tab(key) - list of question codes
def excel_get_model_description():

    #tabs per page
    xls = pd.ExcelFile(excel_file_directory)
    tabs = xls.sheet_names[5:-1]

    tabs_per_pages = {}
    for page in pages:
        tabs_current_page = [tab for tab in tabs if re.match(f'^{tab[:1]}', page)]
        tabs_per_pages[page] = tabs_current_page

    #question_codes per tab
    question_codes_per_tab = excel_get_question_codes_per_tab()

    #final model description dictionary
    model_description = {}
    for page in pages:
        current_page_dict = {} #dictionary of the current page

        for tab in tabs_per_pages[page]:
            current_page_dict[tab] = question_codes_per_tab[tab] #get the question codes per each tab

        model_description[page] = current_page_dict #add the current page dictionary to the final one

    return model_description



#support method for get full model description
def tab_questions_and_stages(tab):
    df = pd.read_excel(excel_file_directory, sheet_name=tab, skiprows=8)

    #----QUESTIONS-----
    quest = df['Questions'].dropna().to_list() #list the question column
    quest = [q for q in quest if q != 'Questions' and q != 'Concept Excellence' and q != 'Process Excellence'
             and q != 'Implementation' and q != 'Definition' and q != ''] #filter
    # -------------------

    #------STAGES DESCRIPTIONS-------
    df_stages = df.fillna(0) #put 0s to deal with stages with no description

    stages = ['Stage 1 = 0 %', 'Stage 2 = 25 %', 'Stage 3 = 50 %', 'Stage 4 = 75 %', 'Stage 5 = 100 %']
    descriptions = []

    for q in quest:
        question_stages = []

        for s in stages:
            descr = df_stages[s][df['Questions'] == q] #for each stage get the description ...

            if isinstance(descr.tolist()[0], str):
                question_stages.append(descr.tolist()[0]) #... and if not empty put it in the list

            else:
                question_stages.append('none') #... otherwise append none string

        descriptions.append(question_stages) #append the list of the stages descriptions for the current question to the general list
    #---------------------------------

    quests_stages = dict(zip(quest, descriptions)) #create the dict by zipping since the order of stages is the same of the questions one
    return quests_stages

#returns a dictionary with the following structure: page(key) - tab(key) - question code(key) - question text(key) - list of stages description
def excel_get_full_model_description():
    local_model_descriptor = excel_get_model_description()

    #get a full descriptor
    model_full_descriptor = {}
    for page in local_model_descriptor.keys():
        page_full_descriptor = {}

        for tab in local_model_descriptor[page].keys():
            tab_full_descriptor = {}
            questions_and_stages = tab_questions_and_stages(tab)

            for question_code, question in zip(local_model_descriptor[page][tab], questions_and_stages.keys()):

                tab_full_descriptor[question_code] = {question: questions_and_stages[question]}

            page_full_descriptor[tab] = tab_full_descriptor

        model_full_descriptor[page] = page_full_descriptor

    return model_full_descriptor
    #########################


#the new information that the app gets here is a description per each tab and a weight for each tab score
#it returns a df with the following columns: tab - description
def excel_get_overview_description():
    df = pd.read_excel(excel_file_directory, sheet_name='Overview', skiprows=3, usecols='A:D,L')
    df.columns = ['Tab', 'Code', 'Description', 'NCode', 'Weight']

    df = df.astype({'Tab': str})
    df = df.dropna(subset=['NCode'])

    df = df.drop(['Code', 'NCode', 'Weight'], axis=1)
    df = df.reset_index(drop=True)

    return df



#GLOBAL VARIABLES - define the model
model_descriptor = excel_get_model_description()
model_full_descriptor = excel_get_full_model_description()
model_ovw_descriptor = excel_get_overview_description()

#methods to get copies of global variables
@st.cache_data
def return_model_descriptor_copy():
    return model_descriptor.copy()

@st.cache_data
def return_model_full_descriptor_copy():
    return model_full_descriptor.copy()

@st.cache_data
def return_model_ovw_descriptor_copy():
    return model_ovw_descriptor.copy()