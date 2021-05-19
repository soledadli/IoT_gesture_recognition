import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

merge_dir = 'merge_data/'
scaled_dir = "merge_data/scaled_data/"
fileName = "test0"

app = dash.Dash(__name__)

df = pd.read_csv(merge_dir + fileName +".csv")
df["err_aX"] = df["aX"] - df["aX"].std() # difference to std

# dfs = pd.read_csv(scaled_dir + fileName +".csv")
#num = df["activity"].value_counts()




linechart = px.line(
    data_frame = df,
    x = 'time',
    y = ["aX","aY","aZ","gX","gY",],
    facet_col = 'activity', # Separate the line plots according to the activities
    error_y = 'err_aX',
    labels = {"value":"Data"},
    title = 'IMU Data Respective to Time',
    template='ggplot2', #Choices: 'seaborn', 'plotly' 'gridon'


    #hover_name ="aX" # values appear in bold in hover tooltip information
    # hover_data = df["activity"].value_counts() # values appear as extra data in the hover tooltip
)

linechart.show()


'''
app.layout = html.Div([

    html.Div([
        dcc.Graph(id="our_graph")
    ],className = " six columns"),

    html.Div([
        html.Br(),

        #html.Label(["Choose 3 motion data:"], style = {'font-weight':'bold', 'text-alight':'center'}),
        dcc.Dropdown(id='first_motion',
            options=[{'label':x, 'value':x} for x in df["activity"].unique()],
            value = 'slow',
            multi = False,
            disabled = False,
            clearable = True,
            searchable = True,
            placeholder = 'Choose motion',
            className = 'form-dropdown',
            style = {'width':'90%'},
            persistence = 'string',
            persistence_type = 'memory')

    ], className = 'one column'),

])

@app.callback(
    Output('our_graph','figure'),
    [Input('first_motion','value')]
)

def build_graph(motion_one):
#    dff = df[df["activity"]==motion_one]

    fig = px.line(df, y=['aX','aY','aZ',"gX","gY","gZ"], height = 600 )
    fig.update_layout(yaxis={'title':'Magnititude'},
                      title={'text':'IMU Data Respective to Time',
                   'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
'''