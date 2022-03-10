import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

from dash import Dash, html, Output, Input
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

from dash_extensions.javascript import assign
from geopy.distance import geodesic

# A few countries.
countries = [dict(name="测试asdfasdfds",  lat=31.255256, lon=121.207784),]
# countries = [dict(name="测试asdfasdfds",  lat=121.207784, lon=31.255256),]

# Generate geojson with a marker for each country and name as tooltip.
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in countries])

# How to render geojson.
point_to_layer = assign("""function(feature, latlng, context){
    const p = feature.properties;
    if(p.type === 'circlemarker'){return L.circleMarker(latlng, radius=p._radius)}
    if(p.type === 'circle'){return L.circle(latlng, radius=p._mRadius)}
    return L.marker(latlng);
}""")

#${feature.properties.name}
#return L.marker(latlng, {icon: flag});
# const flag = L.divIcon({html: `测试`});
#const flag = L.divIcon({html:`测试`, className: `map-text`, iconAnchor: [43, -4],iconSize: [86, 22]});
# const flag = L.divIcon({html:`测试`, className: `map-text`});

# const flag = L.divIcon({html: `测试`,className: `map-text`, iconAnchor: [43, -4],iconSize: [86, 22]});
# const flag = L.divIcon({html: `测试`,className: `map-angle`, iconAnchor: [0, 9],iconSize: [6, 5]]});

# const flag = L.divIcon({html: `测试`,className: `map-text map-text-error`, iconAnchor: [0, 9],iconSize: [6, 5]]});
# let textIcon = L.divIcon({
#   html: name,
#   className: "map-text map-text-" + colorClass,
#   iconAnchor: [6 * (name.length + 1) + 1, -4],
#   iconSize: [12 * (name.length + 1) + 2, 22]
# });
# const flag = L.divIcon({html: `测试`,className: `map-text`, iconAnchor: [43, -4],iconSize: [86, 22]});

draw_text = assign("""function(feature, latlng, context){
const p = feature.properties;
const flag = L.divIcon({html: `${p.distance}km`,className: `map-text`, iconAnchor: [20, -4],iconSize: [86, 22]});
return L.marker(latlng, {icon: flag});
}""")

#  var myIcon = L.divIcon({
#             html: "狗子",
#             className: 'my-div-icon',
#             iconSize:30
#         });
#         L.marker([31.864942016,117.2882028929], { icon: myIcon }).addTo(map);


countries = [
    dict(name="测试asdfasdfds",iso2="dk",   lat=31.255256, lon=121.207784),
            # dict(name="Denmark", iso2="dk", lat=56.26392, lon=9.501785),
            #  dict(name="Sweden", iso2="se", lat=59.334591, lon=18.063240),
            #  dict(name="Norway", iso2="no", lat=59.911491, lon=9.501785)
             ]
# Generate geojson with a marker for each country and name as tooltip.
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in countries])
# Create javascript function that draws a marker with a custom icon, in this case a flag hosted by flagcdn.
draw_flag = assign("""function(feature, latlng){
const flag = L.icon({iconUrl: `https://flagcdn.com/64x48/${feature.properties.iso2}.png`, className: `map-text`, iconAnchor: [43, -4],iconSize: [86, 22]});
return L.marker(latlng, {icon: flag});
}""")


# Create example app.
app = Dash()
app.layout = html.Div([
    # Setup a map with the edit control.
    dl.Map(center=[31.255256,121.207784], zoom=11, children=[
        dl.TileLayer(
            url='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}'
        ), dl.FeatureGroup([
            dl.EditControl(id="edit_control"),
            # dl.GeoJSON(data=geojson, options=dict(pointToLayer=draw_flag), zoomToBounds=True)
            dl.GeoJSON(id="okjson",data=geojson, options=dict(pointToLayer=draw_text), zoomToBounds=True)
        # dl.Marker(position=[31.255256,121.207784]),
        
        ]),
        # dl.GeoJSON(data=geojson, options=dict(pointToLayer=draw_text), zoomToBounds=True)
    ], style={'width': '50%', 'height': '50vh', 'margin': "auto", "display": "inline-block"}, id="map"),
    # Setup another map to that mirrors the edit control geometries using the GeoJSON component.
    dl.Map(center=[31.255256,121.207784], zoom=4, children=[
        dl.TileLayer(), dl.GeoJSON(id="geojson", options=dict(pointToLayer=point_to_layer), zoomToBounds=True),
    ], style={'width': '50%', 'height': '50vh', 'margin': "auto", "display": "inline-block"}, id="mirror"),
])

# Copy data from the edit control to the geojson component.
@app.callback(Output("okjson", "data"), Input("edit_control", "geojson"))
def mirror(x):
    ret =[]
    if not x:
        raise PreventUpdate

    features = x['features']
    for feature in features:
        print(feature)
        feature_type = feature['type']
        if feature_type == 'Feature':
            properties = feature['properties']
            geometry = feature.get('geometry',None)
            if geometry is not None:
                geometry_type = geometry['type']
                if geometry_type == 'LineString':
                    distance = 0
                    for i,v in enumerate(geometry['coordinates'][:-1]):
                        lat1 = geometry['coordinates'][i][0]
                        lng1 = geometry['coordinates'][i][1]
                        lat2 = geometry['coordinates'][i+1][0]
                        lng2 = geometry['coordinates'][i+1][1]

                        distance += geodesic((lng1,lat1), (lng2,lat2)).km
                    distance = round(distance,3)
                    features.append(
                        {
                        'type': 'Feature',
                            'properties': {'type': 'circlemarker','distance':distance},
                            'geometry': {'type': 'Point', 'coordinates': geometry['coordinates'][-1]}
                        }
                    )


    return x

if __name__ == '__main__':
    app.run_server()