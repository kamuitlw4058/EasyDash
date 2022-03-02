
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import Output,Input,State
from dash import dash_table

import dash_dangerously_set_inner_html as dhtml

import dash_bootstrap_components as dbc

from easy_dash.utils.engine import conver_python_sql
from  sqlalchemy import create_engine

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "right":0,
    "width": "18rem",
    # "padding": "1rem 0rem 1rem 1rem",
    "padding": "0rem",
    "background-color": "#f8f9fa",
    'overflowY': 'auto'
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "0rem",
    "padding": "0rem 0rem",
}

NAVBAR_STYLE = {
    "height":"4rem",
    "padding": "0rem 0rem",
}

TOTAL_STYLE={
    "height":"100%",
        "top": 0,
    "left": 0,
    "bottom": 0,
    "right":0,
}

BREADCRUMB_TYPE = {
"padding": "0.5rem 0.5rem 0.5rem 1rem",
}

CONTENT_PAGE_STYLE = {
"padding": "0rem",
}


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"



class EasyApp():

    def __init__(self,title='EasyApp',pages=None):
        self.app = dash.Dash(title=title,
                        external_stylesheets=[dbc.themes.BOOTSTRAP]
                        )

        self.app.config.suppress_callback_exceptions = True
        self.pages = pages
        self.page_dict = {}
        if pages is not None:
            for page in pages:
                module_name = page.module_name
                page_name = page.page_name
                self.page_dict[f'{module_name}/{page_name}'] = page
    

    def init_callback(self):
        @self.app.callback(Output("page-content", "children"),
         [Input("url", "pathname")])
        def render_page_content(pathname):
            ret = []
            if pathname[0] == '/':
                pathname = pathname[1:]
            
            page =  self.page_dict.get(pathname,None)
            if page is not None:
                breadcrumb_items = []
                breadcrumb_items.append({"label": "root", "href": "/", "external_link": True,"active": True})
                breadcrumb_items.append({"label": page.module_name, "href": f"/{page.module_name}", "external_link": True})
                breadcrumb_items.append({"label": page.page_name, "href": f"/{page.module_name}/{page.page_name}", "external_link": True,"active": True})
                breadcrumb = dbc.Breadcrumb(items = breadcrumb_items,style = BREADCRUMB_TYPE)
                ret.append(dbc.Row(breadcrumb))
                page_layout = page.layout()
                if isinstance(page_layout,list):
                    page_layout = [dbc.Row(layout) for layout in page_layout]
                    ret.extend(page_layout)
                else:
                    ret.append(html.Div(page.layout(),style =CONTENT_PAGE_STYLE))
                return ret
            ret.append(
                html.Div(
                    dbc.Container(
                        [
                            html.H1("Jumbotron", className="display-3"),
                            html.P(
                                "404: Not found",
                                className="lead",
                            ),
                            html.Hr(className="my-2"),
                            html.P(
                                f"The pathname {pathname} was not recognised..."
                            ),
                        ],
                        fluid=True,
                        className="py-3",
                    ),
                className="p-3 bg-light rounded-3",
                # className = "align-items-md-stretch"
            ))
            return  html.Div(ret,style =CONTENT_PAGE_STYLE)

    def run(self):
        self.app.run_server()


    def layout(self,content):
        self.app.layout = content

    def get_titles(self):
        ret = {}
        for page in self.pages:
            module_name = page.module_name
            module =  ret.get(module_name,{})
            module_pages =  module.get('pages',[])
            module_pages.append(page)
            module['pages'] = module_pages
            ret[module_name] = module
        return ret


    def side_bar(self):
        modules = self.get_titles()
        module_accordion_list = []
        for module_name,module_dict in modules.items():
            module_pages = module_dict.get('pages',[])
            module_page_titles = [dbc.NavLink(i.page_name, href=f"/{i.module_name}/{i.page_name}", active="partial") for i in  module_pages]
            module_accordion_list.append(
                dbc.AccordionItem(
                    module_page_titles,
                    title=module_name,
                ))

        base_control = [
            dbc.Row(
                dbc.Col(
            dbc.Navbar(
                    dbc.Container(
                        [
                            html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="https://plotly.com",
                                style={"textDecoration": "none"},
                            ),

                        ]
                    ),
                    color="dark",
                    dark=True,
                )
                ),
                className= 'g-0'
            ),
            dbc.Nav(
                dbc.Accordion(module_accordion_list, start_collapsed=True),
                vertical=True,
                pills=True,
            ),
            # dbc.Accordion( module_accordion_items)
            
        ]
        return html.Div(base_control,style=SIDEBAR_STYLE)
    
    def navbar(self):
        @self.app.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        return dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                                dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                            ],
                            align="left",
                            className="g-0",
                        ),
                        href="https://plotly.com",
                        style={"textDecoration": "none"},
                    ),


                ]
            ),
            color="dark",
            dark=True,
        )

    
    def content(self):
        return  html.Div([
            dbc.Row( dbc.Navbar(
                    dbc.Container(
                        [
                            html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                    [
                                        # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                                        dbc.Col(dbc.NavbarBrand(" ", className="ms-2")),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="https://plotly.com",
                                style={"textDecoration": "none"},
                            ),

                        ]
                    ),
                    color="dark",
                    dark=True,
                )
                ),
                dbc.Row(html.Div(id='page-content')),
                
            ],style=CONTENT_STYLE)


    def normal(self,pages=None):
        if pages is None:
            pages =[]
        
        self.init_callback()

        self.app.layout = html.Div([
            dcc.Location(id="url"),
            self.side_bar(),
            self.content()
        ])