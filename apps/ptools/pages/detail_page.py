
import sys
import requests
import pandas as pd
from easy_dash.app import EasyApp
# sys.path.append("../../")
# print(sys.path)
from engine import get_engine

from easy_dash.model.options import OptionModelParams,Option
from easy_dash.page.auto_detail_page import AutoDetailPage


def update_func(params):
    return {'test':'test'}

def option_update_func(inputs,states):
    print(f'inputs:{inputs}')
    print(f'states:{states}')
    # engine = get_engine()
    # engine = 
    df =  pd.read_excel('data/data.xlsx')
    style = list(set(df['STYLE']))
    return [ {'label': i, 'value':i} for i in style ]

    # return [i[''] for i in style ]

detail_page= AutoDetailPage('procurement','detail_page',
                            module_title='采购',
                            page_title="详情查询",
                            update_func=update_func,
                            update_params={
                                'style':Option(option_update_func=option_update_func,options = [
                                   ],id='style_option'),
                                },
                            
                            )

