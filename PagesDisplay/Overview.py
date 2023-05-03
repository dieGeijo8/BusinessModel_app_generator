import pandas as pd
import streamlit as st
from SessionState.Session_state_dataframes import Session_state_dataframes
from SessionState.Session_state_variables import Session_state_variables
from PagesDisplay.Visualizations import Visualizations
from Configuration.Configuration import pages

class Overview:

    @staticmethod
    def display_overview():

        #get an updated copy of the ovw df
        Session_state_variables.update_company_overview_session_state()
        df_ovw = Session_state_dataframes.get_ovw_df_copy()

        tabs = st.tabs(['Data', 'Dashboard'])

        with tabs[0]:
            #display the df
            start = 0
            pages_titles_index = 0

            for j in range(len(df_ovw)):

                if j == 0:
                    st.header(pages[pages_titles_index])
                    pages_titles_index += 1

                elif df_ovw.loc[j, 'Tab'][:1] != df_ovw.loc[j - 1, 'Tab'][:1]:

                    st.dataframe(df_ovw.iloc[start:j])

                    start = j

                    if pages_titles_index <= (len(pages) - 1):

                        st.header(pages[pages_titles_index])
                        pages_titles_index += 1

                elif j == len(df_ovw) - 1:

                    st.dataframe(df_ovw.iloc[start:j+1])

        with tabs[1]:

            bp = Visualizations.overview_barplot()

            st.plotly_chart(bp, theme="streamlit", use_container_width=True)

