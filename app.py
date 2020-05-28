import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from pandas_datareader import data as web
from datetime import datetime as dt

app = dash.Dash('COVID-19 Dashboard')

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Cases', 'value': 'cases'},
            {'label': 'Deaths', 'value': 'deaths'},
            {'label': 'Tests', 'value': 'tests'},
        ],
        value='cases'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    # df = web.DataReader(
    #     selected_dropdown_value,
    #     'google',
    #     dt(2017, 1, 1),
    #     dt.now()
    # )
    input_path = "./data.csv"

    df_raw = pd.read_csv(input_path)
    df_country = df_raw[df_raw['country_name'] != 'World'].set_index(['country_name'])
    df_out = df_country[selected_dropdown_value].groupby('country_name').sum().sort_values(ascending=False).head(10).to_frame()    
    return {
        'data': [{
            'x': df_out.index,
            'y': df_out[selected_dropdown_value]
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()