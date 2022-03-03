from sched import scheduler
import requests
import pandas as pd
import json
from easy_dash.app import EasyApp
from easy_dash.page.page import Page
from easy_dash.page.db_page import DBTablePage
from easy_dash.page.auto_detail_page import AutoDetailPage

from easy_dash.utils.engine import conver_python_sql
from  sqlalchemy import create_engine

def update_func(params):
    d = params
    r = requests.post('http://route-log-api.51xpx.com/order_route_detail',json=d)
    return r.json()['data']

def update_list_func(params):
    d = params
    r = requests.post('http://route-log-api.51xpx.com/get_log_list',json=d)
    return r.json()['data']    


def get_log_detail(params):
    request_id = params.get('request_id',None)
    if request_id is not None:
        sql = f"""select * from iwn_route_work_log where request_id = '{request_id}'"""
        engine = create_engine('mysql+pymysql://xpx_data_only:8C5bWCLkDW@rm-bp10h91kf7w6i19k0ko.mysql.rds.aliyuncs.com:3306/xpx_data')
        df = pd.read_sql(conver_python_sql(sql),engine)
        if df is not None and len(df) > 0:
            order_route_log = df.to_dict('records')[0]
            order_info = {}
            order_sn =  order_route_log['order_sn']

            order_info["request_id"] = request_id
            order_info["order_sn"] = order_sn

            param_content =  json.loads(order_route_log['param_content'])
            print(param_content)

            order_skus_df = pd.DataFrame(param_content['order']['skus'])
            order_skus_df = order_skus_df[['goods_id','goods_attr_id','goods_name','attr_value','weight','volume','count']]
            order_info['订单需求'] = order_skus_df

            supply_info = {}
            # supply_items = []
            # supply_list = param_content['supply']
            # for store in supply_list:
            #     store_id = store['store_id']
            #     store_name = store['store_name']
            #     supply_skus = store['skus']
            #     for supply_item in supply_skus:
            #         goods_attr_id = supply_item['goods_attr_id']
            #         nums = supply_item['nums']
            #         supply_items.append({
            #             'store_id':store_id,
            #             'store_name':store_name,
            #             'goods_attr_id':goods_attr_id,
            #             '库存':nums,
            #         })
            # supply_info['库存信息'] = pd.DataFrame(supply_items)

            process_param_content =  order_route_log['process_param_content']
            if process_param_content is not None:
                process_param_content =  json.loads(order_route_log['process_param_content'])
                supply_store_info ={}
                print(process_param_content)
                for store in  process_param_content['supply']:
                    store_name = store['store_name']
                    store_id = store['store_id']
                    delivery_distance = store['delivery_distance']
                    delivery_duration = store['delivery_duration']
                    store_type = store['store_type']
                    floor_time = store.get('floor_time',0)

                    sharing_truck_delivery  = store['sharing_truck_delivery']
                    sharing_truck_delivery_list = []
                    for delivery_cost in sharing_truck_delivery:
                        weight_range = delivery_cost['weight_range']
                        truck_type = delivery_cost['truck_type']
                        point = delivery_cost['point']
                        cost = delivery_cost['cost']
                        sharing_truck_delivery_list.append({
                            '重量起始':weight_range[0],
                            '重量结束':weight_range[1],
                            '车型':truck_type,
                            '点位数':point,
                            '成本':cost,
                        })
                    
                    supply_skus = store['skus']
                    schedule_period = 0
                    supply_items =[]
                    for supply_item in supply_skus:
                        sku_id = supply_item['sku_id']
                        nums = supply_item['nums']
                        schedule_period = supply_item['time']['调度时间']
                        storage_cost = supply_item['cost']['存储成本']
                        purchase_cost = supply_item['cost']['采购成本']

                        supply_items.append({
                            'goods_attr_id':sku_id,
                            '采购成本':purchase_cost,
                            '仓储成本':storage_cost,
                            '库存':nums,
                        })

                    supply_store_info[store_name] = {
                        "store_id": store_id,
                        "配送距离": delivery_distance,
                        "配送时效": delivery_duration,
                        "搬楼时效": floor_time,
                        "仓库类型": store_type,
                        "配送成本": pd.DataFrame(sharing_truck_delivery_list),
                        "商品成本": pd.DataFrame(supply_items)
                    }
                
                supply_info['仓库信息'] = supply_store_info

            return {
                '订单信息':order_info,
                '供应信息':supply_info
            }


log_list_page= AutoDetailPage('order_route_algo_log','log_list',
                            module_title='智能路由日志',
                            page_title="日志列表", 
                            update_func=update_list_func,
                            update_params={
                                "page":1,
                                "limit":10,
                                "order_sn":None
                            })

detail_page= AutoDetailPage('order_route_algo_log','detail_page',
                            module_title='智能路由日志',
                            page_title="日志详细",
                            update_func=update_func,
                            update_params={
                                "request_id":'a09a635a7289bc4e38c06fef566dfd1e',
                                "data":{"test":"test"}
                                }
                            )

detail_page_v2= AutoDetailPage('order_route_algo_log','detail_page_v2',
                            module_title='智能路由日志',
                            page_title="日志详细v2",
                            update_func=get_log_detail,
                            update_params={
                                "request_id":'a09a635a7289bc4e38c06fef566dfd1e',
                                }
                            )
