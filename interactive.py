import json, webbrowser
from textwrap import dedent as d
from collections import OrderedDict as odict
import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.figure_factory as ff
from format_data import obtain_dataframe
from gantt import single_telescope_configure_df, single_telescope_plot_gantt
from collapsible import dict_to_collapsible, test_dict
# from contention_pressure import contention

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def single_telescope(input_file, output_file):
    orig_df = obtain_dataframe(input_file, output_file)
    df = single_telescope_configure_df(orig_df)
    fig = single_telescope_plot_gantt(df)

    # Create the drop down menu for selecting requests
    request_dict = []
    for row in df.itertuples():
        label = str(row.request_id) + ("" if row.scheduled else " (Not Scheduled)")
        request_dict.append( { 'label':label, 'value':row.request_id } )
    request_dict.sort(key=lambda x: x['value'])
    request_dict.insert(0, {'label': 'None', 'value':'None'} )

    # Set up the app
    app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

    styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        }
    }

    color_options = {
        'ID': 'id',
        'Proposal Priority': 'proposal',
        'IPP': 'ipp'
        }

    app.layout = html.Div([
        html.H2("SOAR Scheduler Analysis"),

        # Could maybe add some general information here?

        html.Div([
                dcc.Dropdown(
                    id="colorcode-dropdown",
                    options=[{'label':l,'value':v} for l,v in color_options.iteritems()],
                    value='id_default',
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
                    id="request-dropdown",
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

    #### Callback Functions ################################################

    # Click on a Scheduled Observation
    @app.callback(
        Output('request-dropdown','value'),
        [Input('gantt-chart', 'clickData')]
    )
    def display_request_data_from_click(clickData):
        if clickData == None:
            return 'None'

        # try:
        point_clicked = clickData['points'][0]
        if "pointIndex" in point_clicked:
            # Have clicked on an edge point, not a central point
            point_dt = dt.datetime.strptime(point_clicked['x'], "%Y-%m-%d %H:%M:%S")
            gantt_line = point_clicked['y']
            nominal_date = fig['layout']['yaxis']['ticktext'][gantt_line]
            matching_rows = df.loc[(df['Task'] == nominal_date) & \
                ((df['start_dt']==point_dt) | (df['end_dt']==point_dt))]

            # XXX: PROBLEM HERE
            print(nominal_date)
            print(df['Task'].unique())
            # Work out why a row in the DF isn't being found that matches the provided data.

            click_ids_multiple = matching_rows['request_id'].values
            if len(click_ids_multiple) > 1:
                print("ERROR: Multiple rows matched")
                print(matching_rows)
            else:
                click_id = click_ids_multiple[0]

        else:
            # Have clicked on a central point, with a valid curveNumber
            curve_num = point_clicked['curveNumber']
            click_id = df.loc[df['curve'] == curve_num]['request_id'].values[0]

        return click_id

        # except Exception as e:
        #     print("MAJOR ERROR: Something went wrong when clicking.")
        #     print e
        #     return 'None'

    # Select Observation from Dropdown List
    @app.callback(
        Output('collapsible-info', 'children'),
        [Input('request-dropdown', 'value')]
    )
    def display_request_data_from_dropdown(request_id):
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
        print("Triggered?")
        if color_code == "id_default":
            return dash.no_update
        print("Triggered!")
        fig = single_telescope_plot_gantt(df, color_code)
        return fig

    #### Run the app #######################################################
    app.run_server(debug=False)
    # NOTE: With debug=True, the app can be updated when the code is changed,
    # allowing for better prototyping. However, it runs the original script
    # twice to allow for this in a subprocess, so is not ideal for final script.

################################################################################

def create_display_dict(row):
    # Request Scheduling Information
    if row['scheduled']:
        scheduled_info = odict()
        scheduled_info['Telescope'] = row['telescope']
        scheduled_info['Start'] = row['start_dt']
        scheduled_info['End'] = row['end_dt']
        scheduled_key = "Scheduled: Yes"
    else:
        scheduled_info = "No"
        scheduled_key = "Scheduled"

    # Request Proposal Information
    proposal_info = odict()
    proposal_info['Name'] = row['proposal']
    proposal_info['Priority'] = row['proposal_priority']

    # Request Details
    details_info = odict()
    details_info['Acceptability Threshold'] = row['acceptability_threshold']
    details_info['Observation Windows'] = row['windows']
    details_info['Configurations'] = row['configurations']

    # Macro Information
    dd = odict()
    dd['Request Name'] = row['name']
    dd['Type'] = row['observation_type']
    dd[scheduled_key] = scheduled_info
    dd['Proposal'] = proposal_info
    dd['IPP'] = row['ipp_value']
    dd['Duration'] = str(row['duration']) + " seconds"
    dd['Total Priority (Proposal * IPP * Duration)'] = row['priority_total']
    dd['Details'] = details_info

    return dd


# ################################################################################

if __name__ == '__main__':
    input_filepath = "sample_files/sample_input.pickle"
    output_filepath = "sample_files/sample_output.json"
    single_telescope(input_filepath, output_filepath)
