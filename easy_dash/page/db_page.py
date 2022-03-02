import pandas as pd

from easy_dash.page.page import Page
from easy_dash.app import * 
from easy_dash.utils.engine import conver_python_sql
from  sqlalchemy import create_engine


DBTABLE_STYLE = {
    'padding':'0rem',
     "top": 0,
    "left": 0,
    "bottom": 0,
    "right":0,
}

class DBTablePage(Page):
    def __init__(self, module_name, page_name,sql):
        super().__init__(module_name, page_name)
        self.sql = sql

    def layout(self):
        engine = create_engine('mysql+pymysql://xpx_data_only:8C5bWCLkDW@rm-bp10h91kf7w6i19k0ko.mysql.rds.aliyuncs.com:3306/xpx_data')
        df = pd.read_sql(conver_python_sql(self.sql),engine)
        # return dbc.Container([
        #     dbc.Row(dbc.Label('Click a cell in the table:')),
        #     dbc.Row(dash_table.DataTable(data=df.to_dict('records'),columns=[{"name": i, "id": i} for i in df.columns]),style = DBTABLE_STYLE),
        # ],style = DBTABLE_STYLE
        # )
        return [
            dbc.Label('Click a cell in the table:'),
            dbc.Col(
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'textAlign': 'left',
                        # 'backgroundColor': 'rgb(210, 210, 210)',
                        # 'color': 'black',
                        'fontWeight': 'bold'
                    },
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                ),
                width={"size": 10,  "offset": 1},
            )
        ]
