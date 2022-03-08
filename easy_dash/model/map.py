import folium
import json
from easy_dash.page.page import Page
from easy_dash.app import * 

def parse_zhch(s):
    return str(str(s).encode('ascii' , 'xmlcharrefreplace'))[2:-1]

class MapModelParams(): 
    def __init__(self,marks):
        self.marks = marks
        pass

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
    
    def build_map(self):
        tooltip = parse_zhch('用户')
        folium.Marker(['31.255256','121.207784'],
            popup=folium.Popup(html=parse_zhch('用户'),max_width=300,show=True),
            tooltip=tooltip,
            icon=folium.Icon(color='green' ,icon='glyphicon glyphicon-user' ,icon_color='red')
        ).add_to(self.map)

    def layout(self):
        return html.Div(dhtml.DangerouslySetInnerHTML(self.map._repr_html_()))
