import streamlit as st
from Extensions.Standard_extensions.Checkbox import Checkbox

class Questions_settings:
    
    # support method to get the full code of a question
    @staticmethod
    def get_full_question_code(page, tab, question_code):
        return str(page) + '_' + str(tab) + '_' + str(question_code)



    # support method in Session_state_variables - for first setting
    @staticmethod
    def sessionstate_set_question_data_values(company_data, page, tab, question_code):

        st.session_state['rendering_stage' + Questions_settings.get_full_question_code(page, tab, question_code)] = \
            company_data[page][tab][question_code]['Stage']
        st.session_state['rendering_remarks' + Questions_settings.get_full_question_code(page, tab, question_code)] = \
            company_data[page][tab][question_code]['Remarks']

        #standard extensions
        Checkbox.set_checkbox(company_data, page, tab, question_code)

    # support method in Session_state_variables - for deleting
    @staticmethod
    def sessionstate_delete_question_data_values(page, tab, question_code):

        del st.session_state['rendering_stage' + Questions_settings.get_full_question_code(page, tab, question_code)]
        del st.session_state['rendering_remarks' + Questions_settings.get_full_question_code(page, tab, question_code)]

        # standard extensions
        Checkbox.del_checkbox(page, tab, question_code)



    #support method - to get the list of values names collected for each question
    @staticmethod
    def get_question_values_name():
        return_list = ['Stage', 'Remarks']

        #standard extensions
        Checkbox.append_checkbox_value_name(return_list)

        return return_list

    # support method in FirestoreAPI - for submitting
    @staticmethod
    def get_question_data_values(page, tab, question_code):

        return_dict =  {'Stage': st.session_state['rendering_stage' + Questions_settings.get_full_question_code(page, tab, question_code)],
            'Remarks': st.session_state['rendering_remarks' + Questions_settings.get_full_question_code(page, tab, question_code)]}

        #standard extensions
        Checkbox.add_checkbox_value(return_dict, page, tab, question_code)

        return return_dict

    # support method in Firestore API - decide the types of the values to collect for each question
    @staticmethod
    def get_first_question_data_values():

        return_dict = {'Stage': 1, 'Remarks': ''}

        #standard extensions
        Checkbox.first_checkbox_value(return_dict)

        return return_dict




    # save the new stage value in the reendering session state variable
    @staticmethod
    def stage_callback(page, tab, question_code):

        st.session_state['rendering_stage' + Questions_settings.get_full_question_code(page, tab, question_code)] = \
            int(st.session_state['stage' + Questions_settings.get_full_question_code(page, tab, question_code)])

    # save the new remarks value in the reendering session state variable
    @staticmethod
    def remarks_callback(page, tab, question_code):

        st.session_state['rendering_remarks' + Questions_settings.get_full_question_code(page, tab, question_code)] = \
            int(st.session_state['remarks' + Questions_settings.get_full_question_code(page, tab, question_code)])

    # method in Pages_display - display single question
    @staticmethod
    def display_question(local_model_full_descriptor, page, tab, question_code):

        question_text = list(local_model_full_descriptor[page][tab][question_code].keys())[0]

        #standard extension
        Checkbox.display_checkbox(page, tab, question_code)

        st.radio(question_text, ('1', '2', '3', '4', '5'),
                 disabled=Checkbox.checkbox_disable_othervalues(page, tab, question_code),
                 index=st.session_state['rendering_stage' + Questions_settings.get_full_question_code(page, tab, question_code)] - 1,
                 on_change=Questions_settings.stage_callback, args=(page, tab, question_code),
                 key='stage' + Questions_settings.get_full_question_code(page, tab, question_code))

        st.text_area('Remarks',
                     disabled=Checkbox.checkbox_disable_othervalues(page, tab, question_code),
                     value=st.session_state['rendering_remarks' + Questions_settings.get_full_question_code(page, tab, question_code)],
                     on_change=Questions_settings.remarks_callback, args=(page, tab, question_code),
                     key='remarks' + Questions_settings.get_full_question_code(page, tab, question_code))


