import re
import pandas as pd

excel_file_directory = '15MNewVersion.xlsx'

pages = ['1', '2', '3', '4', '5']

def excel_get_question_codes_per_tab():
    # get the sheets list to iterate over them
    xls = pd.ExcelFile(excel_file_directory)
    tabs = xls.sheet_names[8:-4]

    question_codes_per_tab = {}

    for tab in tabs:
        df = pd.read_excel(excel_file_directory, sheet_name=tab, skiprows=9)

        # get the list from where to obtain the needed information
        quest = df[' quick check'].dropna().to_list()  #list the question column
        quest = [q for q in quest if q != ' ']
        quest = [q for q in quest if q != ' Questions']
        quest = [q for q in quest if q != ' quick check']
        quest = [q for q in quest if q != ' detail questions']

        #extract the number of questions for each subsection from the list
        number_questions_ce = (quest.index(' process excellence')) - 0
        ce = ['ce' + str(i + 1) for i in range(number_questions_ce)]

        number_questions_pe = (quest.index(' implementation') - quest.index(' process excellence')) - 1
        pe = ['pe' + str(i + 1) for i in range(number_questions_pe)]

        number_questions_i = (len(quest) - quest.index(' implementation')) - 1
        i = ['i' + str(i + 1) for i in range(number_questions_i)]

        question_codes_per_tab[tab] = ce + pe + i

    return question_codes_per_tab

def excel_get_model_description_2():

    #tabs per page
    xls = pd.ExcelFile(excel_file_directory)
    tabs = xls.sheet_names[8:-4]

    tabs_per_pages = {}
    for page in pages:
        tabs_current_page = [tab for tab in tabs if re.match(f'^{tab[1:2]}', page)]
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


def tab_questions_and_stages(tab):
    df = pd.read_excel(excel_file_directory, sheet_name=tab, skiprows=9)

    #----QUESTIONS-----
    quest = df[' quick check'].dropna().to_list()  # list the question column
    quest = [q for q in quest if q != ' ']
    quest = [q for q in quest if q != ' Questions']
    quest = [q for q in quest if q != ' quick check']
    quest = [q for q in quest if q != ' detail questions']
    # -------------------

    #------STAGES DESCRIPTIONS-------
    df_stages = df.fillna(0) #put 0s to deal with stages with no description

    stages = [' Stage 1 = 0%', ' Stage 2 = 25%', ' Stage 3 = 50%', ' Stage 4 = 75%', ' Stage 5 = 100%']
    descriptions = []

    for q in quest:
        question_stages = []

        for s in stages:
            descr = df_stages[s][df[' quick check'] == q] #for each stage get the description ...

            if isinstance(descr.tolist()[0], str):
                question_stages.append(descr.tolist()[0]) #... and if not empty put it in the list

            else:
                question_stages.append('none') #... otherwise append none string

        descriptions.append(question_stages) #append the list of the stages descriptions for the current question to the general list
    #---------------------------------

    quests_stages = dict(zip(quest, descriptions)) #create the dict by zipping since the order of stages is the same of the questions one
    return quests_stages

def excel_get_full_model_description_2():
    local_model_descriptor = excel_get_model_description_2()

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

# if __name__ == "__main__":
#     print(excel_get_full_model_description())

