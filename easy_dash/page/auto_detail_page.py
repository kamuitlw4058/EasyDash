import pandas as pd
import json

from  easy_dash.model.map import MapModelParams,MapModel
from easy_dash.page.page import Page
from easy_dash.app import * 


class AutoDetailPage(Page):
    def __init__(self, module_name, page_name, update_func=None,update_params:dict=None, context=None,module_title=None, page_title=None):
        super().__init__(module_name, page_name, module_title, page_title)
        self.context = context
        self.update_func = update_func
        self.update_params = update_params
        self.update_params_type = {}
        self.update_params_index = {}
        self.update_params_inverted_index = {}
        if update_params is not None:
            for k,v in self.update_params.items():
                if isinstance(v,dict) or isinstance(v,list):
                    self.update_params_type[k] = 'json'
                elif isinstance(v,int):
                    self.update_params_type[k] = 'int'
                elif isinstance(v,float):
                    self.update_params_type[k] = 'float'
                elif isinstance(v,MapModelParams):
                    self.update_params_type[k] = 'map'
                else:
                    self.update_params_type[k] = 'value'
            for (i, value) in enumerate(list(self.update_params.keys())):
                self.update_params_inverted_index[i] = value
                self.update_params_index[value] = i

    
    def button_id(self):
        return f"{self.page_key()}-update-button"
    
    def params_input_id(self):
        return f"{self.page_key()}-update-params-input"
    
    def params_output_id(self):
        return f"{self.page_key()}-update-params-output"

    def params_index2key(self,index):
        return self.update_params_inverted_index.get(index,None)
    
    def params_key2index(self,k):
        return self.update_params_index.get(k,None)


    def init_callback(self,app=None):
        # print('init callback')
        if app is not None and self.update_func is not None:
            @app.callback(
                Output(self.page_key(), "children"),
                [Input(self.button_id(), "n_clicks")],
                [State(self.page_key(), "children")],
                running=[
                    (Output(self.button_id(), "disabled"), True, False),
                ],
            )
            def update_page(n, old_page):
                if n:
                    r =  self.update_func(self.update_params)
                    self.context = r
                    return self.detail_page()
                return old_page

            
            @app.callback(
                Output(self.params_output_id(), 'children'),
                Input({'type': self.params_input_id(), 'index': ALL}, 'value')
            )
            def params_result(values):
                for (i, value) in enumerate(values):
                    k = self.update_params_inverted_index[i]
                    value_type = self.update_params_type.get(k,'value')
                    if value_type == 'value':
                        if value is None or  len(value) == 0:
                            self.update_params[k] = None
                        else:
                            self.update_params[k] = value
                    elif value_type == 'int':
                        self.update_params[k] = int(value)
                    elif value_type == 'float':
                        self.update_params[k] = float(value)
                    elif value_type == 'map':
                        self.update_params[k] = 'map render'
                    else:
                        self.update_params[k] = json.loads(value)

                return json.dumps(self.update_params,ensure_ascii=False)

    def auto_context(self,ret_list:list,context,layer=0):
        h_dict = {
            0:html.H1,
            1:html.H2,
            2:html.H3,
            3:html.H4,
            4:html.H5,
            5:html.H6,
            # 6:html.H7,
        }
        # html.H1("Example heading")
        if isinstance(context,dict):
            for k,v in context.items():
                if not isinstance(v,str) and not  isinstance(v,float) and not isinstance(v,int):
                    h =  h_dict.get(layer)
                    ret_list.append(h(k))
                    self.auto_context(ret_list,v,layer=layer +1)
                else:
                    ret_list.append(dbc.Row([
                            dbc.Label(k,width=2),
                            dbc.Col(dbc.Input(type="text", value=v, disabled=True),width=5)
                        ],
                    ))
                if layer == 0:
                    ret_list.append(html.Hr())
        elif isinstance(context,list):
            guess_table = True
            for row in context:
                if isinstance(row,dict):
                    for k,v in row.items():
                        if isinstance(v,dict) or isinstance(v,list):
                            guess_table = False
                            break
                else:
                    guess_table = False
                    break
            
            if guess_table:
                df =  pd.DataFrame(context)
                ret_list.append(
                        dbc.Row(dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{"name": i, "id": i} for i in df.columns],
                            style_cell={'textAlign': 'left'},
                            style_header={
                                'textAlign': 'left',
                                'fontWeight': 'bold'
                            },
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                        )
                    )
                )
            else:
                for row in context:
                    self.auto_context(ret_list,row,layer=layer +1)
        elif isinstance(context,pd.DataFrame):
            df = context
            ret_list.append(
                    dbc.Row(dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df.columns],
                        style_cell={'textAlign': 'left'},
                        style_header={
                            'textAlign': 'left',
                            'fontWeight': 'bold'
                        },
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        column_selectable="single",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                    )
                )
            )
        elif isinstance(context,MapModelParams):
            ret_list.append(MapModel(context).layout())


    def detail_page(self):
        ret = []
        if self.update_func is not None:
            input_row = []
            input_row.append(
                dbc.Col(
                    dbc.Button(
                    "更新数据",
                    id=self.button_id(),
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                    ),
                    width=1
                )
            )
            if self.update_params is not None:
                input_params_row = []
                for k,v in self.update_params.items():
                    if self.update_params_type.get(k,'value') not in ('map', 'value'):
                        value = json.dumps(v)
                    else:
                        value = v

                    input_params_row.append(dbc.Row([
                                dbc.Label(k,width=2),
                                dbc.Col(dbc.Input(type="text", value=value,id={
                                    "type":self.params_input_id(),
                                    "index":self.params_key2index(k)
                                }),width=5)

                            ],
                        ))
                input_params_row.append(dbc.Row([
                         dbc.Label("最终参数",width=2),
                        dbc.Col(html.Div(id=self.params_output_id()),width=5)
                    ]))
            input_row.append(dbc.Col(input_params_row))
            ret.append(dbc.Row(input_row))
            ret.append(html.Hr())

        self.auto_context(ret,self.context)
        
        return ret


    def layout(self):
        return [html.Div(self.detail_page(),id=self.page_key()
        )] 