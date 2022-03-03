import requests
import pandas as pd
from easy_dash.app import EasyApp
from easy_dash.page.page import Page
from easy_dash.page.db_page import DBTablePage
from easy_dash.page.auto_detail_page import AutoDetailPage

def update_func(params):
    d = params
    r = requests.post('http://route-log-api.51xpx.com/order_route_detail',json=d)
    return r.json()['data']

def update_list_func(params):
    d = params
    r = requests.post('http://route-log-api.51xpx.com/get_log_list',json=d)
    return r.json()['data']    

log_list_page= AutoDetailPage('order_route_algo_log','log_list',module_title='智能路由日志',page_title="日志列表", update_func=update_list_func,update_params={
    "page":1,
    "limit":10,
    "order_sn":None
})
detail_page= AutoDetailPage('order_route_algo_log','detail_page',module_title='智能路由日志',page_title="日志详细",update_func=update_func,update_params={"request_id":'a09a635a7289bc4e38c06fef566dfd1e',"data":{"test":"test"}})
