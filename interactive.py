import json, webbrowser
from textwrap import dedent as d
from collections import OrderedDict as odict

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

def create_display_dict(row):

    if row['scheduled']:
        scheduled_info = odict()
        scheduled_info['Start'] = row['start']
        scheduled_info['Finish'] = row['finish']
    else:
        scheduled_info = "No"

    display_dict = odict()
    display_dict['Request Name'] = row['request_name']
    display_dict['Type'] = row['request_type']
    display_dict['Scheduled'] = scheduled_info
    display_dict['Proposal'] = odict()
    display_dict['Proposal']['Name'] = row['proposal_name']
    display_dict['Proposal']['Priority'] = row['proposal_priority']
    display_dict['IPP'] = row['ipp']
    display_dict['Duration'] = str(row['duration']) + " seconds"
    display_dict['Total Priority (Proposal * IPP * Duration)'] = row['priority_total']
    display_dict['Details'] = odict()
    display_dict['Details']['Acceptability Threshold'] = row['acceptability_threshold']
    display_dict['Details']['Observation Windows'] = row['windows']
    display_dict['Details']['Configurations'] = row['configurations']

    return display_dict

# Create unscheduled_dict
request_dict = []
for row in df.itertuples():
    label = str(row.request_id) + ("" if row.scheduled else " (Not Scheduled)")
    request_dict.append( { 'label':label, 'value':row.request_id } )
request_dict.sort(key=lambda x: x['value'])
request_dict.insert(0, {'label': 'None', 'value':'None'} )

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
                id="colorcode-dropdown",
                options=[{'label':l,'value':v} for l,v in color_options.iteritems()],
                value='id',
                clearable=False),
        ],
        style={'width':'25%', 'display':'inline-block'}),

    dcc.Graph(
        id='gantt-chart',figure=fig,config={'displayModeBar': False}),

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
            id='collapsible-info',
            children=dict_to_collapsible(test_dict),
            style={'width':'25%', 'display':'inline-block'},
            className='column'
        )

    ])
])

##### Callback Functions #######################################################

# Click on a Scheduled Observation
@app.callback(
    Output('unscheduled-dropdown','value'),
    [Input('gantt-chart', 'clickData')]
)
def display_click_data(clickData):
    if clickData == None:
        click_id = 'None'
    else:
        try:
            curve_num = clickData['points'][0]['curveNumber']
            click_id = df.loc[df['curve'] == curve_num]['request_id'].values[0]
        except Exception as e:
            print "CLICKING ERROR: Something went wrong"
            print e
            click_id = 'None'
    return click_id

# Select Observation from Dropdown List
@app.callback(
    Output('collapsible-info', 'children'),
    [Input('unscheduled-dropdown', 'value')]
)
def display_click_data(request_id):
    if request_id == 'None':
        output_dict = 'No request selected'
    else:
        try:
            selected_row = df.loc[df['request_id'] == request_id].reset_index(\
                drop=True).to_dict('index')[0]
            output_dict = create_display_dict(selected_row)
        except Exception as e:
            print e
            output_dict = "clickData does exist, but there was an error"
    return dict_to_collapsible(output_dict)

# Select a different color code
@app.callback(
    Output(component_id='gantt-chart',component_property='figure'),
    [Input(component_id='colorcode-dropdown', component_property='value')]
)
def recolor_graph(color_code):
    global df
    fig = create_gantt(df,color_code)
    return fig

################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)
