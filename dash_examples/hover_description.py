import plotly
import plotly.figure_factory as ff
import plotly.offline as py

df = [
    dict(Task='Evening Sleep', Start='2009-01-01', Finish='2009-02-28', Resource='Sleep', Description = 'my hover1' ),
    dict(Task='Morning Sleep', Start='2009-03-05', Finish='2009-04-15', Resource='Sleep', Description = 'my hover1')
]

colors = dict(Cardio = 'rgb(46, 137, 205)',
              Food = 'rgb(114, 44, 121)',
              Sleep = 'rgb(198, 47, 105)')

fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='Daily Schedule',
                      show_colorbar=True, showgrid_x=True, showgrid_y=True, group_tasks=True)

py.plot(fig, filename='plots/hover_description.html')
