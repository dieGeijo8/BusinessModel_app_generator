import streamlit as st
from Extensions.Standard_extensions.Plan import Plan


class Percentages:

    activate_percentages = True

    @staticmethod
    def percentages_decorator(func):
        def wrapper(*args, **kwargs):
            if Percentages.activate_percentages == False:

                a = 0  # just to do something

            else:

                func(*args, **kwargs)

        return wrapper


    #conversion from number from 1 to 5 to percentage
    @staticmethod
    def __conversion_function(x):

        new_x = 0 + (100 - 0) * (x - 1) / (5 - 1)

        return round(new_x, 2)


    #conversion of current and Plan column for display
    @percentages_decorator
    @staticmethod
    def ovw_as_percentage(df_ovw):

        df_ovw['Current'] = [str(Percentages.__conversion_function(x)) + '%' for x in df_ovw['Current'].to_list()]

        Plan.plan_ovw_as_percentage(df_ovw)


    @staticmethod
    def page_overall_as_percentage(scores_overall_dict, key):

        if Percentages.activate_percentages == True:

            value = str(Percentages.__conversion_function(scores_overall_dict[key])) + '%'
        else:

            value = str(scores_overall_dict[key])

        return value

    @staticmethod
    def print_overall(scores_per_page_dict, page, key, metrics_titles, metric_title):
        if Percentages.activate_percentages == True:

            if metric_title == 'Weight':
                value = str(round(100 * scores_per_page_dict[page][key], 2))

            else:
                value = str(Percentages.__conversion_function(scores_per_page_dict[page][key]))

            st.metric(label=metrics_titles[metric_title], value=value + '%')
        else:

            st.metric(label=metrics_titles[metric_title], value=str(scores_per_page_dict[page][key]))