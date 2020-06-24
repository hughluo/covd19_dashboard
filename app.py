import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

dashboard_name = "COVID-19 Dashboard"
info = 'Germany'
csv_link = "https://covid19-lake.s3.us-east-2.amazonaws.com/enigma-aggregation/csv/global_countries/enigma_covid_19_global_countries.csv"
df_raw = pd.read_csv(csv_link)
timeline_info = "Timeline from https://www.nytimes.com/article/coronavirus-timeline.html"


def increase_rate(df_raw, country, metric):
    df = df_raw[df_raw['country_name'] == country][[
        'country_name', 'date', metric]].reset_index(drop=True)
    df['increase_rate'] = df.groupby('country_name')[[metric]].pct_change()
    df.fillna(0, inplace=True)
    df.replace([np.inf], 0, inplace=True)
    res = df
    return res


# avg_increase_rate_before_event(event_time) = avg(increase_rate(origin to event))
# avg_increase_rate_after_event(event_time) = avg(increase_rate(event to today))

def avg_increase_rate(df_with_increase_rate, event_date, after=True):
    df = df_with_increase_rate
    df_event = df[df['date'] > event_date]
    if not after:
        df_event = df[df['date'] <= event_date]
    res = df_event['increase_rate'].mean()
    return res


df_increase_rate = increase_rate(df_raw, 'Germany', 'cases')

avg_after_childrensday = avg_increase_rate(df_increase_rate, '2020-05-01')
avg_before_childrensday = avg_increase_rate(
    df_increase_rate, '2020-05-01', False)


def init(app):
    #  app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    country_dropdown = dcc.Dropdown(
        id='country',
        options=[{'label': country, 'value': country}
                 for country in df_raw['country_name'].unique()],
        value='Germany'
    )

    event_dropdown = dcc.Dropdown(
        id='event',
        options=[
            {'label': 'Obligation to notify', 'value': '2020-01-31'},
            {'label': 'Stop of entry', 'value': '2020-03-17'},
            {'label': 'Contact restrictions', 'value': '2020-03-22'},
            {'label': 'Quarantine obligation', 'value': '2020-04-10'},
            {'label': 'Masc obligation', 'value': '2020-04-22'},
            {'label': 'Strong relaxations of Corona event', 'value': '2020-05-06'},
        ],
        value='Obligation to notify',
    )

    app.layout = html.Div([
        html.H1(children=dashboard_name),
        html.H4(children=f'datasource: {csv_link}'),
        html.H6(children=info),
        html.H2(children="Select country"),
        country_dropdown,
        html.H2(children="Select measure"),
        event_dropdown,

        dcc.Graph(
            id='my-graph',
            config={'displayModeBar': False},
            animate=True,
            # figure=fig
        )])

    @app.callback(Output('my-graph', 'figure'), [Input('event', 'value')])
    def update_graph(event):
        fig = go.Figure()
        # Doc for go.Scatter: https://plotly.com/python/reference/#scatter
        # Examples: https://plotly.com/python/line-charts/
        fig.add_trace(go.Scatter(
            x=df_increase_rate['date'],
            y=df_increase_rate['increase_rate'], 
            mode='lines+markers',
            line=dict(color="black", width=2),
            connectgaps=True,
        ))

        return fig


if __name__ == '__main__':
    app = dash.Dash(dashboard_name, external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])
    init(app)
    app.run_server(host='0.0.0.0', port=8050, debug=True)
