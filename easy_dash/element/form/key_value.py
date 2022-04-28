from easy_dash.element.base import Element
# from easy_dash.element.layout.rows import RowsElement
from easy_dash.element.json_element import JsonElement 
from easy_dash.app import *

class KeyValueElement(JsonElement):
    def __init__(self,key,value,display_name=None ,editabled=True):
        super().__init__(id=id)
        self.key = key
        self.value = value
        if display_name is None:
            self.display_name = self.key
        else:
            self.display_name = display_name
        self.disabled = not editabled

    def init_callback(self, app=None):
        if isinstance(self.value,Element):
            self.value.init_callback(app=app)
    
    def value_id(self):
        return f'{self.id()}-value'

    def to_json(self):
        ret = {}
        if isinstance(self.value,Element) or isinstance(self.value,list):
            raise Exception(f'{type(self)} need value is  List or base type like int string...')
        # elif isinstance(self.value,list):
        #     ret_value =  RowsElement(self.value).to_json()
        else:
            ret_value = self.value
        return {
            self.key:ret_value
        }

    def to_string(self):
        return super().to_string()

    def layout(self, app=None):
        if isinstance(self.value,Element):
            value_layout = self.value.layout()
        else:
            value_layout =  dbc.Input(type="text", value=self.value,disabled=self.disabled,id=self.value_id())

        return  [dbc.Label(self.display_name,width=2),
                dbc.Col(value_layout,width=5)]

            