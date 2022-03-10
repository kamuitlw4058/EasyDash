import folium
import json
from easy_dash.page.page import Page
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

from easy_dash.app import * 

def parse_zhch(s):
    return str(str(s).encode('ascii' , 'xmlcharrefreplace'))[2:-1]

class MapModelParams(): 
    def __init__(self,markers=None,center=[31.23136, 121.47004],zoom=13,geojson=None,color_prop = None,vmax=100,cluster=True):
        self.center = center
        self.zoom = zoom
        self.markers = markers
        self.geojson = geojson
        self.color_prop = color_prop
        self.vmax = vmax
        self.cluster = cluster

class MapModel():
    def __init__(self,params:MapModelParams):
        self.params = params
        self.map = None
        self.init_map()

    def init_map(self):
        self.map = folium.Map(location=[31.1589, 121.4092], zoom_start=10,
        default_css = [('leaflet_css', 'http://localhost:9999/cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css'), 
        ('bootstrap_css', 'http://localhost:9999/maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'), 
        ('bootstrap_theme_css', 'http://localhost:9999/maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css'),
        ('awesome_markers_font_css', 'http://localhost:9999/maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css'),
        ('awesome_markers_css', 'http://localhost:9999/cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css'),
        ('awesome_rotate_css', 'http://localhost:9999/cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css')],
        default_js = [('leaflet', 'http://localhost:9999/cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js'),
            ('jquery', 'http://localhost:9999/code.jquery.com/jquery-1.12.4.min.js'),
            ('bootstrap', 'http://localhost:9999/maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'),
            ('awesome_markers', 'http://localhost:9999/cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js')],
        tiles = 'http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
        # tiles = 'https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=2&style=8&ltype=11',
        # tiles = 'http://wprd04.is.autonavi.com/appmaptile?lang=zh_cn&size=1&style=7&x={x}&y={y}&z={z}',
        attr = 'default'
        )

    def build_ext(self):
        ret = []
        if self.params.markers is not None:
            for item in self.params.markers:
                ret.append(dl.Marker(position=item))

        if self.params.geojson is not None:
            geojson = dlx.dicts_to_geojson(self.params.geojson)  # convert to geojson
            geobuf = dlx.geojson_to_geobuf(geojson)  # convert to geobuf
            colorscale = [ 'green','yellow', 'orange', 'red']
            
            point_to_layer = assign("""function(feature, latlng, context){
                const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
                const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
                if (colorProp == "" || colorProp == undefined || colorProp == null){
                    circleOptions.fillColor = csc(min);
                }else{
                    circleOptions.fillColor = csc(feature.properties[colorProp]);
                }
                  // set color based on color prop.
                return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
            }""")

            cluster_to_layer = assign("""function(feature, latlng, index, context){
                const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
                const csc = chroma.scale(colorscale).domain([min, max]);
                // Set color based on mean value of leaves.
                const leaves = index.getLeaves(feature.properties.cluster_id);
                let valueSum = 0;
                for (let i = 0; i < leaves.length; ++i) {
                    valueSum += leaves[i].properties[colorProp]
                }
                const valueMean = valueSum / leaves.length;
                // Render a circle with the number of leaves written in the center.
                const icon = L.divIcon.scatter({
                    html: '<div style="background-color:white;"><span>' + feature.properties.point_count_abbreviated + '</span></div>',
                    className: "marker-cluster",
                    iconSize: L.point(40, 40),
                    color: csc(valueMean)
                });
                return L.marker(latlng, {icon : icon})
            }""")
            if self.params.cluster:
                apply_cluster_to_layer =  cluster_to_layer
            else:
                apply_cluster_to_layer = None
            geojson = dl.GeoJSON(data=geobuf, format="geobuf",
                        zoomToBounds=True,  # when true, zooms to bounds when data changes
                        cluster=self.params.cluster,
                        clusterToLayer=apply_cluster_to_layer,
                        zoomToBoundsOnClick=self.params.cluster,
                        options=dict(pointToLayer=point_to_layer),  # how to draw points
                        superClusterOptions=dict(radius=50),   # adjust cluster size
                        hideout=dict(colorProp=self.params.color_prop, circleOptions=dict(fillOpacity=1, stroke=False, radius=5),
                                    min=0, max=self.params.vmax, colorscale=colorscale))
            colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=200, min=0, max=self.params.vmax, unit='kg',nTicks=5)

            ret.extend([geojson,colorbar])
        return ret

    
    def build_map(self):
        layers = [dl.TileLayer(url='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}'),
        ]
        layers.extend(self.build_ext())
        # print(layers)
        return dl.Map(
            center=self.params.center,
            zoom=self.params.zoom,
            children=layers)

    def layout(self):
        # return html.Div(dhtml.DangerouslySetInnerHTML(self.map._repr_html_()))
        return html.Div(self.build_map(), style={'width': '100%', 'height': '80vh', 'margin': "auto", "display": "inline-block"})

