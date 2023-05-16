import os
from Configuration_settings.Set_start import Set_start

if Set_start.config_file_checks() == 1:

    print('Incorrect configuration file')

else:

    os.system('python Configuration_settings/Set_start.py')

    os.system('streamlit run Home.py')