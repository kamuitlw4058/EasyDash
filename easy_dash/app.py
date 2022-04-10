
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import Output,Input,State
from dash import dash_table
from dash import ALL,MATCH

import dash_dangerously_set_inner_html as dhtml

import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache

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

HEADER_STYLE = {
    "position": "fixed", 
    "top": 0,
    "left": 0,
    # "bottom": 0,
    "right":0,
    "margin-left": "18rem",
    # "padding": "1rem 0rem 1rem 1rem",
    "padding": "0rem",
    'overflowY': 'auto'
}

CONTENT_STYLE = {
    "margin-top": "3rem",
    "margin-left": "18rem",
    "margin-right": "0rem",
    "padding": "1rem",
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
"padding": "0rem 0rem 0rem 1rem",
}



PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"



class EasyApp():

    def __init__(self,title='EasyApp',pages=None):
        chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors


        # self.cache = diskcache.Cache("./cache")
        # self.long_callback_manager = DiskcacheLongCallbackManager(self.cache)
        self.app = dash.Dash(title=title,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                external_scripts=[chroma],
                # long_callback_manager= self.long_callback_manager
                )

        self.app.config.suppress_callback_exceptions = True
        self.pages = pages
        self.page_dict = {}
        if pages is not None:
            for page in pages:
                module_name = page.module_name
                page_name = page.page_name
                self.page_dict[f'{module_name}/{page_name}'] = page
        self.title = title
    

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
                    ret.extend(page_layout)
                else:
                    ret.append(page.layout())

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
            return  html.Div(ret)
        
        for page_path,page in self.page_dict.items():
            page.init_callback(app=self.app)

    def run(self):
        self.app.run_server(host='0.0.0.0')


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
            module_page_titles = []
            module_title = module_name
            for page in module_pages:
                page_title = page.page_title if page.page_title is not None else page.page_name
                module_title = page.module_title if page.module_title is not None else page.module_name
                module_page_titles.append(dbc.NavLink(page_title, href=f"/{page.module_name}/{page.page_name}", active="exact"))
                
            # module_page_titles = [dbc.NavLink(i.page_name, href=f"/{i.module_name}/{i.page_name}", active="exact") for i in  module_pages]
            module_accordion_list.append(
                dbc.AccordionItem(
                    module_page_titles,
                    title=module_title,
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
                                        dbc.Col(dbc.NavbarBrand(self.title, className="ms-2")),
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
    
    
    def content(self):
        return  html.Div([
            html.Div(
                    dbc.Navbar(
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
                ),style= HEADER_STYLE),
             html.Div(dbc.Row(html.Div(id='page-content')),style=CONTENT_STYLE)])
        


    def normal(self,pages=None):
        self.init_callback()
        self.app.layout = html.Div([
            dcc.Location(id="url"),
            self.side_bar(),
            self.content()
        ])