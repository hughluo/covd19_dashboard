import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from pandas_datareader import data as web
from datetime import datetime as dt

csv_link = "https://covid19-lake.s3.us-east-2.amazonaws.com/enigma-aggregation/csv/global_countries/enigma_covid_19_global_countries.csv"
df_raw = pd.read_csv(csv_link)

def init(app):
    app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    metric_type_dropdown = dcc.Dropdown(
        id='metric_type',
        options=[
            {'label': 'Cases', 'value': 'cases'},
            {'label': 'Deaths', 'value': 'deaths'},
            {'label': 'Tests', 'value': 'tests'},
        ],
        value='cases'
    )


    app.layout = html.Div([
        metric_type_dropdown,
        dcc.Graph(id='my-graph')
    ], style={'width': '500'})

    @app.callback(Output('my-graph', 'figure'), [Input('metric_type', 'value')])
    def update_graph(metric_type):
        df_date = df_raw[df_raw['country_name'] == 'Jordan'].set_index(['date'])
        df_out = df_date[metric_type].sort_index(axis = 0).to_frame()
        return {
            'data': [{
                'x': df_out.index,
                'y': df_out[metric_type]
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }


if __name__ == '__main__':
    app = dash.Dash('COVID-19 Dashboard')
    init(app)
    app.run_server()