import pandas as pd
import json

from easy_dash.element.base import Element
# from  easy_dash.model.map import MapModelParams,MapModel
# from easy_dash.model.options import OptionModelParams,Option
# from easy_dash.page.page import Page
from easy_dash.app import * 


class DictParams(Element):
    def __init__(self,  params,buttons=None, update_func=None, content=None,id=None):
        super().__init__(id=id)
        self.content = content
        self.update_func = update_func
        self.init_params(params)
        self.init_buttons(buttons)
            
    def content_id(self):
        return f'{self.id()}-content'

    def sub_id(self,sub_key):
        return f'{self.id()}-{sub_key}'

    def params_output_id(self):
        return f"{self.id()}-update-params-output"
    
    def update_params(self,key,value):
        self.params[key] = value

    def build_params_dict(self,values):
        ret = {}
        for k,value in values.items():
            opt_key = self.params_opt_key[k]
            value_type = self.params_type.get(k,'value')
            if value_type == 'value':
                if value is None or  len(value) == 0:
                    ret[opt_key] = None
                else:
                    ret[opt_key] = value
            elif value_type == 'int':
                ret[opt_key] = int(value)
            elif value_type == 'float':
                ret[opt_key] = float(value)
            elif value_type == 'element':
                ret[opt_key] = value
            else:
                ret[opt_key] = json.loads(value)
        return ret
    
    def button_id(self,key=None):
        button_key = f'{self.id()}-button'
        if key is not None:
            button_key = f'{button_key}-{key}'
        return button_key

    def button_output_id(self,key=None):
        button_key = f'{self.id()}-buttonoutput'
        if key is not None:
            button_key = f'{button_key}-{key}'
        return button_key

    def init_buttons(self,buttons):
        self.buttons= buttons


    def init_params(self,params):
        self.params = params
        self.params_type = {}
        self.params_opt_key = {}
        self.params_obj_dict ={}
        if self.params is not None:
            for k,v in self.params.items():
                print(f'k:{k} v:{v}')
                if isinstance(v,dict) or isinstance(v,list):
                    self.params_type[k] = 'json'
                elif isinstance(v,int):
                    self.params_type[k] = 'int'
                elif isinstance(v,float):
                    self.params_type[k] = 'float'
                elif isinstance(v,Element):
                    self.params_type[k] = 'element'
                else:
                    self.params_type[k] = 'value'
        
        for k,v in self.params.items():
            if isinstance(v,Element):
                self.params_opt_key[v.id()] = k
                self.params_obj_dict[k] = (v.layout(),v)
            else:
                update_params_type =  self.params_type.get(k,'value') 
                if update_params_type not in ('map', 'option','value'):
                    value = json.dumps(v)
                else:
                    value = v

                self.params_opt_key[self.sub_id(k)] = k
                self.params_obj_dict[k] = (dbc.Input(type="text", value=value,id=self.sub_id(k)),None)

    def init_callback(self,app=None):
        if app is not None :
            inputs = {}
            for k,v in self.params.items():
                if isinstance(v,Element):
                    inputs[v.id()] = Input(v.id(),'value')
                else:
                    inputs[self.sub_id(k)] = Input(self.sub_id(k),'value')

            @app.callback(
                output = Output(self.params_output_id(), 'children') ,
                inputs = {'values': inputs}
            )
            def params_result(values):
                ret = self.build_params_dict(values)
                return   json.dumps(ret,ensure_ascii=False)

            @app.callback(
                output = Output(self.content_id(), 'children') ,
                inputs = {'values': inputs}
            )
            def update_content(values):
                ret = self.build_params_dict(values)
                if self.update_func is not None:
                    self.content = self.update_func(ret)
                content = self.build_content()
                return content

            if self.buttons is not None:

                button_inputs = {}
                for k,v in self.buttons.items():
                    button_inputs[self.button_id(k)] = Input(self.button_id(k),'n_clicks')
                    @app.callback(
                        Output(self.button_output_id(k), "children"),
                        Input(self.button_id(k), 'n_clicks'),
                    )
                    def update_button_func(values):
                       return values

            
            for k,v in self.params.items():
                if isinstance(v,Element):
                    v.init_callback(app=app)
                
            if self.content and isinstance(self.content,Element):
                self.content.init_callback(app=app)
            
    def build_content(self):
        content = []
        if self.content is not None:
            if isinstance(self.content,Element):
                context_layout = self.content.layout()
                content = context_layout
            else:
                content = self.content

        return content


    def auto_content(self):
        ret = []
        if self.params is not None:
            for k,v in self.params.items():
                layout,model = self.params_obj_dict[k]
                ret.append(dbc.Row([
                            dbc.Label(k,width=2),
                            dbc.Col(layout,width=5)

                        ],
                    ))
            ret.append(dbc.Row([
                        dbc.Label("最终参数",width=2),
                    dbc.Col(html.Div(id=self.params_output_id()),width=5)
                ]))
        
        if self.update_func is not None or self.buttons is not None:
            ret.append(html.Hr())

        
        if self.update_func is not None:
            content = self.build_content()
            ret.append( html.Div(content,id=self.content_id()))
        
        if self.buttons is not None:
            if len(self.buttons) <=3:
                button_list = []
                button_output_list =[]
                for k,v in self.buttons.items():
                    button_list.append(
                        dbc.Col(
                            dbc.Button(k, color="primary", className="me-1",id=self.button_id(k))
                        ,width="auto")
                    )
                    button_output_list.append(
                        dbc.Col(
                            html.Div([],id=self.button_output_id(k))
                        ,width="auto")
                    )
                ret.append(dbc.Row(button_list,className="g-0"))
                ret.append(dbc.Row(button_output_list))
        return ret


    def layout(self):
        ret = html.Div(self.auto_content(),id=self.id()
        )
        return ret