# It looks like the contention of the network is to split the RA span (24 hours)
# into chunks. For each configuration of each request, add the duration of the
# configuration to the nearest bin of the RA of its target.
from numpy import floor
import plotly.offline as py
import plotly.graph_objs as go
from format_data import obtain_dataframe

def contention(df,anonymous=True,hour_divs=1):
    # for each user:
        # get list of bins (24 / 15)
    # cycle through requests
        # cycle through configurations
        # Determine bin closest to target RA
        # Add duration of configuration to bin
    proposals = df['proposal_name'].unique()
    contention = {}
    for user in proposals:
        contention[user] = [ 0 for i in range(24 * hour_divs) ]
    for request in df[['proposal_name','configurations','request_id']].itertuples():
        configurations = request.configurations
        proposal = request.proposal_name
        rid = request.request_id

        for config in configurations:
            ra = config['target_ra']
            ra_hours = ra / 15.
            # print rid, ra_hours
            floored_ra_interval = int(floor(ra_hours * hour_divs))
            for instr_config in config['instrument_configs']:
                duration = instr_config['exposure_time'] * instr_config['exposure_count'] / 3600
                contention[proposal][floored_ra_interval] += duration

    if anonymous:
        total_contention = [ 0 for i in range(24 * hour_divs) ]
        for user in contention:
            for i in range(len(contention[user])):
                total_contention[i] += contention[user][i]
        bar_data = [go.Bar(
            x= [ i / float(hour_divs) for i in range(24*hour_divs) ],
            y=total_contention
        )]

        layout = go.Layout(
            xaxis={
                'tickmode': 'linear',
                'ticks': 'outside',
                'tick0': 0,
                'dtick': 1. / hour_divs
            }
        )

        fig = go.Figure(data=bar_data, layout=layout)

    else:
        bar_data = [
            go.Bar(
                x= [ i / float(hour_divs) for i in range(24*hour_divs) ],
                y = contention[user],
                name=user
            ) for user in proposals
        ]

        layout = go.Layout(
            barmode='stack',
            xaxis={
                'tickmode': 'linear',
                'ticks': 'outside',
                'tick0': 0,
                'dtick': 1. / hour_divs
            }
        )

        fig = go.Figure(data=bar_data, layout=layout)
    return fig

def pressure():
    pass
    # get observation of observing block
    # divide by length of time target is viewable by the telescope
    ## (then divide by number of telescopes, which is 1, so ignore.)
    # add this pressure to all time periods that are within the observing window

if __name__ == '__main__':
    df = obtain_dataframe()
    fig = contention(df)
    py.plot(fig, filename='plots/stacked-bar.html')

# For the pressure on the network, the total required time of the observing
# block is divided by the sum total time that it is seeable by all telescopes
# (i.e. the length of time visible on telescope_1 + the length of time visible
#  on  telescope_2 + ... etc). For each time bin that these windows overlap,
# this value is then divided by the number of telescopes that can see it during
# that time bin, and then added to that bin.

# https://github.com/LCOGT/observation-portal/blob/master/observation_portal/requestgroups/contention.py
