import json, webbrowser
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.figure_factory as ff
from format_data import *
from gantt import configure_df_for_plotting, create_gantt
from collapsible import dict_to_collapsible, test_dict

df = configure_df_for_plotting(obtain_dataframe())
fig = create_gantt(df)

# Create unscheduled_dict
request_dict = []
for row in df.itertuples():
    label = str(row.request_id) + ("" if row.scheduled else " (Not Scheduled)")
    request_dict.append( { 'label':label, 'id':row.request_id } )
request_dict.sort(key=lambda x: x['id'])
request_dict.insert(0, {'label': 'None', 'value':'None'} )

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
        style={'width':'25%', 'display':'inline-block'}),

    dcc.Graph(
        id='basic-interactions',figure=fig,config={'displayModeBar': False}),

    html.Div(className='row', children=[

        html.Div([
            dcc.Markdown(d("""
                **Requests**

                Select a request from the dropdown below (or click on one above).
            """)),
            dcc.Dropdown(
                id="unscheduled-dropdown",
                options=request_dict,
                value='None',
                clearable=False),
            ],
            style={'width':'25%', 'display':'inline-block'},
            className='column'
        ),

        html.Div(
            [
                dcc.Markdown(d("""
                    **Request Data**

                    Click on a request to see its details below.
                """)),
                html.Pre(id='click-data', style=styles['pre'])
            ],
            style={'width':'25%', 'display':'inline-block'},
            className='column'
        ),

        html.Div(
            dict_to_collapsible(test_dict),
            style={'width':'25%', 'display':'inline-block'},
            className='column'
        )

    ])
])

# Click on a Scheduled Observation
@app.callback(
    [Output('click-data', 'children'), Output('unscheduled-dropdown','value')],
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    if clickData == None:
        click_text = "No click data yet"
    else:
        try:
            curve_num = clickData['points'][0]['curveNumber']
            print curve_num
            config_data = df.loc[df['curve'] == curve_num]['configurations'].values[0]
            click_text = json.dumps(config_data,indent=2)
        except Exception as e:
            print e
            click_text = "clickData exists, but there was an error. See terminal"
    return click_text, "None"

# # Select Observation from Dropdown List
# @app.callback(
#     Output('click-data', 'children'),
#     [Input('unscheduled-dropdown', 'value')]
# )
# def display_click_data(request_id):
#     if request_id == 'None':
#         output_text = 'No request selected'
#     else:
#         try:
#             config_data = df.loc[df['request_id'] == request_id].values[0]
#             output_text = json.dumps(config_data,indent=1)
#         except Exception as e:
#             print e
#             output_text = "clickData does exist, but there was an error"
#     return output_text

# Select a different color code
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
