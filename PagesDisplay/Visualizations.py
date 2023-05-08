from Configuration.Configuration import pages, pages_names
from SessionState.Session_state_dataframes import Session_state_dataframes
import plotly.express as px
import plotly.graph_objects as go
from Extensions.Standard_extensions.Plan import Plan
import numpy as np


class Visualizations:

    @staticmethod
    def stages_line_plot(page):

        # df with page data
        df = Session_state_dataframes.get_df_page_visualizations(page)

        fig = px.line(df, x='Code', y='Stage', color='Tab', color_discrete_sequence=px.colors.qualitative.Vivid[:len(np.unique(df['Tab']).tolist())],
                      markers=True, labels=dict(IDs='Question code'))

        fig.update_layout(xaxis=dict(ticklabelstep=100, tickfont=dict(size=1), showgrid= True, tickangle=-45))
        fig.update_layout(yaxis=dict(tickvals=[1, 2, 3, 4, 5], showgrid=True))
        fig.update_layout(yaxis_range=[0.5, 5.5])

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

        #figure
        fig = px.bar(grouped_df, x='Tab', y='Stage', color='Tab',
                     color_discrete_sequence=px.colors.qualitative.Vivid[:len(np.unique(sub_df['Tab']).tolist())])

        fig.update_traces(width=0.5, showlegend=False)
        fig.update_layout(xaxis=dict(tickvals=grouped_df['Tab'].tolist(),
                                     ticktext=[str(x) for x in grouped_df['Tab'].tolist()]))
        fig.update_layout(yaxis=dict(tickvals=[1, 2, 3, 4, 5]))
        fig.update_layout(bargap=0.5, yaxis_range=[0, 5.5])

        return fig

    @staticmethod
    def overview_barplot():
        # get the updated overview df
        df = Session_state_dataframes.get_ovw_df_aggregated_by_page_copy()
        df['Page name'] = pages_names

        y_list = ['Current']

        #standard extension
        Plan.add_plan_to_column_list(y_list)

        fig = px.bar(df, x='Page', y=y_list, color_discrete_sequence=['#42A7B3', '#FFC000'], barmode='group',
                     hover_data=['Page name'])

        #fig.update_layout(yaxis_range=[-0.5,5.5], bargap=0.5)


        curr_avg = sum(df['Current'].tolist()) / len(df['Current'].tolist())
        fig.add_shape(type="line", line_color='black', line_width=2, opacity=0.5, line_dash="dot",
                      x0=0, x1=1, xref="paper", y0=curr_avg, y1=curr_avg, yref="y")
        fig.add_annotation(text='Avg. current stage', x=df['Page'].tolist()[len(df['Page'].tolist()) - 1],
                           y=curr_avg+0.1, showarrow=False)


        #standard extension
        Plan.ovw_barplot_plan_lines(fig, df)

        return fig


    @staticmethod
    def overview_radarchart(page_selected):
        df_ovw = Session_state_dataframes.get_ovw_df_copy()

        df_ovw['Page'] = [x[:1] for x in df_ovw['Tab'].to_list()]
        subset_df_ovw = df_ovw.loc[df_ovw['Page'] == page_selected]
        subset_df_ovw['Tab'] = [str(x).replace('.', '_') for x in subset_df_ovw['Tab']]


        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=subset_df_ovw['Current'].tolist(), theta=subset_df_ovw['Tab'].tolist(), name='Current',
                                      fill='toself',
                                      line_color='#42A7B3'))
        fig.add_trace(go.Scatterpolar(r=subset_df_ovw['Plan'].tolist(), theta=subset_df_ovw['Tab'].tolist(), name='Plan',
                                      fill='toself',
                                      line_color='#FFC000'))

        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5.1])), showlegend=True)
        fig.update_polars(angularaxis_linewidth=0.1)

        return fig

