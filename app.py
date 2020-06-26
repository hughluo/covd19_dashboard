import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

dashboard_name = "COVID-19 Dashboard"
info = 'Made by Samir & Yinchi'
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


def avg_increase_rate(df_with_increase_rate, event_date, after=True):
    df = df_with_increase_rate
    df_event = df[df['date'] > event_date]
    if not after:
        df_event = df[df['date'] <= event_date]
    res = df_event['increase_rate'].mean()
    return res


def init(app):

    country_dropdown = dcc.Dropdown(
        id='country',
        options=[{'label': country, 'value': country}
                 for country in df_raw['country_name'].unique()],
        value='Germany'
    )
    
    metric_dropdown = dcc.Dropdown(
        id='metric',
        options=[
            {'label': 'Cases', 'value': 'cases'},
            {'label': 'Deaths', 'value': 'deaths'},
        ],
        value='cases'
    )

    event_dropdown = dcc.Dropdown(
        id='event',
        options=[
            {'label': 'Notification obligation', 'value': '2020-01-31'},
            {'label': 'Stop of entry', 'value': '2020-03-17'},
            {'label': 'Contact restrictions', 'value': '2020-03-22'},
            {'label': 'Quarantine obligation', 'value': '2020-04-10'},
            {'label': 'Mask obligation', 'value': '2020-04-22'},
            {'label': 'Strong relaxations', 'value': '2020-05-06'},
        ],
        value='2020-01-31',
    )

    app.layout = html.Div([
        html.H1(children=dashboard_name),
        html.H4(children=f'datasource: {csv_link}'),
        html.H6(children=info),
        html.H3(children="Select metric"),
        metric_dropdown,
        html.H3(children="Select event"),
        event_dropdown,

        # output
        html.H3(id='avg_before', style={'color': 'red'}),
        html.H3(id='avg_after', style={'color': 'blue'}),
        dcc.Graph(
            id='growth',
        )])

    @app.callback([Output('avg_before', 'children'), Output('avg_after', 'children'), Output('growth', 'figure')], [Input('metric', 'value'), Input('event', 'value')])
    def update_graph(metric, event):
        metric_name = metric.capitalize()
        df = increase_rate(df_raw, 'Germany', metric)

        avg_before_event = avg_increase_rate(df, event, False)
        avg_after_event = avg_increase_rate(df, event)

        avg_before_child = 'Average {} Growth Rate Before Event {:.4f}'.format(metric_name, avg_before_event)
        avg_after_child = 'Average {} Growth Rate After Event {:.4f}'.format(metric_name, avg_after_event)
        df_before_event = df[df['date'] <= event]
        df_after_event = df[df['date'] > event]


        scatter_before_event = go.Scatter(
            name = "Before Event",
            x=df_before_event['date'],
            y=df_before_event['increase_rate'], 
            mode='lines+markers',
            line=dict(color="red", width=2),
            showlegend = True,
            # connectgaps=True,
        )
        
        scatter_after_event = go.Scatter(
            name = "After Event",
            x=df_after_event['date'],
            y=df_after_event['increase_rate'], 
            mode='lines+markers',
            line=dict(color="blue", width=2),
            showlegend = True,
            # connectgaps=True,
        )

        fig = go.Figure()
        # Doc for go.Scatter: https://plotly.com/python/reference/#scatter
        # Examples: https://plotly.com/python/line-charts/
        fig.add_trace(scatter_before_event)
        fig.add_trace(scatter_after_event)
        fig.update_layout(legend=dict(y=0.5, font_size=16))
        fig.update_layout(title=f'{metric_name} Growth Rate in Germany',
                   xaxis_title='Date',
                   yaxis_title=f'{metric_name} Growth Rate')

        return avg_before_child, avg_after_child, fig


if __name__ == '__main__':
    app = dash.Dash(dashboard_name, external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])
    init(app)
    app.run_server(host='0.0.0.0', port=8050, debug=True)
