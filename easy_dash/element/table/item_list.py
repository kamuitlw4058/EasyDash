import pandas as pd
import json

from easy_dash.element.base import Element
from easy_dash.element.params.dict_params import DictParams
from easy_dash.app import * 


class ItemList(Element):
    def __init__(self,get_func=None,data = None):
        super().__init__()
        self.column_names = []
        self.columns = []
        self.data = []
        self.dict_params = None
        if data is not None:
            if isinstance(data,pd.DataFrame):
                self.data = data.to_dict('records')
                self.column_names = data.columns
                self.columns = [{"name": i, "id": i} for i in data.columns]
                rows = data.to_dict('records')
                if len(rows)> 0:
                    row = rows[0]
                    self.dict_params = self.build_row_detail(row)
            elif isinstance(data,list):
                self.data = data
                if len(data) > 0:
                    row = data[0]
                    self.dict_params = self.build_row_detail(row)
                    if isinstance(row,dict):
                        self.column_names = list(row.keys())
                        self.columns =  [{"name": i, "id": i} for i in list(row.keys())]
            else:
                raise Exception(f'unknown data type {type(data)}. want df or list')

    def build_row_detail(self,row=None):
        return DictParams(row,id=self.dict_params_id(),buttons={
            '更新':lambda x:True,
            '删除':lambda x:True,
        })

    def init_callback(self,app=None):
        if app is not None :
            @app.callback(
                Output(self.store_id(), 'data'),
                Input(self.table_id(), 'active_cell'),
                State(self.table_id(),'data'),
                State(self.table_id(),'page_current'),
                State(self.table_id(),'page_size'),
                State(self.modal_id(),'is_open')
            )
            def update_store(active_cell,data,page_current,page_size,is_open):
                if page_current is None:
                    page_current = 0
                    page_size = 0
                if active_cell is not None:
                    row_num = active_cell['row']
                    column_num = active_cell['row']
                    column_id = active_cell['column_id']
                    row_num  = page_current * page_size + row_num
                    return {
                        'active_cell':active_cell,
                        'value':data[row_num][column_id],
                        'row':data[row_num],
                        'row_num':row_num,
                        'column_num':column_num,
                        'column_id':column_id,
                        'page_current':page_current,
                        'page_size':page_size,
                        'modal_is_open':is_open,
                        'output':f'active_cell:{active_cell} value1:{data[row_num][column_id]}'
                    }
                return {
                        'active_cell':None,
                        'value':None,
                        'modal_is_open':is_open,
                        # 'row':data[row_num],
                        # 'row_num':row_num,
                        # 'column_num':column_num,
                        # 'column_id':column_id,
                        # 'page_current':page_current,
                        # 'page_size':page_size,
                        'output':"Click the table"
                    }    


            @app.callback(
                Output(self.table_out_id(), "children"),
                Input(self.store_id(), 'data'),
            )
            def update_table_out(data):
                if data is not None:
                    return data['output']
                
                return 'data is None'
                

            @app.callback(
                Output(self.modal_id(), "is_open"),
                Input(self.store_id(), 'data'),
            )
            def update_modal(data):
                if data is not None and data['active_cell'] is not None:
                    return True
                return False


            @app.callback(
                Output(self.modal_body_id(), "children"),
                Input(self.store_id(), 'data'),
            )
            def update_modal_body(data):
                if data is not None and data['active_cell'] is not None:
                    row = data['row']
                    if self.dict_params is not None:
                        self.dict_params = self.build_row_detail(row)
                        return self.dict_params.layout()
                return 'Body no data'
            
            if self.dict_params is not None:
                self.dict_params.init_callback(app=app)


    def table_id(self):
        return f'{self.id()}-table' 

    def table_out_id(self):
        return f'{self.id()}-table-out' 
    
    def modal_id(self):
        return f'{self.id()}-modal'

    def modal_body_id(self):
        return f'{self.id()}-modal-body'
    
    def dict_params_id(self):
        return f'{self.id()}-dict-params'

    def build_table(self):
        table = dash_table.DataTable(
        id=self.table_id(),
        columns=self.columns,
        data=self.data,
        sort_action='native',
        filter_action='native',
        # row_selectable= 'single',
        page_action="native",
        page_current= 0,
        page_size= 30,
        # editable=True
    )
        return table
    
    def bulid_modal(self):
        return dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Header")),
                    dbc.ModalBody("This is the content of the modal",id=self.modal_body_id()),
                    # dbc.ModalFooter(
                    # ),
                ],
                id=self.modal_id(),
                is_open=False,
                size="xl",
                centered=True
                )



    def layout(self):
        ret = html.Div(
            [
                self.build_table(),
                html.Div(id=self.table_out_id()),
                self.bulid_modal(),
                dcc.Store(id=self.store_id(), storage_type='local'),
            ],
            id=self.id()
        )
        return ret