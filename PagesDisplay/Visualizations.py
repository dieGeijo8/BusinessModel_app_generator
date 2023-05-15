import plotly.express as px
import plotly.graph_objects as go
import re
from wordcloud import WordCloud, STOPWORDS
from Configuration.Configuration import pages, pages_names, return_model_descriptor_copy
from Configuration.ParseConfigFile import ParseConfigFile
from Questions_settings.Questions_settings import Questions_settings
from SessionState.Session_state_dataframes import Session_state_dataframes
from Extensions.Standard_extensions.Plan import Plan
from Extensions.Standard_extensions.Percentages import Percentages
import numpy as np


class Visualizations:

    @staticmethod
    def stages_line_plot(page):

        # df with page data
        df = Session_state_dataframes.get_df_page_visualizations(page)

        tab_dictionary = ParseConfigFile.get_tab_dictionary()
        df['Tab name'] = [tab_dictionary[x] for x in df['Tab'].tolist()]

        fig = px.line(df, x='Code', y='Stage', color='Tab', color_discrete_sequence=px.colors.qualitative.Vivid[:len(np.unique(df['Tab']).tolist())],
                      hover_data=['Tab', 'Tab name'],
                      markers=True, labels={'Code': 'Question', 'Stage': 'Value'})#dict(IDs='Question code'))

        fig.update_layout(xaxis=dict(ticklabelstep=100, tickfont=dict(size=1), showgrid= True, tickangle=-45))
        fig.update_layout(yaxis=dict(tickvals=[1, 2, 3, 4, 5], showgrid=True))
        fig.update_layout(yaxis_range=[0.5, 5.5])

        fig.update_traces(hovertemplate="Tab: %{customdata[0]}<br>Tab name: %{customdata[1]}<br>Quest.Code: %{x}<br><br><br>Value: %{y}<br>")

        return fig

    @staticmethod
    def stages_barplot(page):

        #df with page data
        df = Session_state_dataframes.get_df_page_visualizations(page)

        #grouped df
        sub_df = df[['Tab', 'Stage']]
        grouped_df = sub_df.groupby('Tab').mean().round(1)
        grouped_df.reset_index(inplace=True)

        #to ensure the right order after the df manipulation
        grouped_df['Tab'] = [int(x[2:]) for x in grouped_df['Tab'].tolist()]
        grouped_df = grouped_df.sort_values(by=['Tab'])
        grouped_df['Tab'] = grouped_df['Tab'].astype('category')

        tab_dictionary = ParseConfigFile.get_tab_dictionary()
        grouped_df['Tab name'] = [tab_dictionary[x] for x in df['Tab'].tolist()]

        #figure
        fig = px.bar(grouped_df, x='Tab', y='Stage', color='Tab',
                     color_discrete_sequence=px.colors.qualitative.Vivid[:len(np.unique(sub_df['Tab']).tolist())],
                     hover_data=['Tab name'],
                     labels={'Stage': 'Average value'})

        fig.update_traces(width=0.5, showlegend=False)
        fig.update_layout(xaxis=dict(tickvals=grouped_df['Tab'].tolist(),
                                     ticktext=[str(x) for x in grouped_df['Tab'].tolist()]))
        fig.update_layout(yaxis=dict(tickvals=[1, 2, 3, 4, 5]))
        fig.update_layout(bargap=0.5, yaxis_range=[0, 5.5])

        fig.update_traces(hovertemplate="Tab: %{x}<br>Tab name: %{customdata[0]}<br><br>Average value: %{y}<br>")

        return fig

    @staticmethod
    def remarks_wordcloud(page):
        local_model_descriptor = return_model_descriptor_copy()

        stopwords = set(STOPWORDS)
        text = ''

        for tab in local_model_descriptor[page].keys():
            for question_code in local_model_descriptor[page][tab]:

                question_data = Questions_settings.get_question_data_values(page, tab, question_code)

                text += question_data['Remarks']

            text += ' '


        if text.replace(' ', '') == '':

            return 'Not enough words.'
        else:

            wordcloud = WordCloud(width=600, height=400,
                                  background_color='white',
                                  stopwords=stopwords,
                                  min_font_size=10).generate(text)

            return wordcloud.to_array()



    @staticmethod
    def overview_barplot():
        # get the updated overview df
        df = Session_state_dataframes.get_ovw_df_aggregated_by_page_copy()

        #standard extension
        Percentages.percentages_for_visualizations_firstmethod(df)

        df['Page name'] = pages_names

        y_list = ['Current']

        #standard extension
        Plan.add_plan_to_column_list(y_list)

        fig = px.bar(df, x='Page', y=y_list, color_discrete_sequence=['#42A7B3', '#FFC000'], barmode='group',
                     hover_data=['Page name'],
                     labels={'value': 'Average value', 'variable': ''})

        fig.update_layout(yaxis_range=[-0.5, 5.5], bargap=0.5)

        #standard extension
        Percentages.percentages_for_visualizations_secondmethod(fig)


        annotation_y = Percentages.percentages_for_visualizations_thirdmethod()

        curr_avg = sum(df['Current'].tolist()) / len(df['Current'].tolist())
        fig.add_shape(type="line", line_color='black', line_width=2, opacity=0.5, line_dash="dot",
                      x0=0, x1=1, xref="paper", y0=curr_avg, y1=curr_avg, yref="y")
        fig.add_annotation(text='Avg. current value', x=df['Page'].tolist()[len(df['Page'].tolist()) - 1],
                           y=curr_avg+annotation_y, showarrow=False)

        fig.update_traces(hovertemplate="Page: %{x}<br>Page name: %{customdata[0]}<br><br>Average value: %{y}<br>")


        #standard extension
        Plan.ovw_barplot_plan_lines(fig, df, annotation_y)

        return fig


    @staticmethod
    def overview_radarchart(page_selected):
        df_ovw = Session_state_dataframes.get_ovw_df_copy()

        # standard extension
        Percentages.percentages_for_visualizations_firstmethod(df_ovw)

        # otherwise the radial axis is not recognized as categoric - 'bug'
        df_ovw['Page'] = [x[:1] for x in df_ovw['Tab number'].to_list()]
        subset_df_ovw = df_ovw.loc[df_ovw['Page'] == page_selected]

        tab_dictionary = ParseConfigFile.get_tab_dictionary()
        subset_df_ovw['Tab name'] = [tab_dictionary[x] for x in subset_df_ovw['Tab number'].tolist()]

        subset_df_ovw['Tab number'] = [str(x).replace('.', '_') for x in subset_df_ovw['Tab number']]


        fig = go.Figure()
        Plan.ovw_radarchart_plan(fig, subset_df_ovw)
        fig.add_trace(go.Scatterpolar(r=subset_df_ovw['Current'].tolist(), theta=subset_df_ovw['Tab number'].tolist(), name='Current',
                                      customdata=subset_df_ovw['Tab name'].tolist(),
                                      fill='toself',
                                      line_color='#42A7B3'))


        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5.1])), showlegend=True)
        fig.update_polars(angularaxis_linewidth=0.1)

        Percentages.percentages_for_visualizations_fourthmethod(fig)

        fig.update_traces(hovertemplate="Tab: %{theta}<br>Tab name: %{customdata}<br><br>Average value: %{r}<br>")

        return fig

