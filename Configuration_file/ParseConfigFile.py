import numpy as np
import math
import pandas as pd

class ParseConfigFile:

    # Configuration_settings/RiskModel_ConfigurationFile.xlsx
    config_file_sheet1 = pd.read_excel('Configuration_file/15M_ConfigurationFile.xlsx', sheet_name='ModelQuestions')
    config_file_sheet2 = pd.read_excel('Configuration_file/15M_ConfigurationFile.xlsx', sheet_name='ModelOverview')

    #clean data
    score_columns = config_file_sheet1.columns[list(config_file_sheet1.columns).index('Question')+1:]

    for col in score_columns:
        config_file_sheet1[col] = config_file_sheet1[col].fillna(' ')

    # pages and pages names
    @staticmethod
    def get_pages_list():

        number_of_pages = len(ParseConfigFile.config_file_sheet1['Page'].unique())

        page_list = [str(x+1) for x in range(number_of_pages)]

        return page_list

    @staticmethod
    def get_pages_names_list():

        pages_names = [x for x in ParseConfigFile.config_file_sheet1['Page'].unique()]

        return pages_names



    # model descriptor and model full descriptor

    # support methods to get the different partial parts of the model
    @staticmethod
    def get_tabs_by_page(page_name):

        df_page = ParseConfigFile.config_file_sheet1[ParseConfigFile.config_file_sheet1['Page'] == page_name]

        tabs = list(df_page['Tab'].unique())

        return tabs

    @staticmethod
    def get_questions_by_tab(page_name, tab_name):
        df_tab = ParseConfigFile.config_file_sheet1[(ParseConfigFile.config_file_sheet1['Page'] == page_name)
                                                    & (ParseConfigFile.config_file_sheet1['Tab'] == tab_name)]

        subsections = list(df_tab['Question'].unique())

        return subsections

    @staticmethod
    def get_stage_descriptions_by_question(page_name, tab_name, question):
        df_question = ParseConfigFile.config_file_sheet1[(ParseConfigFile.config_file_sheet1['Page'] == page_name)
                                                           & (ParseConfigFile.config_file_sheet1['Tab'] == tab_name)
                                                           & (ParseConfigFile.config_file_sheet1['Question'] == question)]

        stages = []

        for stage in df_question.columns[4:]:
            stages.append(df_question[stage].tolist()[0])

        return stages

    # this is used also in the page display for the subsections titles
    @staticmethod
    def get_subsections_by_tab(page_name, tab_name):

        df_tab = ParseConfigFile.config_file_sheet1[(ParseConfigFile.config_file_sheet1['Page'] == page_name)
                                                    & (ParseConfigFile.config_file_sheet1['Tab'] == tab_name)]

        subsections = list(df_tab['Subsection'].unique())

        return subsections

    @staticmethod
    def get_questions_by_subsection(page_name, tab_name, subsection_name):

        df_subsection = ParseConfigFile.config_file_sheet1[(ParseConfigFile.config_file_sheet1['Page'] == page_name)
                                                           & (ParseConfigFile.config_file_sheet1['Tab'] == tab_name)
                                                           & (ParseConfigFile.config_file_sheet1['Subsection'] == subsection_name)]

        questions = df_subsection['Question'].tolist()

        return questions

    @staticmethod
    def get_question_codes_by_tab(page_name, tab_name):

        subsections = ParseConfigFile.get_subsections_by_tab(page_name, tab_name)

        if isinstance(subsections[0], float) == True:

            question_codes = ['nc_' + str(x+1) for x in range(len(ParseConfigFile.get_questions_by_tab(page_name, tab_name)))]

            return question_codes
        else:

            question_codes = []

            for subsection in subsections:

                subsection_codes = [subsection.replace(' ', '') + '_' + str(x+1) for x in range(len(ParseConfigFile.get_questions_by_subsection(page_name, tab_name, subsection)))]

                question_codes += subsection_codes

            return question_codes

    # model descriptor - support for numeric model descriptor
    @staticmethod
    def get_model_descriptor():
        pages_names = ParseConfigFile.get_pages_names_list()

        model_descriptor = {}

        for page in pages_names:

            model_descriptor[page] = {}

            for tab in ParseConfigFile.get_tabs_by_page(page):

                question_codes = ParseConfigFile.get_question_codes_by_tab(page, tab)

                model_descriptor[page][tab] = question_codes

        return model_descriptor

    # numeric model descriptor
    @staticmethod
    def get_numeric_model_descriptor():
        model_descriptor = ParseConfigFile.get_model_descriptor().copy()
        final_model_descriptor = {}

        pages = ParseConfigFile.get_pages_list()
        pages_names = ParseConfigFile.get_pages_names_list()

        pages_dict = dict(zip(pages_names, pages))

        for page in model_descriptor.keys():

            final_model_descriptor[pages_dict[page]] = {}
            tab_index = 1
            for tab in model_descriptor[page].keys():

                final_model_descriptor[pages_dict[page]][pages_dict[page]+'.'+str(tab_index)] = model_descriptor[page][tab]
                tab_index += 1

        return final_model_descriptor


    # model full descriptor - support for numeric model full descriptor
    @staticmethod
    def get_model_full_descriptor():
        pages = ParseConfigFile.get_pages_names_list()
        model_descriptor = {}

        for page in pages:

            model_descriptor[page] = {}

            for tab in ParseConfigFile.get_tabs_by_page(page):

                model_descriptor[page][tab] = {}

                question_codes = ParseConfigFile.get_question_codes_by_tab(page, tab)
                questions = ParseConfigFile.get_questions_by_tab(page, tab)

                for question_code, question in zip(question_codes, questions):

                    model_descriptor[page][tab][question_code] = {question: ParseConfigFile.get_stage_descriptions_by_question(page, tab, question)}

        return model_descriptor

    @staticmethod
    def get_numeric_model_full_descriptor():
        model_descriptor = ParseConfigFile.get_model_full_descriptor().copy()
        final_model_descriptor = {}

        pages = ParseConfigFile.get_pages_list()
        pages_names = ParseConfigFile.get_pages_names_list()

        pages_dict = dict(zip(pages_names, pages))

        for page in model_descriptor.keys():

            final_model_descriptor[pages_dict[page]] = {}# model_descriptor[page]
            tab_index = 1
            for tab in model_descriptor[page].keys():

                final_model_descriptor[pages_dict[page]][pages_dict[page]+'.'+str(tab_index)] = model_descriptor[page][tab]
                tab_index += 1

        return final_model_descriptor



    # page and tabs dictionary - used in page display for displaying tab and subsections titles
    @staticmethod
    def get_page_dictionary():
        model_descriptor = ParseConfigFile.get_model_descriptor().copy()
        model_numeric_descriptor = ParseConfigFile.get_numeric_model_descriptor().copy()

        pages = []
        pages_numbers = []

        for page, page_number in zip(model_descriptor.keys(), model_numeric_descriptor.keys()):
            pages.append(page)
            pages_numbers.append(page_number)

        return dict(zip(pages_numbers, pages))

    @staticmethod
    def get_tab_dictionary():
        model_descriptor = ParseConfigFile.get_model_descriptor().copy()
        model_numeric_descriptor = ParseConfigFile.get_numeric_model_descriptor().copy()

        tabs = []
        tabs_numbers = []

        for page, page_number in zip(model_descriptor.keys(), model_numeric_descriptor.keys()):
            for tab, tab_number in zip(model_descriptor[page].keys(), model_numeric_descriptor[page_number].keys()):

                tabs.append(tab)
                tabs_numbers.append(tab_number)

        #print(dict(zip(tabs_numbers, tabs)))
        return dict(zip(tabs_numbers, tabs))




    # stages
    @staticmethod
    def get_stages_list():

        columns = list(ParseConfigFile.config_file_sheet1.columns)

        number_of_stages = len(columns[4:])

        stages_list = [str(x+1) for x in range(number_of_stages)]

        return stages_list

    @staticmethod
    def get_max_stage():

        columns = list(ParseConfigFile.config_file_sheet1.columns)

        number_of_stages = len(columns[4:])

        stages_list = [int(x + 1) for x in range(number_of_stages)]

        return max(stages_list)




    # ovw
    @staticmethod
    def get_model_ovw_descriptor():

        df = ParseConfigFile.config_file_sheet2.copy()

        df['Description'] = [' ' if math.isnan(x) else x for x in df['Description'].tolist()]

        tab_dictionary = ParseConfigFile.get_tab_dictionary()
        reversed_tab_dict = {name:number for number, name in tab_dictionary.items()}

        tabs_number_column = []
        tabs_names_column = []
        for name in reversed_tab_dict.keys():

            tabs_names_column.append(name)
            tabs_number_column.append((reversed_tab_dict[name]))

        if all(x == ' ' for x in df['Description'].tolist()):

            descriptions_column = df['Description'].tolist()[:len(tabs_names_column)]
        else:

            descriptions_column = list(np.unique(df['Description'].tolist()))


        ovw_df = pd.DataFrame.from_dict({'Tab number': tabs_number_column, 'Tab': tabs_names_column, 'Description': descriptions_column})
        return ovw_df



    # tab and page weights
    @staticmethod
    def get_tab_weights():

        df = ParseConfigFile.config_file_sheet2.copy()

        tab_weigths_list = df['Tab weight'].tolist()

        return tab_weigths_list

    @staticmethod
    def get_page_weights():

        df = ParseConfigFile.config_file_sheet2.copy()

        pages_names = df['Page'].unique()

        page_weights_list = []
        for page in pages_names:

            page_weights_list.append(df['Page weight'][df['Page'] == page].tolist()[0])

        pages = ParseConfigFile.get_pages_list()
        return dict(zip(pages, page_weights_list))




# if __name__ == "__main__":
