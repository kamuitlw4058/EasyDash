import pandas as pd

from easy_dash.page.page import Page
from easy_dash.app import * 





class DBTablePage(Page):
    def __init__(self, module_name, page_name, sql,module_title=None, page_title=None):
        super().__init__(module_name, page_name, module_title, page_title)
        self.sql = sql


    def init_callback(self,app=None):
        # print('init callback')
        if app is not None:
            @app.callback(
                Output(f"{self.page_key()}-collapse", "is_open"),
                [Input(f"{self.page_key()}-collapse-button", "n_clicks")],
                [State(f"{self.page_key()}-collapse", "is_open")],
            )
            def toggle_collapse(n, is_open):
                if n:
                    return not is_open
                return is_open


    def layout(self):
        engine = create_engine('mysql+pymysql://xpx_data_only:8C5bWCLkDW@rm-bp10h91kf7w6i19k0ko.mysql.rds.aliyuncs.com:3306/xpx_data')
        df = pd.read_sql(conver_python_sql(self.sql),engine)

        return [
            dcc.Store(id='local', storage_type='local'),
            dbc.Row([dbc.Col(
            dbc.Button(
                "编辑sql",
                id=f"{self.page_key()}-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),width=1),
            dbc.Col(
            dbc.Collapse(
                 dcc.Textarea(
                    id=f"{self.page_key()}-collapse-textarea",
                    value = self.sql,
                    style={'width': '100%', 'height': 300},
                    ),
                id=f"{self.page_key()}-collapse",
                is_open=False,
            ))],className="g-0"),
            dbc.Row(dbc.Col(
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
                    page_size= 30,
                ),
            ))
        ]
