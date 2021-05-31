import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import os
import glob

list_of_files = glob.glob( 'predictions/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([


    html.Div(id='prediction'),
    dcc.Interval(
                        id='interval-component',
                        interval=5*1000,  # in milliseconds 5*60*
                        n_intervals=0
            )]

)

@app.callback(Output('prediction', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_predictions(n):
    m_df = pd.read_csv('predictions/2021-05-30-predictions.csv', index_col=[0])
    m_df = m_df.groupby(['hour', 'motion']).count().reset_index()

    bar_list = list()

    for motion in m_df['motion'].unique().tolist():
        bar = go.Bar(name=motion, x=m_df[m_df['motion'] == motion]['hour'].to_list(),
               y=m_df[m_df['motion'] == motion]['predictions'].to_list())

        bar_list.append(bar)

    fig = go.Figure(data=
        bar_list
    ,

        layout=go.Layout(
            title='Prediction Graph'
        )
    )


    return html.Div(dcc.Graph(
            id='Prediction_Graph',
            figure=fig
        ))

if __name__ == '__main__':
    app.run_server(debug=True)