from easy_dash.app import *

class Page():
    def __init__(self,module_name,page_name,module_title=None,page_title=None):
        self.module_name = module_name
        self.page_name = page_name
        self.module_title = module_title
        self.page_title = page_title

    def page_key(self):
        return f'{self.module_name}-{self.page_name}'


    def init_callback(self,app=None):
        pass

    def layout(self,app=None):
        return html.P(f"This is the content of the {self.page_name} page!")