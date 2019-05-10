import plotly.offline as py
import plotly.figure_factory as ff
import pandas as pd
import json

# import schedule data into a pandas dataframe
# load it into a gantt chart
# fix axes
    # how to get rid of dates and only use times?
# fix tooltips
# fix colour coding

# # Obtain data from the scheduler output
# filename = "normal_schedule_20190416024632.json"
# with open(filename, "r") as openfile:
#     data = json.loads(openfile.read())
#
# semester_id = data['semester_id']
# schedule_start = data['schedule_start']
# schedule_end = data['schedule_end']
# horizon_days = data['horizon_days']
# total_priority = data['total_priority_value']
#
# telescope_name = "4m0a.doma.sor"
# telescope_info = data['resources'][telescope_name]
# telescope_priority = telescope_info['priority_value']
# dark_intervals = telescope_info['dark_intervals']
#
# def format_block(r):
#     r_id = x['request_id']
#     r_start = str(x['start']).split("T")
#     r_sd = r_start[0]
#     r_st = r_start[1]
#     r_end = str(x['end']).split("T")
#     r_ed = r_end[0]
#     r_et = r_end[1]
#     return (r_id,r_sd,r_st,r_ed,r_et)
#
# scheduled_requests = [ format_block(x) for x in telescope_info['reservations']]
#
# # Split up any requests that occur over midnight
# requests = []
# split_requests = []
# for req in scheduled_requests:
#     if req[1] != req[3]:
#         split_requests.append(req)
#     else:
#         requests.append(req)
#
# for r in split_requests:
#     requests.append( r[:3] + (r[1], '23:59:59') )
#     requests.append( (r[0], r[3], '00:00:00', r[3], r[4]) )
#
#
# # Obtain data from the input requests
# data = json.load(open("input_request_data.json","r"))
# available_telescopes = data['available_resources']
# semester_details = data['semester_details']
#
# request_groups = data['json_request_group_list']
#
# def format_request(r):
#     ipp = 0
#
#




ffd = [ x for x in scheduled_requests if (x[1] == '2019-04-17' or x[3] == '2019-04-17')]

df = [dict(Task=1,Start=x[1]+" "+x[2],Finish=x[3]+" "+x[4]) for x in requests]

fig = ff.create_gantt(df, title='Daily Schedule',showgrid_x=True,
    showgrid_y=True, group_tasks=True)
py.plot(fig, filename='gantt-simple-gantt-chart.html')

print schedule_start, schedule_end

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
