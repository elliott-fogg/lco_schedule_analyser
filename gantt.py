import plotly.offline as py
import plotly.figure_factory as ff
import pandas as pd
import json, datetime

def create_gantt(df):
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

    df['nominal_day'] = df['start'].apply(nominal_date)
    df['start_time'] = df['start_time'].apply(placeholder_datetime)
    df['finish_time'] = df['finish_time'].apply(placeholder_datetime)

    def duplicate_columns(df,**kwargs):
        try:
            for new_col in kwargs:
                old_col = kwargs[new_col]
                df[new_col] = df[old_col]
        except Exception as e:
            print e
        return df

    duplicate_columns(df,Task="nominal_day",Start="start_time",Finish="finish_time")

    def set_hovertext(id,start,finish):
        return "Request {}: {} to {}".format(id,start,finish)


    df['hovertext'] = df.apply(lambda x: set_hovertext(x['id'],x['start'],x['finish']),axis=1)

    # df.rename(columns={
    #     "nominal_day":"Task",
    #     "start_time":"Start",
    #     "finish_time":"Finish",
    #     },inplace=True)

    df = df.sort_values(by=['id'],ascending=True).reset_index(drop=True)
    print df['id']

    # # Set colour coding
    # def colour_code(start,stop):
    #     colour_dict = {}
    #     n = start-stop+1
    #     halfway = int(n/2)
    #     for i in range(halfway):
    #         passs

    colour_code = {}
    for i in range(104-59):
        #print (104-49)/2
        c = int(i / (103.-59.) * 255.)
        colour = 'rgb({}, 0, 0)'.format(c)
        #print c, colour, i+59
        colour_code[i+59] = colour

    fig = ff.create_gantt(df, title='Example SOAR Schedule',showgrid_x=True,
        showgrid_y=True, group_tasks=True, colors=colour_code, index_col='id')

    # Modifying the hovertext
    for k in range(len(fig['data'])):
        text = df['hovertext'].loc[k]
        fig['data'][k].update(text=text,hoverinfo="text")

    # fig.layout.xaxis.tickformat = "%H:%M%p"
    fig['layout']['xaxis']['tickformat'] = "%H:%M%p"
    fig['layout']['xaxis']['rangeselector']['visible'] = False

    return df, fig

# fig.layout.xaxis.tickformat = "%H:%M%p"

# py.plot(fig, filename='../data/gantt_test_chart.html')

################################################################################

# ## Basic Gantt Data
# # df = [dict(Task="Job A", Start="2009-01-01", Finish="2009-02-28"),
# #       dict(Task="Job B", Start="2009-03-05", Finish="2009-04-15"),
# #       dict(Task="Job C", Start="2009-02-20", Finish="2009-05-30")]
#
# # Gantt Data using times as well as dates, and assigning colours
# # TODO: How to get rid of dates entirely??
# df = [
#     dict(Task='Morning Sleep', Start='2016-01-01', Finish='2016-01-01 6:00:00', Resource='Sleep'),
#     dict(Task='Breakfast', Start='2016-01-01 7:00:00', Finish='2016-01-01 7:30:00', Resource='Food'),
#     dict(Task='Work', Start='2016-01-01 9:00:00', Finish='2016-01-01 11:25:00', Resource='Brain'),
#     dict(Task='Break', Start='2016-01-01 11:30:00', Finish='2016-01-01 12:00:00', Resource='Rest'),
#     dict(Task='Lunch', Start='2016-01-01 12:00:00', Finish='2016-01-01 13:00:00', Resource='Food'),
#     dict(Task='Work', Start='2016-01-01 13:00:00', Finish='2016-01-01 17:00:00', Resource='Brain'),
#     dict(Task='Exercise', Start='2016-01-01 17:30:00', Finish='2016-01-01 18:30:00', Resource='Cardio'),
#     dict(Task='Post Workout Rest', Start='2016-01-01 18:30:00', Finish='2016-01-01 19:00:00', Resource='Rest'),
#     dict(Task='Dinner', Start='2016-01-01 19:00:00', Finish='2016-01-01 20:00:00', Resource='Food'),
#     dict(Task='Evening Sleep', Start='2016-01-01 21:00:00', Finish='2016-01-01 23:59:00', Resource='Sleep')
# ]
#
# colors = dict(Cardio = 'rgb(46, 137, 205)',
#               Food = 'rgb(114, 44, 121)',
#               Sleep = 'rgb(198, 47, 105)',
#               Brain = 'rgb(58, 149, 136)',
#               Rest = 'rgb(107, 127, 135)')
#
# fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='Daily Schedule',
#                       show_colorbar=True, bar_width=0.8, showgrid_x=True, showgrid_y=True)
# print py.plot(fig, filename='gantt-simple-gantt-chart')
#
# # # Gantt using pandas dataframes
# # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gantt_example.csv")
#
# # Grouping multiple items on the same lines
# df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
#       dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
#       dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
#       dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
#       dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
#       dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
#       dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
#       dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]
#
# colors = {'Not Started': 'rgb(220, 0, 0)',
#           'Incomplete': (1, 0.9, 0.16),
#           'Complete': 'rgb(0, 255, 100)'}
#
# fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)
# print py.plot(fig, filename='gantt-simple-gantt-chart2')
#
# # Concept:
# # A Gantt chart which has each row being a different day, with the observations
# # spaced by hours. Have the tooltip for each observation be the target (either name
# # or ra/dec) that is being observed, and the time scheduled, and maybe the priority?
# # If possible, make clicking on a bar open a json-tree-explorer in a frame below,
# # to allow you to see the details of the observation request.
# # ALSO have an additional row/several for observations that did not get scheduled.

if __name__ == "__main__":
    from format_data import *
    df = transform_to_plotly()
    fig = create_gantt(df)
    print json.dumps(fig)
    py.plot(fig, filename='../data/gantt_test_chart.html')
