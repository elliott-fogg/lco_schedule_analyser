@app.callback(
    Output(component_id='mapbox',component_property='figure'),
    [Input(component_id='dist-drop', component_property='value')]
)
def update_map(city_value):
    #function to deliver lat and lon from value in drop box
    if city_value == 'Montreal':
        latx = ["45.5017"]
        longx = ["-73.5673"]
    else:
        latx = ["46.829853"]
        longx = ["-71.254028"]


    return {
                "data": [
                    dict(
                        type = "scattermapbox",
                        lat = latx,
                        lon = longx,
                        mode = "markers",
                        marker = dict(size = 14),
                        text = city_value)],
                'layout': dict(
                    autosize = True,
                    hovermode = "closest",
                    margin = dict(l = 0, r = 0, t = 0, b = 0),
                    mapbox = dict(
                        accesstoken = mapbox_access_token,
                        bearing = 0,
                        center = dict(lat = 45, lon = -73),
                        pitch = 0,
                        zoom = 5
                    )
                )
            }
