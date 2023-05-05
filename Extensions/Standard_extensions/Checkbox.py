import streamlit as st

class Checkbox:

    name = 'Checkbox'
    activate_checkbox = True # this is what controls if activate the checkbox or not

    #decorator to check if activate the checkbox or not
    @staticmethod
    def checkbox_decorator(func):
        def wrapper(*args, **kwargs):
            if Checkbox.activate_checkbox == False:

                a = 0 #just to do something

            else:

                func(*args, **kwargs)

        return wrapper

    #support method
    @staticmethod
    def get_full_question_code(page, tab, question_code):
        return str(page) + '_' + str(tab) + '_' + str(question_code)



    #for first setting
    @checkbox_decorator
    @staticmethod
    def set_checkbox(company_data, page, tab, question_code):
        st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)] = \
            company_data[page][tab][question_code][Checkbox.name]

    #for deleting
    @checkbox_decorator
    @staticmethod
    def del_checkbox(page, tab, question_code):
        del st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]




    #append checkbox to the names of the values collected per each question
    @checkbox_decorator
    @staticmethod
    def append_checkbox_value_name(values_names_list):
        values_names_list.append(Checkbox.name)


    #add the checkbox value to the values collected per each question
    @checkbox_decorator
    @staticmethod
    def add_checkbox_value(question_data_values_dict, page, tab, question_code):
        question_data_values_dict[Checkbox.name] = \
            st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]

    #aad the checkbox value to the first values registered per each question
    @checkbox_decorator
    @staticmethod
    def first_checkbox_value(first_question_data_values_dict):
        first_question_data_values_dict[Checkbox.name] = False




    #display checkbox per each question + callback
    @checkbox_decorator
    @staticmethod
    def checkbox_callback(page, tab, question_code):
        st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)] = \
            st.session_state['checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]

    @checkbox_decorator
    @staticmethod
    def display_checkbox(page, tab, question_code):
        st.checkbox('Question not relevant to my assessment, dont\'t consider it',
                                    value=st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab,question_code)],
                                    on_change=Checkbox.checkbox_callback, args=(page, tab, question_code),
                                    key='checkbox' + Checkbox.get_full_question_code(page, tab, question_code)
                                    )

    @staticmethod
    def checkbox_disable_othervalues(page, tab, question_code):
        if Checkbox.activate_checkbox == True:

            return st.session_state['rendering_checkbox' + Checkbox.get_full_question_code(page, tab, question_code)]
        else:
            return False