## TODO: Add documentation strings for all functions, like I should have done
##       in the first place.

import plotly.offline as py
from plotly import figure_factory
# import plotly.figure_factory as ff
import pandas as pd
from numpy import nan as NAN
from colorsys import hsv_to_rgb, yiq_to_rgb
import json
import datetime as dt

def gantt_single_telescope(df, color_code="id"):

    #### Pandas DataFrame Manipulation #####################################

    def nominal_start(dt_obj):
        date_format = "%Y-%m-%d"
        nominal_start = dt_obj
        if dt_obj.time() < dt.time(12):
            nominal_start -= dt.timedelta(days=1)
        return nominal_start.strftime(date_format)

    def nominal_datetime(dt_obj):
        datetime_format = "%Y-%m-%d %H:%M:%S"
        nominal_datetime = dt_obj.replace(2000,1,1)
        if dt_obj.time() < dt.time(12):
            nominal_datetime += dt.timedelta(days=1)
        return nominal_datetime.strftime(datetime_format)

    def set_hovertext(row):
        if not row['scheduled']:
            return NAN
        return "ID: {}\n\nStart: {}\n\nEnd: {}".format(
            row['request_id'], row['start_dt'], row['end_dt'])

    #### Creating the Gantt Plot ###########################################

    def gantt_plot(df):
        df_plot = df[ df['scheduled'] ]
        # df_plot.reset_index(drop=True, inplace=True)
        colors, color_key = colormap(df_plot, color_code)

        fig = figure_factory.create_gantt(df_plot, title="Example SOAR Schedule",
        showgrid_x=True, showgrid_y = True, group_tasks=True,
        colors = colors, index_col = color_key)

        # Modify the hovertext
        for k in range(len(df_plot['hovertext'])):
            text = df_plot['hovertext'].iloc[k]
            fig['data'][k].update(text=text, hoverinfo="text")

        # Change axes labels to only use times
        fig['layout']['xaxis']['tickformat'] = "%H:%M%p"

        # Remove rangeselector buttons
        fig['layout']['xaxis']['rangeselector']['visible'] = False

        print(type(fig))
        print(type(fig['layout']))

        # Reenable autosizing
        # if 'height' in fig['layout']:
        #     del fig['layout']['height']
        # if 'width' in fig['layout']:
        #     del fig['layout']['width']

        return fig

    ########################################################################

    df.loc[ df['scheduled'], 'Task'] = \
        df.loc[df['scheduled']]['start_dt'].apply(nominal_start)
    df.loc[df['scheduled'], 'Start'] = \
        df.loc[df['scheduled']]['start_dt'].apply(nominal_datetime)
    df.loc[df['scheduled'], 'Finish'] = \
        df.loc[df['scheduled']]['end_dt'].apply(nominal_datetime)

    df['hovertext'] = df.apply(set_hovertext, axis=1)
    df.sort_values(by="scheduled", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.loc[df['scheduled'], 'curve'] = df[df['scheduled']].index

    fig = gantt_plot(df)

    return (fig, df)


#### Color Functions ###########################################################

######## Basic Color Functions #############################################

def spaced_colors(n):
    colors = [
        [ int(c * 255) for c in hsv_to_rgb(float(i) / n,1,1) ] \
        for i in range(n)
    ]
    return colors

def scale_color(p):
    i_val = p  - 0.5
    return [ int(c * 255) for c in yiq_to_rgb(1,i_val,0.5) ]

######## Color-Coding Functions ############################################

def color_by_id(df, color_key):
    id_max = df['request_id'].max()
    id_min = df['request_id'].min()
    num_values = id_max - id_min + 1

    color_map = {}
    for i in df['request_id']:
        red_val = int(((i - id_min) / float(num_values)) * 255.)
        color = "rgb({}, 0, 0)".format(red_val)
        color_map[i] = color
    return color_map

def unique_colors(df,color_key):
    v = df[color_key].unique()
    n = len(v)
    c = spaced_colors(n)

    color_map = {}
    for i in range(n):
        color_map[v[i]] = "rgb({}, {}, {})".format(\
            int(c[i][0]), int(c[i][1]), int(c[i][2]))

    return color_map

def ipp_colors(df,color_key):
    v_max = df[color_key].max()
    v_min = df[color_key].min()
    v_list = df[color_key].unique()

    color_map = {}
    for value in v_list:
        proportion = ((value - v_min) / (v_max - v_min))
        print value, proportion
        c = scale_color(proportion)
        print c
        rgb = "rgb({}, {}, {})".format(c[0],c[1],c[2])
        print rgb
        color_map[value] = rgb

    return color_map

######## Color Map Selector ################################################

color_code_dict = {
    'id': [color_by_id,'request_id'],
    'proposal': [unique_colors,'proposal_priority'],
    'ipp': [ipp_colors,'ipp']
}

def colormap(df,color_code):
    selection = color_code_dict[color_code]
    _function = selection[0]
    value = selection[1]

    return _function(df,value), value

################################################################################
# XXX: This will need to be split - one for a single schedule over multiple days,
#      and one for multiple schedules, each inline.

# TODO: Create a function that will display the schedules of multiple telescopes,
#       and a function that will display the schedule of just one telescope, split
#       over multiple days (for better viewing).

def gantt_multi_telescope(df, color_code='id'):
    pass

################################################################################

if __name__ == "__main__":
    from format_data import *
    df = obtain_dataframe()
    fig, formatted_df = gantt_single_telescope(df)
    print(type(fig))
    print(type(formatted_df))
    py.plot(fig, filename='plots/gantt_test_chart.html')
