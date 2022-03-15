
import sys
import requests
import pandas as pd
from easy_dash.app import EasyApp
# sys.path.append("../../")
# print(sys.path)


from easy_dash.model.options import OptionModelParams

from easy_dash.page.auto_detail_page import AutoDetailPage


def update_func(params):
    

    return {'test':'test'}

def option_update_func(inputs,states):
    print(f'inputs:{inputs}')
    print(f'states:{states}')
    if len(inputs.values()) > 0:
        print(inputs.values())
        v = list(inputs.values())[0]
        return [{'label':i, 'value':i} for i in  v.split(',')]
    return [{'label': 'San Francisco', 'value': 'San Francisco'}]

detail_page= AutoDetailPage('test','test_options',
                            module_title='测试',
                            page_title="测试 选项框",
                            update_func=update_func,
                            update_params={
                                "request_id":'a09a635a7289bc4e38c06fef566dfd1e',
                                "data":{"test":"test"},
                                'options':OptionModelParams(option_update_func=option_update_func,options = [
                                    {'label': 'New York City', 'value': 'New York City'},
                                    {'label': 'San Francisco', 'value': 'San Francisco'},
                                ]),
                                },
                            depend={
                                'options':['request_id']
                            }
                            )

app = EasyApp(pages=[
    detail_page,
])
app.normal()
app.run()