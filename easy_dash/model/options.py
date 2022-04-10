import json

from jmespath import search
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

from easy_dash.app import * 
from easy_dash.element.base import Element


class OptionModelParams(): 
    def __init__(self,options=None, multi =False,options_inputs=None,options_states=None,option_update_func=None):
        self.multi = multi
        self.options = options
        self.options_inputs = options_inputs
        self.options_states = options_states
        self.option_update_func = option_update_func

class Option(Element):
    def __init__(self,options=None,multi=False, option_update_func=None,options_inputs=None,id=None):
        super(Option, self).__init__(id=id)

        self.multi = multi
        self.options = options
        self.options_inputs = options_inputs
        # self.options_states = options_states
        self.option_update_func = option_update_func

    def parse_options_inputs(self):
        if self.options_inputs is not None and isinstance(self.options_inputs,list):
            ret = {}
            for (k,v) in self.options_inputs:
                params_key =  f'{k}#{v}'
                ret[params_key]= Input(k,v)
            return ret
        return {}

    # def parse_options_states(self):
    #     if self.options_states is not None and isinstance(self.options_states,list):
    #         ret = {}
    #         for (k,v) in self.options_states:
    #             params_key =  f'{k}#{v}'
    #             ret[params_key]= State(k,v)
    #         return ret
    #     return {}
    
    def init_callback(self,app=None):
        if app is not None :
            # print('init options')
            if not self.multi:
                @app.callback(
                    Output(self.id(), "options"),
                    Input(self.id(), "search_value"),
                    Input(self.store_id(), "data")
                )
                def update_options(search_value,store_data:dict):
                    # if not search_value :
                    #     raise PreventUpdate

                    if store_data:
                        options=  store_data.get('options',[])
                    else:
                        options = self.options

                    # print(options)
                    if search_value:
                        ret = [o for o in options if  str(o["label"]).find(search_value) >= 0 ]
                    else:
                        ret = options

                    return ret
            else:

                @app.callback(
                    Output(self.id(), "options"),
                    Input(self.id(), "search_value"),
                    State(self.id(), "value"),
                    State(self.store_id(), "data")
                )
                def update_multi_options(search_value, value,store_data:dict):
                    if not search_value or not self.options:
                        raise PreventUpdate
                    
                    options=  store_data.get('options',[])
                    options.extend(self.options)
                    # Make sure that the set values are in the option list, else they will disappear
                    # from the shown select list, but still part of the `value`.
                    return [
                        o for o in options if  str(o["label"]).find(search_value) >= 0 or o["value"] in (value or [])
                    ]
            
            if   self.options_inputs is None and self.option_update_func is not None:
                self.options = self.option_update_func(None,None)
            
            # if len(self.parse_options_inputs()) > 0:
            #     @app.callback(
            #         output=Output(self.store_id(), "data"),
            #         inputs={
            #             'inputs':self.parse_options_inputs(),
            #             'states':self.parse_options_states()
            #         },
            #     )
            #     def update_options_func(inputs,states):
            #         if self.option_update_func is not None:
            #             r= self.option_update_func(inputs,states)
            #             print(r)
            #             return {
            #                 'options':r
            #             }
            #         return {
            #             'options':[]
            #         }

    def layout(self):
            # print(self.id())
            return [
                dcc.Dropdown(id=self.id(), multi=self.multi,options = self.options),
                dcc.Store(id=self.store_id(), storage_type='local'),
            ]
