import pandas as pd
import json

from easy_dash.element.base import Element
from easy_dash.element.form.key_value import KeyValueElement
from easy_dash.element.layout.collapse_section import CollapseSection
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

    def to_json(self):
        ret = {}
        for row in self.rows:
            if isinstance(row,KeyValueElement):
                ret[row.key] = row.value
            elif isinstance(row,CollapseSection):
                ret[row.key] = row.value
                pass

    def layout(self, app=None):
        ret = []
        for row in self.rows:
            ret.append(dbc.Row(row.layout(),class_name='mb-3'))
        return html.Div( ret,id=self.id())
            