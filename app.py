import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from pandas_datareader import data as web
from datetime import datetime as dt

dashboard_name = "COVID-19 Dashboard"
info = 'made by Yinchi "Wexort" Luo'
csv_link = "https://covid19-lake.s3.us-east-2.amazonaws.com/enigma-aggregation/csv/global_countries/enigma_covid_19_global_countries.csv"
df_raw = pd.read_csv(csv_link)

def init(app):
    app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    metric_type_dropdown = dcc.Dropdown(
        id='metric_type',
        options=[
            {'label': 'Cases', 'value': 'cases'},
            {'label': 'Deaths', 'value': 'deaths'},
            # {'label': 'Tests', 'value': 'tests'},
        ],
        value='cases'
    )


    app.layout = html.Div([
        html.H1(children=dashboard_name),
        html.H4(children=f"datasource: {csv_link}"),
        html.H6(children=info),
        metric_type_dropdown,
        dcc.Graph(id='my-graph')
    ], style={'width': '500'})

    @app.callback(Output('my-graph', 'figure'), [Input('metric_type', 'value')])
    def update_graph(metric_type):
        selected_country = "Jordan"
        df_date_world = df_raw[df_raw['country_name'] == 'World'].set_index(['date'])
        df_out_world = df_date_world[metric_type].sort_index(axis = 0).to_frame()
        df_date_selected = df_raw[df_raw['country_name'] == selected_country].set_index(['date'])
        df_out_selected = df_date_selected[metric_type].sort_index(axis = 0).to_frame()
        return {
            'data': [
                {
                'x': df_out_world.index,
                'y': df_out_world[metric_type],
                'name': "World",
                'marker': { 'color': 'rgb(55, 83, 109)' },
                },
                {
                'x': df_out_selected.index,
                'y': df_out_selected[metric_type],
                'name': selected_country,
                'marker': { 'color': 'rgb(26, 118, 255)' },
                },
            ],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }


if __name__ == '__main__':
    app = dash.Dash(dashboard_name)
    init(app)
    app.run_server()