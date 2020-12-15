import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import plotly.io as pio

pio.templates.default = "ggplot2"

df = pd.read_csv(".//Data//csv//2020_National_ENG.csv",index_col=0)
coor = pd.read_csv(".//Data//Coordinate.csv")

names = coor[["Region","Name"]]

options = []
for subject in df.columns:
    option = {}
    option["label"] = subject
    option["value"] = subject
    options.append(option)


options_name = [{"label": "All", "value" : 0}]
for index,name in names.iterrows():
    option_name ={}

    option_name["label"] = name["Name"]
    option_name["value"] = name["Region"]
    options_name.append(option_name)


df = pd.merge(df,names,on = "Region")



app = dash.Dash(__name__)
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_subject",
                 options=options,
                 multi=False,
                 value="Math",
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="select_Region",
                 options=options_name,
                 multi=False,
                 value=0,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='select_subject', component_property='value'),
    Input(component_id='select_Region', component_property='value')]
)
def update_graph(select_subject,select_Region):

    container = "The subject chosen by user was: {}".format(select_subject)
    data = df.copy()
    if(select_Region != 0):
        data = data[data["Region"] == select_Region]

    fig = px.histogram(data, x=select_subject)


    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
