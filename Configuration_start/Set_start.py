import math
import openpyxl
import numpy as np
import pandas as pd

class Set_start():

    config_file = 'Configuration_file/RiskModel_ConfigurationFile.xlsx' #'Configuration_file/15M_ConfigurationFile.xlsx'

    @staticmethod
    def config_file_checks():

        # sheets names check
        workbook = openpyxl.load_workbook(Set_start.config_file)
        sheets = workbook.sheetnames

        if sheets != ['ModelQuestions', 'ModelOverview']:
            return 1

        config_file_sheet1 = pd.read_excel(Set_start.config_file,
                                           sheet_name='ModelQuestions')
        config_file_sheet2 = pd.read_excel(Set_start.config_file,
                                           sheet_name='ModelOverview')

        # columns names check
        if any(i != j for i, j in zip(config_file_sheet1.columns[:4], ['Page', 'Tab', 'Subsection', 'Question'])):
            return 1

        if any(i != j for i, j in zip(config_file_sheet2.columns, ['Page', 'Tab', 'Description', 'Tab weight', 'Page weight'])):
            return 1

        # null page check
        for x, y in zip(config_file_sheet1['Page'].tolist(), config_file_sheet2['Page'].tolist()):

            if isinstance(x, float):
                if math.isnan(x):
                    return 1

            if isinstance(y, float):
                if math.isnan(y):
                    return 1

        # null tab check
        for x, y in zip(config_file_sheet1['Tab'].tolist(), config_file_sheet2['Tab'].tolist()):

            if isinstance(x, float):
                if math.isnan(x):
                    return 1

            if isinstance(y, float):
                if math.isnan(y):
                    return 1

        # null question check
        for x in config_file_sheet1['Question'].tolist():

            if isinstance(x, float):
                if math.isnan(x):
                    return 1

        # persistency between the 2 sheets checks
        if any(i not in np.unique(config_file_sheet2['Page'].tolist()) or j not in np.unique(config_file_sheet1['Page'].tolist())
               for i, j in
               zip(np.unique(config_file_sheet1['Page'].tolist()), np.unique(config_file_sheet2['Page'].tolist()))):

            print('Page persistency problem.')
            return 1

        if any(i not in np.unique(config_file_sheet2['Tab'].tolist()) or j not in np.unique(config_file_sheet1['Tab'].tolist())
               for i, j in
               zip(np.unique(config_file_sheet1['Tab'].tolist()), np.unique(config_file_sheet2['Tab'].tolist()))):

            print('Tab persistency problem.')
            return 1

        return 0

    @staticmethod
    def create_pages_files():

        # get the pages
        config_file_sheet1 = pd.read_excel(Set_start.config_file,
                                           sheet_name='ModelQuestions')

        number_of_pages = len(config_file_sheet1['Page'].unique())
        pages = [str(x + 1) for x in range(number_of_pages)]

        pages_names = [x for x in config_file_sheet1['Page'].unique()]


        # create the pages
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


