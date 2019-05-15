import json, webbrowser
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.figure_factory as ff
from format_data import *
from gantt import configure_df_for_plotting, create_gantt

df = configure_df_for_plotting(obtain_dataframe())
fig = create_gantt(df)

# Create unscheduled_dict
unscheduled_requests = list(df.loc[df['scheduled'] == False]['request_id'])
unscheduled_dict = [{'label':id,'value':id} for id in unscheduled_requests]
unscheduled_dict.insert(0, {'label': 'None', 'value':'None'} )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

color_options = {
    'ID': 'id',
    'Proposal Priority': 'proposal'
    }

app.layout = html.Div([
    html.H2("SOAR Scheduler Analysis"),

    # Could maybe add some general information here?

    html.Div([
            dcc.Dropdown(
                id="color_code",
                options=[{'label':l,'value':v} for l,v in color_options.iteritems()],
                value='id',
                clearable=False),
        ],
        style={'width': '25%',
                'display': 'inline-block'}),

    dcc.Graph(
        id='basic-interactions',figure=fig,config={'displayModeBar': False}),

    html.Div(className='row', children=[


        html.Div([
            dcc.Markdown(d("""
                **Unscheduled Requests**

                Select an unscheduled requests from the dropdown below.
            """)),
            dcc.Dropdown(
                id="unscheduled-dropdown",
                options=unscheduled_dict,
                value='None',
                clearable=False),
            ],
            style={'width': '25%',
                    'display': 'inline-block'}),

        html.Div([
            dcc.Markdown(d("""
                **Request Data**

                Click on a request to see its details below.
            """)),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns')

    ])
])

@app.callback(
    [Output('click-data', 'children'),Output('unscheduled-dropdown','value')],
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    if clickData == None:
        return "No click data yet"
    else:
        try:
            curve_num = clickData['points'][0]['curveNumber']
            print curve_num
            config_data = df.loc[df['curve'] == curve_num]['configurations'].values[0]
            return json.dumps(config_data,indent=2), 'None'
            return "works to here though"
            assert False
            instrument_configs = config_data['instrument_configs']
            return "works to here"
            instrument_text = json.dumps(instrument_configs,indent=2)
            return instrument_text
        except Exception as e:
            print e
            return "clickData exists, but there was an error. See terminal"

    # return clickData["points"][0]['curveNumber"']
    # return str(df['id'].loc(clickData['points'][0]['curveNumber']))
    return json.dumps(clickData['points'][0]["curveNumber"], indent=2)

@app.callback(
    Output(component_id='basic-interactions',component_property='figure'),
    [Input(component_id='color_code', component_property='value')]
)
def recolor_graph(color_code):
    global df
    fig = create_gantt(df,color_code)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
