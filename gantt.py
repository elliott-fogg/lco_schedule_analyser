import plotly.offline as py
import plotly.figure_factory as ff
import pandas as pd
import json, datetime


# Create a Gantt Chart in Plotly from a Pandas Dataframe
def create_gantt(df):

    ##### Pandas manipulation functions ###################################
    def nominal_date(str_date):
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
        return "ID:{}\n\nStart: {}\n\nEnd: {}".format(id,start,finish)

    ##### Pandas Manipulation #############################################
    df['nominal_day'] = df['start'].apply(nominal_date)
    df['start_time'] = df['start_time'].apply(placeholder_datetime)
    df['finish_time'] = df['finish_time'].apply(placeholder_datetime)
    duplicate_columns(df,Task="nominal_day",Start="start_time",Finish="finish_time")
    df['hovertext'] = df.apply(lambda x: set_hovertext(x['id'],x['start'],x['finish']),axis=1)
    df = df.sort_values(by=['id'],ascending=True).reset_index(drop=True)

    ##### Colour-Coding functions #########################################

    def colour_by_id(df):
        id_max = df['id'].max()
        id_min = df['id'].min()
        num_values = id_max - id_min + 1

        colour_map = {}
        for i in df['id']:
            red_val = ((i - id_min) / float(num_values)) * 255.
            colour = "rgb({}, 0, 0)".format(red_val)
            colour_map[i] = colour

        return colour_map

    ##### Plot Creation ###################################################

    colors = colour_by_id(df)

    fig = ff.create_gantt(df, title='Example SOAR Schedule',showgrid_x=True,
        showgrid_y=True, group_tasks=True, colors=colors, index_col='id')

    ##### Final Layout Modifications ######################################

    # Modify the hovertext
    for k in range(len(fig['data'])):
        text = df['hovertext'].loc[k]
        fig['data'][k].update(text=text,hoverinfo="text")

    # Change axes labels to only use times
    fig['layout']['xaxis']['tickformat'] = "%H:%M%p"

    # Remove rangeselector buttons
    fig['layout']['xaxis']['rangeselector']['visible'] = False

    # Reenable autosizing
    del fig['layout']['height']
    del fig['layout']['width']

    return df, fig


################################################################################

if __name__ == "__main__":
    from format_data import *
    df = obtain_dataframe()
    df, fig = create_gantt(df)
    print json.dumps(fig)
    py.plot(fig, filename='../data/gantt_test_chart.html')
