import pandas as pd
import json

from easy_dash.element.base import Element
# from  easy_dash.model.map import MapModelParams,MapModel
# from easy_dash.model.options import OptionModelParams,Option
# from easy_dash.page.page import Page
from easy_dash.app import * 


class DictParams(Element):
    def __init__(self,  params,update_func=None, content=None):
        super().__init__()
        self.content = content
        self.update_func = update_func
        self.params = params
        self.params_type = {}
        self.params_opt_key = {}
        self.params_obj_dict ={}
        if params is not None:
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
                # elif isinstance(v,MapModelParams):
                #     self.update_params_type[k] = 'map'
                # elif isinstance(v,OptionModelParams):
                #     self.update_params_type[k] = 'option'
                else:
                    self.params_type[k] = 'value'
                # print(f'k:{k} rv:{self.update_params_type[k]}')
            
    def content_id(self):
        return f'{self.id()}-content'

    def sub_id(self,sub_key):
        return f'{self.id()}-{sub_key}'

    def params_output_id(self):
        return f"{self.id()}-update-params-output"


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

    def init_callback(self,app=None):
        # print('init callback')
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
                print(content)
                return content

            
            for k,v in self.params.items():
                if isinstance(v,Element):
                    # option = Option(v,id = self.sub_id(k))
                    v.init_callback(app=app)
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
        ret.append(html.Hr())

        content = self.build_content()
        ret.append( html.Div(content,id=self.content_id()))
        # print(ret)
        return ret


    def layout(self):
        ret = html.Div(self.auto_content(),id=self.id()
        )
        return ret