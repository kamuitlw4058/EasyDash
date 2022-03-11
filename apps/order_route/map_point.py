import requests
import pandas as pd
import json
from easy_dash.app import EasyApp
from easy_dash.page.page import Page
from easy_dash.page.db_page import DBTablePage
from easy_dash.page.auto_detail_page import AutoDetailPage

from easy_dash.utils.engine import conver_python_sql
from  sqlalchemy import create_engine
from easy_dash.model.map import MapModelParams
from easy_dash.page.map_edit import MapEditPage



def super_order_point(params):
    url = params.get('url','online')
    if url == 'online':
        url = 'mysql+pymysql://xpx_data_only:8C5bWCLkDW@rm-bp10h91kf7w6i19k0ko.mysql.rds.aliyuncs.com:3306/xpx_data'
    elif url == 'pre':
        url = 'mysql+pymysql://xpx_db:Aa112233445566@rm-bp17v62z92lrim3w2zo.mysql.rds.aliyuncs.com:3306/xpx_data'

    sql = params.get('sql',None)
    print(sql)
    eval_value= params.get('eval',None)

    # sql = f"""select param_content from iwn_route_work_log where request_id like '{keyword}%'  and result like '%超级%' limit 1000"""
    engine = create_engine(url)
    df = pd.read_sql(conver_python_sql(sql),engine)
    print(df)
    df_list = df.to_dict('records')
    l= []
    if eval_value is not None:
        for row in df_list:
            l.append( eval(eval_value))
    # print(l)
        # if eval_value
        # param_content = json.loads(i['param_content'])
        # l.append([param_content['order']['ylocal'],param_content['order']['xlocal']])
    # l = [[ [json.loads(i)['order']['ylocal'],json.loads(i)['order']['xlocal']]] for i in  pd.read_sql(conver_python_sql(sql),engine).to_dict('records')]
    return {
        '值':len(l),
        '地图':MapModelParams(
            markers=[
                [31.255256,121.207784],
                [31.181873,121.573769],
                [30.854813,120.958313]
            ],
            geojson=l,color_prop='value',vmax=4000,cluster=False)
    }

map_page= AutoDetailPage('map','map_detail',module_title='地图显示',page_title="结果分布",
    update_func=super_order_point,
    update_params={
        'url':'pre',
        'sql':"""select param_content,process_param_content from iwn_route_work_log where request_id like '0309-v5%'  and result like '%超级%' limit 1000""",
        'eval':""" { "lat":float(json.loads(row['param_content'])['order']['ylocal']),"lon":float(json.loads(row['param_content'])['order']['xlocal']),"value":float(json.loads(row['process_param_content'])['order']['weight'])}""",
        },
    context={})


edit_map_page = MapEditPage('map','map_edit',module_title='地图显示',page_title="地图编辑")