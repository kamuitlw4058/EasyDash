
import sys
import requests
import pandas as pd
from easy_dash.app import EasyApp
# sys.path.append("../../")
# print(sys.path)

from easy_dash.model.options import OptionModelParams,Option
from easy_dash.page.auto_detail_page import AutoDetailPage


def update_func(params):
    return {'test':'test'}

def option_update_func(inputs,states):
    print(f'inputs:{inputs}')
    print(f'states:{states}')
    return [
                                    {'label': 'New York City', 'value': 'New York City'},
                                    {'label': 'San Francisco', 'value': 'San Francisco'},
                                    {'label': 'test', 'value': 'test'},
                                ]

detail_page= AutoDetailPage('procurement','detail_page',
                            module_title='采购',
                            page_title="详情查询",
                            update_func=update_func,
                            update_params={
                                'style_key':Option(option_update_func=option_update_func,options = [
                                    {'label': 'New York City', 'value': 'New York City'},
                                    {'label': 'San Francisco', 'value': 'San Francisco'},
                                ],id='style_option'),
                                },
                            
                            )

