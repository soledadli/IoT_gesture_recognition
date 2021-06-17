import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import os
import glob
import dash

#import navbar
#from predict_gesture import *


list_of_files = glob.glob( 'predictions/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
df = pd.read_csv(latest_file)
m_df = df.groupby(['hour_min', 'motion']).count().reset_index()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([

    html.H1(children='Movuino Gesture Prediction Dashboard',
            style={
                'textAlign': 'center',
            }
            ),

    html.Div([
    html.P('Data is collected locally and the dashboard is for users to better supervise the predictions',
               style={'color': 'blue', 'fontSize': 18, 'textAlign': 'center'}),
    html.P('Please turn on the watch before clicking "Start the Recording"',
               style={'color': 'blue', 'fontSize': 18, 'textAlign': 'center'})

    ], style={'marginBottom': 30, 'marginTop': 25}),

    dcc.RadioItems(
        id='my_radiochoice',
        options=[
            {'label': 'Start the Recording', 'value': 'recording_true'},
            {'label': 'Stop the Recording', 'value': 'recording_false'},
            {'label': 'Waiting', 'value': 'waiting'}
        ],
        value='waiting',
        labelStyle={'display': 'inline-block'},
        style={'display': 'inline-block'}
    ),

    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Real Time Plot',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Specific Motion Plot',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            )
        ]),
    html.Div(id='tabs-content-classes'),

    html.Div(id='prediction'),

    html.Div([html.P(),
              html.H5('Gestures'),

              dcc.Dropdown(id = 'gesture_name'
                        ,options=[
                             {'label': i, 'value': i} for i in m_df['motion'].unique()],
                        value = 'walk',
                        multi = False,
                        placeholder = 'Select Motions',
                        style={'textAlign': "Left", "display": "center", "width": "50%"}
                    )]),

    dcc.Interval(
                        id='interval-component',
                        interval=20*1000,  # in milliseconds 5*60*
                        n_intervals=0
            )
]

)

@app.callback(Output('prediction', 'children'),
              [Input('interval-component', 'n_intervals'),
              Input('my_radiochoice', 'value'),
              Input('gesture_name','value'),
              Input('tabs-with-classes', 'value')])

def update_predictions(intervals, radiochoice, gesture, tab):
    """
    model = tf.keras.models.load_model('models/lstm_model_2.h5')
    schedule.every(1).minute.do(lambda: predict_motion(model, test_dir, ["walk", "flap", "still"]))

    data_loading = False
    if radiochoice == 'recording_true':
        data_loading = True
        print('saved')

    while data_loading:
        try:
            print('True')
            organize_imu_data()
            schedule.run_pending()
            if radiochoice == 'waiting' or radiochoice == 'recording_false':
                print("stopped")
                break
        except:
            print('Interruption Error')
            break

    """
    list_of_files = glob.glob( 'predictions/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    file_date = latest_file.split("/")[1].split(".")[0].split("-predictions")[0]
    df = pd.read_csv(latest_file)
    m_df = df.groupby(['hour_min', 'motion']).count().reset_index()
    bar_list = list()
    gesture_list = []


    if tab == 'tab-1':
        for motion in m_df['motion'].unique().tolist():
            bar = go.Bar(name=motion, x=m_df[m_df['motion'] == motion]['hour_min'].to_list(),
                   y=m_df[m_df['motion'] == motion]['predictions'].to_list(),
                         texttemplate = "%{y}",
                         textposition = 'inside')

            bar_list.append(bar)

            fig = go.Figure(data=
                bar_list,
            layout=go.Layout(
                title={'text': '{} Real Time Predictions '.format(file_date),
                       'y':0.9, 'x':0.5, 'xanchor': 'center','yanchor': 'top'
                       }
            )
        )
        fig.update_layout(barmode='stack')
        return html.Div(dcc.Graph(
                id='Prediction_Graph',
                figure=fig
            ))
    elif tab == 'tab-2':
        for motion in m_df['motion'].unique().tolist():
            bar = go.Bar(name=motion, x=m_df[m_df['motion'] == gesture]['hour_min'].to_list(),
                   y=m_df[m_df['motion'] == motion]['predictions'].to_list(),
                         texttemplate = "%{y}",
                         textposition = 'inside')

            bar_list.append(bar)

            fig = go.Figure(data=
                bar_list,
            layout=go.Layout(
                title={'text': '{} Real Time Predictions '.format(file_date),
                       'y':0.9, 'x':0.5, 'xanchor': 'center','yanchor': 'top'
                       }
            )
        )
        fig.update_layout(barmode='stack')

        return html.Div([
            dcc.Graph(
                id='Prediction_Graph',
                figure=fig
            )]
        )

if __name__ == '__main__':
    app.run_server(debug=True)
