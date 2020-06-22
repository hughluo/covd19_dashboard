import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

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
        ],
        value='cases'
    )

    country_dropdown = dcc.Dropdown(
        id='country',
        options=[{'label': country, 'value': country} for country in df_raw['country_name'].unique()],
        value='Germany'
    )

    measure_dropdown = dcc.Dropdown(
        id='measure',
        options=[{'label': 'Obligation to notify', 'value': '2020-01-31'},
                 {'label': 'Stop of entry', 'value': '2020-03-17'},
                 {'label': 'Contact restrictions', 'value': '2020-03-22'},
                 {'label': 'Quarantine obligation', 'value': '2020-04-10'},
                 {'label': 'Masc obligation', 'value': '2020-04-22'},
                 {'label': 'Strong relaxations of Corona measures', 'value': '2020-05-06'}, ],
        value='Obligation to notify',
    )

    app.layout = html.Div([
        html.H1(children=dashboard_name),
        html.H4(children=f"datasource: {csv_link}"),
        html.H6(children=info),
        html.H2(children="Select metric type"),
        metric_type_dropdown,
        html.H2(children="Select country"),
        country_dropdown,
        html.H2(children="Select measure"),
        measure_dropdown,
        dcc.Graph(id='my-graph')
    ], style={'width': '500'})

    @app.callback(Output('my-graph', 'figure'),
                  [Input('metric_type', 'value'), Input('country', 'value'), Input('measure', 'value')])
    def update_graph(metric_type, selected_country):
        # selected_country = "Jordan"
        df_date_world = df_raw[df_raw['country_name'] == 'World'].set_index(['date'])
        df_out_world = df_date_world[metric_type].sort_index(axis=0).to_frame()
        df_date_selected = df_raw[df_raw['country_name'] == selected_country].set_index(['date'])
        df_out_selected = df_date_selected[metric_type].sort_index(axis=0).to_frame()
        return {
            'data': [
                {
                    'x': df_out_world.index,
                    'y': df_out_world[metric_type],
                    'name': "World",
                    'marker': {'color': 'rgb(55, 83, 109)'},
                },
                {
                    'x': df_out_selected.index,
                    'y': df_out_selected[metric_type],
                    'name': selected_country,
                    'marker': {'color': 'rgb(26, 118, 255)'},
                },
            ],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }


if __name__ == '__main__':
    app = dash.Dash(dashboard_name)
    init(app)
    app.run_server(host='0.0.0.0', port=8050)
