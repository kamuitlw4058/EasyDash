import pandas as pd
import json

from easy_dash.element.base import Element
from easy_dash.app import * 

class Rows(Element):
    def __init__(self,  rows,buttons=None, update_func=None, content=None,id=None):
        super().__init__(id=id)
        self.init_rows(rows)

    def init_rows(self,rows):
        self.rows = rows

    def init_callback(self, app=None):
        if app is not None:
            for row in self.rows:
                row.init_callback(app=app)

    def layout(self, app=None):
        ret = []
        for row in self.rows:
            ret.append(dbc.Row(row.layout(),class_name='mb-3'))
        return html.Div( ret,id=self.id())
            