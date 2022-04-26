
from unicodedata import name
from easy_dash.app import *
from easy_dash.element.form.key_value import ValueElement 


class FormElement(ValueElement):
    def __init__(self, value,,id=None ):
        super().__init__(value=value,id=id)
        self.name = display_name 

    def init_callback(self, app=None):
        return super().init_callback(app)

    def layout(self, app=None):
        return html.P(f"This is the content of {type(self)} element. name:{self.name} value:{self.value} [{self.id_string()}]")
            