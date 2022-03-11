import pandas as pd
import json

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

from dash import Dash, html, Output, Input
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign
from geopy.distance import geodesic

from easy_dash.page.page import Page
from easy_dash.app import * 

def geojson_key(feature):
    feature_type = feature['type']
    properties = feature.get('properties',{})
    properties_type = properties.get('type','')
    geometry =  feature.get('geometry',{})
    geometry_type = geometry.get('type','')
    coordinates = geometry.get('coordinates',[])
    return f'{feature_type}#{properties_type}#{geometry_type}#{coordinates}'




def geojson_features_dict(d,features):
    for feature in features:
        k = json.dumps(feature)
        d[geojson_key(feature)] = feature
        
#{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'_leaflet_id': 83}}, {'type': 'Feature', 'properties': {'type': 'polyline', '_bounds': [{'lat': 31.242135175350022, 'lng': 121.40012741088869}, {'lat': 31.260488589655434, 'lng': 121.417293548584}], '_leaflet_id': 129}, 'geometry': {'type': 'LineString', 'coordinates': [[121.40012741088869, 31.260488589655434], [121.417293548584, 31.242135175350022]]}}]}
def merge_geojson(gj1,gj2):
    ret = {}
    if gj1 is None:
        gj1 = {}

    if gj2 is None:
        gj2= {}

    gj1_features = gj1.get('features',[])
    gj2_features = gj2.get('features',[])
    geojson_features_dict(ret,gj1_features)
    geojson_features_dict(ret,gj2_features)
    
    return {
        'type': 'FeatureCollection', 'features':list(ret.values())
    }   



class MapEditPage(Page):
    def __init__(self, module_name, page_name, module_title=None, page_title=None):
        super().__init__(module_name, page_name, module_title, page_title)
        self.geojson = None
        self.map = None

    def edit_control_id(self):
        return f"{self.page_key()}-edit-control"

    def geojson_id(self):
        return f'{self.page_key()}-geojson'

    def display_geojson_id(self):
        return f'{self.page_key()}-display-geojson'

    def textarea_id(self):
        return f'{self.page_key()}-textarea'

    def button_id(self):
        return f'{self.page_key()}-button'

    def store_id(self):
        return f'{self.page_key()}-store'

    def init_callback(self,app=None):
        if app is not None:
            print('init callback')
            @app.callback(
                Output(self.geojson_id(), "data"),
                Input(self.store_id(),'data')
            )
            def update_map(data):
                v = data.get('geojson',None)
                # print(f'update v:{v}')
                return v

            @app.callback(
                Output(self.store_id(), "data"),
                Input(self.button_id(), "n_clicks"),
                Input(self.edit_control_id(), "geojson"),
                State(self.textarea_id(), "value"),
                State(self.store_id(),'data')
            )
            def append_km(n,geojson,text_geojson,old_data):
                # print(f'enter append_km {geojson},{n}')
                # print(f'enter append_km old_data:{old_data}')
                # print(f'text_geojson:{text_geojson} ')
               
                if old_data is None:
                    old_data = {
                        'clicks':None,
                        'geojson':None
                    }
                old_clicks = old_data.get('clicks',0)
                # print(f'enter func n:{n} o:{old_clicks}')


                old_geojson =  old_data.get('geojson',{})
                display_geojson = {}
                try:
                    display_geojson = json.loads(text_geojson)
                except Exception as e:
                    print(e)
                    pass
                
                # old_geojson =  merge_geojson(old_geojson,display_geojson)
                
                if  old_clicks != n and n:
                    print('by click')
                    # display_geojson
                    # geojson = merge_geojson(geojson,old_geojson)
                    print(f'display_geojson:{display_geojson}')
                    return {
                         'clicks':n,
                         'geojson': display_geojson
                     }

                if geojson is not None:
                    print('by update edit')
                    if geojson is not None:
                        # print(geojson)
                        features = geojson['features']
                        for feature in features:
                            # print(feature)
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
                                        distance = round(distance,1)
                                        features.append(
                                            {
                                            'type': 'Feature',
                                                'properties': {'type': 'text','distance':distance},
                                                'geometry': {'type': 'Point', 'coordinates': geometry['coordinates'][-1]}
                                            }
                                        )
                else:
                    print('stop update')
                    raise PreventUpdate
                geojson = merge_geojson(geojson,old_geojson)
                print(geojson)
                # if len(geojson.get('features')) > 0:
                #     leaflet_id  = geojson.get('features')[0][]
                return {
                    'clicks':n,
                    'geojson': geojson
                }

            @app.callback(
                Output(self.textarea_id(), "value"),
                Input(self.store_id(), "data")
            )
            def output_geojson(data):
                geojson = data.get('geojson',None)
                return json.dumps(geojson)
            

    def build_map(self):
        # if self.geojson:
        #     geojson = self.geojson
        # else:
        geojson = None
        
        if self.map is None:
            draw_point = assign("""function(feature, latlng, context){
            const p = feature.properties;
            if(p.type === 'text'){
                const flag = L.divIcon({html: `<h6><span class="badge bg-secondary">${p.distance}km</span></h6>`,className: `map-text`, iconAnchor: [20, -4],iconSize: [86, 22]});
                return L.marker(latlng, {icon: flag});
            }
            if(p.type === 'circlemarker'){return L.circleMarker(latlng, radius=p._radius)}
            if(p.type === 'circle'){return L.circle(latlng, radius=p._mRadius)}
            }""")
            self.map  = dl.Map(
            center=[31.23136, 121.47004],
            zoom=13,
            children=[
                dl.TileLayer(
                    url='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}'
                ), dl.FeatureGroup([
                    dl.EditControl(id=self.edit_control_id()),
                    dl.GeoJSON(id=self.geojson_id(),data=geojson, options=dict(pointToLayer=draw_point), zoomToBounds=True),
                    # dl.GeoJSON(id=self.display_geojson_id(),data=geojson, options=dict(pointToLayer=draw_point), zoomToBounds=True)
                ]),
        ], style={'width': '100%', 'height': '80vh', 'margin': "auto", "display": "inline-block"}, id=f"{self.page_key()}-map")

        return self.map

    def layout(self):
        return [
            self.build_map(),
            dcc.Store(id=self.store_id(), storage_type='memory'),
            dbc.Row([
                dbc.Col(
                dbc.Button(
                    "更新地图",
                    id=self.button_id(),
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),width=1),
                dbc.Col(
                    dcc.Textarea(
                            id=self.textarea_id(),
                            value = '',
                            style={'width': '100%', 'height': '500px'},
                    )
                    ,width=11)
            ])

        ]

