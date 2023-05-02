import streamlit as st
from SessionState.Session_state_dataframes import Session_state_dataframes
from PagesDisplay.Visualizations import Visualizations
from Configuration.Configuration import pages

class Overview:

    @staticmethod
    def display_overview():
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

                elif df_ovw.loc[j, 'Tab'][:1] != df_ovw.loc[j - 1, 'Tab'][:1] or j == len(df_ovw) - 1:

                    st.experimental_data_editor(df_ovw.iloc[start:j], key=str(j) + '_data_editor_ovw')
                    start = j

                    if pages_titles_index <= (len(pages) - 1):

                        st.header(pages[pages_titles_index])
                        pages_titles_index += 1

        with tabs[1]:

            bp = Visualizations.overview_barplot()

            st.plotly_chart(bp, theme="streamlit", use_container_width=True)

