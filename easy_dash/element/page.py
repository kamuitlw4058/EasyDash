from email import contentmanager
from tkinter import E
from easy_dash.element.base import Element
from easy_dash.app import * 


class Page(Element):
    def __init__(self,module_name,page_name,content=None,module_title=None,page_title=None,id=None):
        super().__init__(id=id)
        self.module_name = module_name
        self.page_name = page_name
        self.module_title = module_title
        self.page_title = page_title
        self.content =content
        self.display_content = None

    
    def init_content(self,app=None):
        display_content = []
        print(self.content)
        if isinstance(self.content,list):
            for i in self.content:
                if isinstance(i,Element):
                    i.init_callback(app=app)
                    display_content.append(i.layout())
        elif isinstance(self.content,Element):
            self.content.init_callback(app=app)
            display_content.append(self.content.layout())
        self.display_content = display_content
        return display_content

    def page_key(self):
        return f'{self.module_name}-{self.page_name}'

    def init_callback(self,app=None):
        self.init_content(app=app)

    def layout(self,app=None):
        if self.display_content is not None:
            return [html.Div(self.display_content,id=self.page_key()
        )] 
        return html.P(f"This is the content of the {self.page_name} page!")