import math
import openpyxl
import numpy as np
import pandas as pd

class Set_start():

    @staticmethod
    def create_pages_files(pages, pages_names):

        for i in range(len(pages)):
            file = open('pages/' + str(i + 1) + '_' + str(i + 1) + '-' + pages_names[i] + '.py', 'w')

            file.write('from PagesDisplay.Page_display import Page_display\n')
            file.write('from Configuration_file.Configuration import pages\n')
            file.write('\n')
            file.write('if __name__ == "__main__":\n')
            file.write(f'    Page_display.display_page(pages[{i}])')

        file = open('pages/' + str(len(pages) + 1) + '_Overview.py', 'w')
        file.write('from PagesDisplay.Overview import Overview\n')
        file.write('\n')
        file.write('if __name__ == "__main__":\n')
        file.write('    Overview.display_overview()')

    @staticmethod
    def config_file_checks():

        # sheets names check
        workbook = openpyxl.load_workbook('Configuration_file/RiskModel_ConfigurationFile.xlsx')
        sheets = workbook.sheetnames

        if sheets != ['ModelQuestions', 'ModelOverview']:
            return 1

        config_file_sheet1 = pd.read_excel('Configuration_file/RiskModel_ConfigurationFile.xlsx',
                                           sheet_name='ModelQuestions')
        config_file_sheet2 = pd.read_excel('Configuration_file/RiskModel_ConfigurationFile.xlsx',
                                           sheet_name='ModelOverview')

        # null page check
        for x in config_file_sheet1['Page'].tolist():
            if isinstance(x, float):
                    return 1

        for x in config_file_sheet2['Page'].tolist():
            if isinstance(x, float):
                    return 1

        # null tab check
        # if any(math.isnan(x) for x in config_file_sheet1['Tab']) or any(math.isnan(x) for x in config_file_sheet2['Tab']):
        #     return 1

        # null question check
        for x in config_file_sheet1['Tab'].tolist():
            if isinstance(x, float):
                if math.isnan(x):
                    return 1

        for x in config_file_sheet2['Tab'].tolist():
            if isinstance(x, float):
                if math.isnan(x):
                    return 1

        # page and tab persistency check
        # if (np.unique(config_file_sheet1['Page'].tolist()) != np.unique(config_file_sheet2['Page'].tolist())) \
        #         or (np.unique(config_file_sheet1['Tab'].tolist()) != np.unique(config_file_sheet2['Tab'].tolist())):
        #     return 1

        return 0

if __name__ == "__main__":

    config_file_sheet1 = pd.read_excel('Configuration_file/15M_ConfigurationFile.xlsx', sheet_name='ModelQuestions')

    number_of_pages = len(config_file_sheet1['Page'].unique())
    pages = [str(x + 1) for x in range(number_of_pages)]

    pages_names = [x for x in config_file_sheet1['Page'].unique()]

    Set_start.create_pages_files(pages, pages_names)