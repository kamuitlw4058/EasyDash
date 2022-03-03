import pandas as pd

from easy_dash.page.page import Page
from easy_dash.app import * 


class DetailPage(Page):
    def __init__(self, module_name, page_name,update_func=None, context_list=None):
        super().__init__(module_name, page_name)
        self.context_list = context_list
        self.update_func = update_func
    
    def button_id(self):
        return f"{self.page_key()}-update-button"

    def init_callback(self,app=None):
        # print('init callback')
        if app is not None and self.update_func is not None:
            @app.callback(
                Output(self.page_key(), "children"),
                [Input(self.button_id(), "n_clicks")],
                [State(self.page_key(), "children")]
            )
            def update_page(n, old_page):
                print("update-page")
                if n:
                    return self.detail_page()
                return old_page


    def detail_page(self):
        ret = []
        if self.update_func is not None:
            ret.append(
                # dbc.Row(
                dbc.Button(
                "更新数据",
                id=self.button_id(),
                className="mb-3",
                color="primary",
                n_clicks=0,
                )
            )
            # )
        
        if self.context_list is not None:
            for context in self.context_list:
                if isinstance(context,str):
                    ret.append(dbc.Row(context))
                elif isinstance(context,pd.DataFrame):
                    ret.append(dbc.Row(dash_table.DataTable(
                        data=context.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in context.columns],
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
                    )))
        return ret


    def layout(self):
        return [html.Div(self.detail_page(),id=self.page_key()
        )] 