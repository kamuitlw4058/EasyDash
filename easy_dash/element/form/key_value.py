
from easy_dash.element.base import Element
from easy_dash.app import * 


class KeyValueElement(Element):
    def __init__(self,key,value,display_name=None ,disabled=False):
        super().__init__(id=id)
        self.key = key
        self.value = value
        if display_name is None:
            self.display_name = self.key
        else:
            self.display_name = display_name
        self.disabled = disabled

    def init_callback(self, app=None):
        if isinstance(self.value,Element):
            self.value.init_callback(app=app)
    
    def value_id(self):
        return f'{self.id()}-value'

    
    def to_string(self):
        return f'key:{self.key} value:{self.value}'

    def layout(self, app=None):
        if isinstance(self.value,Element):
            value_layout = self.value.layout()
        else:
            value_layout =  dbc.Input(type="text", value=self.value,disabled=self.disabled,id=self.value_id())

        return  [dbc.Label(self.display_name,width=2),
                dbc.Col(value_layout,width=5)]

            