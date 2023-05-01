from SessionState.Session_state_dataframes import Session_state_dataframes
import plotly.express as px
import numpy as np
class Visualizations:

    @staticmethod
    def stages_line_plot(page):

        # df with page data
        df = Session_state_dataframes.df_page_visualizations(page)

        fig = px.line(df, x='Code', y='Stage', color='Tab', color_discrete_sequence=px.colors.qualitative.Vivid[:len(np.unique(df['Tab']).tolist())],
                      markers=True, labels=dict(IDs='Question code'))

        fig.update_layout(xaxis=dict(ticklabelstep=100, tickfont=dict(size=1),showgrid= True, tickangle=-45))
        fig.update_layout(yaxis=dict(tickvals=[1, 2, 3, 4, 5], showgrid= True))
        fig.update_layout(yaxis_range=[0.5, 5.5])

        return fig

    @staticmethod
    def stages_barplot(page):

        #df with page data
        df = Session_state_dataframes.df_page_visualizations(page)

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