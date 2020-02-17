import plotly.offline as py
import plotly.figure_factory as ff
import pandas as pd
from numpy import nan as NAN
from colorsys import hsv_to_rgb, yiq_to_rgb
import json, datetime

# Add the necessary plotting information to the dataframe
def configure_df_for_plotting(df):
    import pickle
    pickle.dump(df, open("temp_df.tmp", "wb"))

    ##### Pandas manipulation functions ###################################
    def nominal_date(str_date):
        if pd.isnull(str_date):
            return NAN
        input_format="%Y-%m-%d %H:%M:%S"
        output_format="%Y-%m-%d"
        try:
            date = datetime.datetime.strptime(str_date,input_format)
            placeholder_datetime(str_date.split()[1])
            if date.time() > datetime.time(12):
                return date.strftime(output_format)
            else:
                previous_day = date - datetime.timedelta(days=1)
                return previous_day.strftime(output_format)
        except ValueError:
            date = None

    def placeholder_datetime(time):
        if pd.isnull(time):
            return NAN
        time = datetime.datetime.strptime(time,"%H:%M:%S")
        if time.time() < datetime.time(12):
            time = time + datetime.timedelta(days=1)
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def duplicate_columns(df,**kwargs):
        try:
            for new_col in kwargs:
                old_col = kwargs[new_col]
                df[new_col] = df[old_col]
        except Exception as e:
            print e
        return df

    def set_hovertext(id,start,finish):
        if pd.isnull(start):
            return NAN
        return "ID:{}\n\nStart: {}\n\nEnd: {}".format(id,start,finish)

    ##### Pandas Manipulation #############################################
    df['nominal_day'] = df['start'].apply(nominal_date)
    df['start_time'] = df['start_time'].apply(placeholder_datetime)
    df['finish_time'] = df['finish_time'].apply(placeholder_datetime)
    duplicate_columns(df,Task="nominal_day",\
        Start="start_time",Finish="finish_time")
    df['hovertext'] = df.apply(\
        lambda x: set_hovertext(x['request_id'],x['start'],x['finish']),axis=1)

    df = df.sort_values(by='scheduled',\
        ascending=False).reset_index(drop=True)
    df['curve'] = df.index
    df.loc[df['scheduled'] == False, 'curve'] = NAN

    pickle.dump(df, open("temp_df2.tmp", "wb"))

    return df


# Create a Gantt Chart in Plotly from a Pandas Dataframe
def create_gantt(df,color_code='id'):

    df_plot = df[df['scheduled']]

    ##### Basic Color Functions ##########################################

    def spaced_colors(n):
        colors = [
            [ int(c * 255) for c in hsv_to_rgb(float(i) / n,1,1) ] \
            for i in range(n)
        ]
        return colors

    def scale_color(p):
        i_val = p  - 0.5
        return [ int(c * 255) for c in yiq_to_rgb(1,i_val,0.5) ]

    ##### Color-Coding Functions #########################################

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
            # print value, proportion
            c = scale_color(proportion)
            print c
            rgb = "rgb({}, {}, {})".format(c[0],c[1],c[2])
            print rgb
            color_map[value] = rgb

        return color_map


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

    ##### Plot Creation ###################################################

    colors, color_key = colormap(df_plot, color_code)

    global OBJECT_VAR
    OBJECT_VAR = df_plot

    df_plot = df_plot.reset_index(drop=True)

    fig = ff.create_gantt(df_plot, title='Example SOAR Schedule', \
        showgrid_x=True, showgrid_y=True, group_tasks=True, \
        colors=colors, index_col=color_key)

    ##### Final Layout Modifications ######################################

    print(len(df_plot))

    # Modify the hovertext
    for k in range(len(df_plot['hovertext'])):
        text = df_plot['hovertext'].loc[k]
        fig['data'][k].update(text=text,hoverinfo="text")

    # Change axes labels to only use times
    fig['layout']['xaxis']['tickformat'] = "%H:%M%p"

    # Remove rangeselector buttons
    fig['layout']['xaxis']['rangeselector']['visible'] = False

    # Reenable autosizing
    # del fig['layout']['height']
    # del fig['layout']['width']

    return fig


################################################################################

if __name__ == "__main__":
    from format_data import *
    df = obtain_dataframe()
    df = configure_df_for_plotting(df)
    fig = create_gantt(df,'id')
    # print json.dumps(fig)
    py.plot(fig, filename='plots/gantt_test_chart.html')
