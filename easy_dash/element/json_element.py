import json

from easy_dash.element.base import Element
from easy_dash.app import * 


class JsonElement(Element):
    def __init__(self,id=None):
        super().__init__(id=id)

    def init_callback(self, app=None):
        pass

    def to_json(self):
        return {}
    
    def to_string(self):
        return  json.dumps( self.to_json(),ensure_ascii=False)

    def layout(self, app=None):
        return super().layout(app)