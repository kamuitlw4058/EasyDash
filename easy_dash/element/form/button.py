from easy_dash.element.base import Element
from easy_dash.app import * 


class CollapseP(Element):
    def __init__(self,children, id=None):
        super().__init__(id=id)
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
                

    def layout(self, app=None):
        d = {
            'data-bs-toggle':'collapse',
            'data-bs-target':'#test_menu',
            'data-aria-expanded':False,
        }
        return html.Div([
            html.Button('Primary',  className='btn btn-toggle align-items-center rounded collapsed',id=self.id(),**d),
            dbc.Collapse(
                dbc.ListGroup(
                    [
                        html.Li(
                            html.A('overview', href='#',className='link-dark rounded')
                        ),
                    ],
                    class_name='btn-toggle-nav list-unstyled fw-normal pb-1 small'
                ),
                id=self.collapse_id(),
                is_open=True,
            ),
            ])
        # return   dbc.Button("Primary", color="",contextMenu='test contextmenu', class_name='btn btn-toggle align-items-center rounded collapsed')
            