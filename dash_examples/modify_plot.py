# update embedded plotly plot with drowdown

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# plotly plot embed urls
embed_urls = {
    'plot_1': 'https://plot.ly/~om_ad_ops/69140.embed',
    'plot_2': 'https://plot.ly/~om_ad_ops/69138.embed'
}

# initialize Dash object
app = dash.Dash()

# define dropdown whose options are embed urls
dd = dcc.Dropdown(
    id='dropdown',
    options= [{'label': k, 'value': v} for k, v in embed_urls.iteritems()],
    value=embed_urls.keys()[0],
)

# embedded plot element whose `src` parameter will
# be populated and updated with dropdown values
plot = html.Embed(
    id='plot',
    height=600,
    width=1000
)

# set div containing dropdown and embedded plot
app.layout = html.Div(children=[dd, plot])

# update `src` parameter on dropdown select action
@app.callback(
    Output(component_id='plot', component_property='src'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_plot_src(input_value):

    return input_value

if __name__ == '__main__':

    app.run_server(debug=True)
