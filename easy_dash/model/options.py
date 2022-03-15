import json
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

from easy_dash.app import * 


class OptionModelParams(): 
    def __init__(self):
        pass


class OptionModel():
    def __init__(self,params:OptionModelParams):
        self.params = params

    
    def update_func(self):
        pass

    def layout(self):
        pass
