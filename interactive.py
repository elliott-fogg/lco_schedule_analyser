import json, webbrowser
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.figure_factory as ff
from format_data import *
from gantt import create_gantt

df = obtain_dataframe()
df, fig = create_gantt(df)

# fig = ff.create_gantt(df, title='Daily Schedule',showgrid_x=True,
#     showgrid_y=True, group_tasks=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

colour_options = {'ID': 'id'}

app.layout = html.Div([
    html.H2("SOAR Scheduler Analysis"),

    # Could maybe add some general information here?

    html.Div(
        [
            dcc.Dropdown(
                id="Colour_Code",
                options=[{'label':l,'value':v} for l,v in colour_options.items()],
                value={'label':"ID",'value':'id'},
                clearable=False),
        ],
        style={'width': '25%',
                'display': 'inline-block'}),

    dcc.Graph(
        id='basic-interactions',figure=fig,config={'displayModeBar': False}),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown(d("""
                **Click Data**

                Click on points in the graph.
            """)),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns')
    ])
])


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    if clickData == None:
        return "No click data yet"
    else:
        try:
            curve_num = clickData['points'][0]['curveNumber']
            return df['id'].loc[curve_num]
        except Exception as e:
            print e
            return "clickData exists, but there was an error"
    # return clickData["points"][0]['curveNumber"']
    # return str(df['id'].loc(clickData['points'][0]['curveNumber']))
    return json.dumps(clickData['points'][0]["curveNumber"], indent=2)


if __name__ == '__main__':
    app.run_server()
