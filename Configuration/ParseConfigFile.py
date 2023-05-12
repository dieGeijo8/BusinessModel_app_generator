import numpy as np
import math
import pandas as pd

class ParseConfigFile:

    config_file_sheet1 = pd.read_excel('RiskModel_ConfigurationFile.xlsx', sheet_name='ModelQuestions')

    @staticmethod
    def get_page_list():

        number_of_pages = len(ParseConfigFile.config_file_sheet1['Page'].unique())

        page_list = [str(x+1) for x in range(number_of_pages)]

        return page_list

    @staticmethod
    def get_pages_names_list():

        pages_names = [x for x in ParseConfigFile.config_file_sheet1['Page'].unique()]

        return pages_names

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

        if math.isnan(subsections[0]) == True:

            question_codes = [str(x+1) for x in range(len(ParseConfigFile.get_questions_by_tab(page_name, tab_name)))]

            return question_codes
        else:

            question_codes = []

            for subsection in subsections:

                subsection_codes = [subsection+str(x+1) for x in range(len(ParseConfigFile.get_questions_by_subsection(page_name, tab_name, subsection)))]

                question_codes.append(subsection_codes)

            return question_codes


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

    @staticmethod
    def get_model_full_descriptor():
        pages_names = ParseConfigFile.get_pages_names_list()

        model_descriptor = {}

        for page in pages_names:

            model_descriptor[page] = {}

            for tab in ParseConfigFile.get_tabs_by_page(page):

                question_codes = ParseConfigFile.get_question_codes_by_tab(page, tab)
                questions = ParseConfigFile.get_questions_by_tab(page, tab)

                for question_code, question in zip(question_codes, questions):

                    model_descriptor[page][tab] = {}
                    model_descriptor[page][tab][question_code] = {}
                    model_descriptor[page][tab][question_code][question] = ParseConfigFile.get_stage_descriptions_by_question(page, tab, question)

        return model_descriptor

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




if __name__ == "__main__":

    print(ParseConfigFile.get_model_full_descriptor())