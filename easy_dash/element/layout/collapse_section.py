from readline import insert_text
from easy_dash.element.base import Element
from easy_dash.element.layout.rows import RowsElement
from easy_dash.element.form.key_value import KeyValueElement
from easy_dash.app import * 


class CollapseSection(KeyValueElement):
    def __init__(self,key, value, level=0, display_name=None, editabled=True, id=None):
        super().__init__(key=key,value=value,display_name=display_name,editabled=editabled, id=id)
        self.level = level
    
    def set_level(self,level):
        self.level = level

    def collapse_id(self):
        return f'{self.id()}-collapse'

    def init_callback(self, app=None):
        if app is not None:
            @app.callback(
                Output(self.collapse_id(), "is_open"),
                [Input(self.id(), "n_clicks")],
                [State(self.collapse_id(), "is_open")],
            )
            def toggle_collapse(n, is_open):
                if n:
                    return not is_open
                return is_open

            @app.callback(
                Output(self.id(), "data-aria-expanded"),
                [Input(self.id(), "n_clicks")],
                [State(self.collapse_id(), "is_open")],
            )
            def toggle_collapse(n, is_open):
                return not is_open

            if isinstance(self.value,Element):
                self.value.init_callback(app=app)
            elif isinstance(self.value,list):
                for row in self.value:
                    if isinstance(row,Element):
                        row.init_callback(app=app)
                        if isinstance(row,CollapseSection):
                            row.set_level(self.level +1)


       

    def layout(self, app=None):
        d = {
            'data-bs-toggle':'collapse',
            'data-bs-target':'#test_menu',
            'data-aria-expanded':False,
        }
        ret = []
        if isinstance(self.value,Element):
            ret.append(self.value.layout())
        elif isinstance(self.value,list):
            # print(Rows(self.value).layout())
            ret.append(RowsElement(self.value).layout())
        else:
            raise Exception(f'unknown value type:{type(self.value)},need <Element>')


        if self.level == 0:
            button_size = f'btn-lg'
        elif self.level == 1:
            button_size = f'btn-md'
        elif self.level >= 2:
            button_size = f'btn-sm'
            
        
        return html.Div([
            html.Button(self.display_name, className=f'btn {button_size} btn-toggle align-items-center rounded collapsed',id=self.id(),**d),
                dbc.Collapse(
                    ret,
                    id=self.collapse_id(),
                    is_open=True,
                ),
            ])
            