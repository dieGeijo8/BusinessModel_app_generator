import os
from Configuration_start.Set_start import Set_start

if __name__ == "__main__":

    try:

        if Set_start.config_file_checks() != 1:

            Set_start.create_pages_files()

            os.system('streamlit run Home.py')
        else:

            print('Incorrect configuration file.')

    except:

        print('There was an error in the execution.')