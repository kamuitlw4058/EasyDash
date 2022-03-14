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
import itertools

def update_func(params):
    d = params
    r = requests.post('http://route-log-api.51xpx.com/order_route_detail',json=d)
    return r.json()['data']

def update_list_func(params):
    d = params
    r = requests.post('http://route-log-api.51xpx.com/get_log_list',json=d)
    return r.json()['data']    


def get_log_detail(params):
    url = params.get('url','online')
    if url == 'online':
        url = 'mysql+pymysql://xpx_data_only:8C5bWCLkDW@rm-bp10h91kf7w6i19k0ko.mysql.rds.aliyuncs.com:3306/xpx_data'
    elif url == 'pre':
        url = 'mysql+pymysql://xpx_db:Aa112233445566@rm-bp17v62z92lrim3w2zo.mysql.rds.aliyuncs.com:3306/xpx_data'

    request_id = params.get('request_id',None)
    if request_id is None:
        order_sn= params.get('order_sn',None)
        request_order= params.get('request_order',None)
        if order_sn is not None:
            sql = f"""select request_id from iwn_route_work_log where order_sn = '{order_sn}' order by start_time """
            engine = create_engine(url)
            df = pd.read_sql(conver_python_sql(sql),engine).to_dict('records')

            if len(df) > request_order:
                if request_order > 0:
                    request_order = request_order -1 
                request_id = df[request_order]['request_id']

    if request_id is not None:
        sql = f"""select * from iwn_route_work_log where request_id = '{request_id}'"""
        engine = create_engine(url)
        df = pd.read_sql(conver_python_sql(sql),engine)
        if df is not None and len(df) > 0:
            order_route_log = df.to_dict('records')[0]
            order_info = {}
            order_sn =  order_route_log['order_sn']
            

            order_info["request_id"] = request_id
            order_info["order_sn"] = order_sn

            param_content =  json.loads(order_route_log['param_content'])
            address = param_content['order']['address']
            order_attach = param_content['order']['order_attach']
            order_info["地址"] = address
            order_info["业务线"] = order_attach

            order_skus_df = pd.DataFrame(param_content['order']['skus'])
            order_skus_df = order_skus_df[['sku_id','goods_name','attr_value','weight','volume','count']]
            demand_dict = {}
            skus_demand_list = order_skus_df.to_dict('records')
            for sku_demand in skus_demand_list:
                sku_id = sku_demand['sku_id']
                sku_name = sku_demand['goods_name']
                demand = sku_demand['count']
                weight = sku_demand['weight']
                demand_dict[str(sku_id)] = {
                    'weight':weight,
                    'demand':demand,
                    'name':sku_name
                }

            supply_info = {}

            process_param_content =  order_route_log['process_param_content']
            if process_param_content is not None:
                process_param_content =  json.loads(order_route_log['process_param_content'])
                order_weight = round(process_param_content['order']['weight'],3)
                remain_time = process_param_content['order']['remain_time']


                order_info['订单总重'] = order_weight
                order_info['剩余时效'] = remain_time
                supply_store_info ={}
                # print(process_param_content)
                store_name_list = []
                for store in  process_param_content['supply']:
                    store_name = store['store_name']
                    store_id = store['store_id']
                    delivery_distance = store['delivery_distance']
                    delivery_duration = store['delivery_duration']
                    store_type = store['store_type']
                    floor_time = store.get('floor_time',0)
                    store_kg_cost = 0
                    store_delivery_truck_type = ''

                    store_stock_kg_cost = 0
                    store_stock_delivery_truck_type = ''
                    store_name_list.append(store_name)
                    supply_skus = store['skus']

                    stock_weight = 0
                    for supply_item in supply_skus:
                        sku_id = supply_item['sku_id']
                        nums = supply_item['nums']
                        sku_dict = demand_dict.get(str(sku_id),{})
                        demand = sku_dict.get('demand',0)
                        weight = sku_dict.get('weight',0)
                        stock_weight += float(weight) * min(demand,nums)
                    stock_weight = round(stock_weight,3)

                    sharing_truck_delivery  = store['sharing_truck_delivery']
                    sharing_truck_delivery_list = []
                    for delivery_cost in sharing_truck_delivery:
                        weight_range = delivery_cost['weight_range']
                        truck_type = delivery_cost['truck_type']
                        point = delivery_cost['point']
                        cost = delivery_cost['cost']
                        if order_weight > weight_range[0] and order_weight <= weight_range[1]:
                            store_kg_cost = cost
                            store_delivery_truck_type = truck_type

                        if stock_weight > weight_range[0] and stock_weight <= weight_range[1]:
                            store_stock_kg_cost = cost
                            store_stock_delivery_truck_type = truck_type

                        sharing_truck_delivery_list.append({
                            '重量起始':weight_range[0],
                            '重量结束':weight_range[1],
                            '车型':truck_type,
                            '点位数':point,
                            '成本':cost,
                        })
                    
                    schedule_period = 0
                    supply_items =[]
                    e_cost = 0
                    ep_cost = 0
                    es_cost = 0
                    ed_cost = 0

                    ep_stock_cost = 0
                    es_stock_cost = 0
                    ed_stock_cost = 0
                    e_stock_cost = 0
                    finish_order = True
                    lack_skus = []

                    for supply_item in supply_skus:
                        sku_id = supply_item['sku_id']
                        nums = supply_item['nums']
                        schedule_period = supply_item['time']['调度时间']
                        storage_cost = supply_item['cost']['存储成本']
                        purchase_cost = supply_item['cost']['采购成本']
                        sku_dict = demand_dict.get(str(sku_id),{})
                        sku_name = sku_dict.get('name','')
                        demand = sku_dict.get('demand',0)
                        weight = sku_dict.get('weight',0)
                        sku_delivery_cost =  round(float(weight) * float(store_kg_cost) ,6)

                        sku_total_cost =  round(float(weight) * float(store_kg_cost) + float(purchase_cost) + float(storage_cost),6)
                        ep_cost += purchase_cost * demand
                        es_cost += storage_cost * demand
                        ed_cost += float(weight) * float(store_kg_cost) * demand
                        e_cost += sku_total_cost * demand

                        ep_stock_cost += purchase_cost *  min(demand,nums)
                        es_stock_cost += storage_cost *  min(demand,nums)
                        ed_stock_cost += float(weight) * float(store_kg_cost) *  min(demand,nums)
                        e_stock_cost += round(float(weight) * float(store_stock_kg_cost) + float(purchase_cost) + float(storage_cost),6) *  min(demand,nums)

                        if nums < demand:
                            lack_skus.append(
                                {
                                    'goods_attr_id':sku_id,
                                    'weight':weight,
                                    'lack_stock':demand - nums
                                }
                            )
                            finish_order = False

                        supply_items.append({
                            'goods_attr_id':sku_id,
                            '商品名称':sku_name,
                            '采购成本':purchase_cost,
                            '仓储成本':storage_cost,
                            '配送成本': sku_delivery_cost,
                            '库存':nums,
                            '需求':demand,
                            '是否满足需求': nums >= demand,
                            '单件总成本': sku_total_cost,
                            '预估总配送成本': sku_delivery_cost * demand,
                            '预估总成本': sku_total_cost * demand,
                        })
                        

                    supply_store_info[store_name] = {
                        "store_id": store_id,
                        "配送距离": delivery_distance,
                        "总时效":schedule_period + delivery_duration +floor_time,
                        "是否满足时效": remain_time > (schedule_period + delivery_duration +floor_time),
                        "调度时效":schedule_period,
                        "配送时效": delivery_duration,
                        "搬楼时效": floor_time,
                        "仓库类型": store_type,
                        "是否可以发尽":finish_order,
                        "假设订单发尽-重量":order_weight,
                        "预估配送车型(假设订单发尽)":store_delivery_truck_type,
                        "预估配送费率(假设订单发尽)":round(store_kg_cost,5),
                        "预估配送成本(假设订单发尽)":round(ed_cost,5),
                        "预估采购成本(假设订单发尽)":round(ep_cost,5),
                        "预估仓储成本(假设订单发尽)":round(es_cost,5),
                        "预估总成本(假设订单发尽)":round(e_cost,5),

                        "假设仓库发尽-重量":stock_weight,
                        "预估配送费率(假设仓库发尽)":round(store_stock_kg_cost,5),
                        "预估配送车型(假设仓库发尽)":store_stock_delivery_truck_type,
                        "预估配送成本(假设仓库发尽)":round(ed_stock_cost,5),
                        "预估采购成本(假设仓库发尽)":round(ep_stock_cost,5),
                        "预估仓储成本(假设仓库发尽)":round(es_stock_cost,5),
                        "预估总成本(假设仓库发尽)":round(e_stock_cost,5),


                        "配送成本": pd.DataFrame(sharing_truck_delivery_list),
                        "商品成本": pd.DataFrame(supply_items),
                        "缺货skus":lack_skus
                    }
                
                supply_info['仓库信息'] = supply_store_info

            result_info = {}
            result =  order_route_log['result']
            print(result)
            if result is not None:
                result =  json.loads(result)
                result_conclusion= {}
                store_dict = {}
                result_conclusion['是否满足时效'] = result['period_check']
                result_conclusion['总成本'] = result['total_value']['总成本']
                result_conclusion['总时长'] = result['total_value']['总时长']
                result_conclusion['总重量'] = result['total_value']['总重量']
                result_conclusion['费率'] = result['total_value']['费率']
                result_conclusion['点位成本'] = result['total_value'].get('点位成本',0)

                for row in result['cost_dist']:
                    store_id = list(row[0].keys())[0]
                    store_name = list(row[0].values())[0]
                    total_cost =  row[1]['成本']
                    p_cost =  row[1]['采购成本']
                    s_cost =  row[1]['存储成本']
                    t_cost =  row[1]['运输成本']
                    store_dict[store_name] = {
                        'store_id':store_id,
                        '总成本':total_cost,
                        '采购成本':p_cost,
                        '存储成本':s_cost,
                        '运输成本':t_cost,
                    }
                
                for row in result['time_dist']:
                    store_item =  store_dict[store_name]
                    total_cost =  row[1]['时长']
                    store_item['调度时间'] =  row[1]['调度时间']
                    store_item['运输时间'] =  row[1]['运输时间']
                    store_item['搬楼时间'] =  row[1]['搬楼时间']
                    store_item['点位时间'] =  row[1]['点位时间']

      
                result_conclusion['发货成本'] = store_dict

                result_info['分仓结果'] = result_conclusion

            try_route = []
            single_store_list =[]
            for store_name,store_info in supply_info['仓库信息'].items():
                try_route.append({
                    '方案类型':'单仓发尽',
                    '仓库名':store_name,
                    '是否可以发尽':store_info['是否可以发尽'],
                    '副仓是否发货':'-',
                    '是否满足时效':store_info['是否满足时效'],
                    '需求时效':remain_time,
                    '仓库时效':store_info['总时效'],
                    '发货重量':store_info['假设订单发尽-重量'],
                    '总成本':store_info['预估总成本(假设订单发尽)'],
                    '配送距离(km)':store_info['配送距离'],
                    '车型':store_info['预估配送车型(假设订单发尽)'],
                    '配送费率':store_info['预估配送费率(假设订单发尽)'],
                    '配送成本':store_info['预估配送成本(假设订单发尽)'],
                    '采购成本':store_info['预估采购成本(假设订单发尽)'],
                    '仓储成本':store_info['预估仓储成本(假设订单发尽)'],
                })
                if store_info['是否可以发尽']:
                    single_store_list.append(store_name)
                
                
            com_list = []
            from itertools import combinations
            r = []

            def build_case(ret, first,second,first_info,second_info,point_cost):
                lack_skus =  first_info['缺货skus']
                lack_dict  ={}
                for sku in lack_skus:
                    sku_id = sku['goods_attr_id']
                    lack_stock = sku['lack_stock']
                    lack_dict[str(sku_id)]=sku
                
                second_skus =  second_info['商品成本'].to_dict('records')
                second_dict = {}
                for sku in second_skus:
                    sku_id = sku['goods_attr_id']
                    second_dict[str(sku_id)]=sku
                
                second_weight = 0
                finish_order = True
                second_p_cost = 0
                second_s_cost = 0
                # second_d_cost = 0
                
                for k,v in lack_dict.items():
                    lack_stock =  v['lack_stock']
                    weight = v['weight']
                    second_item = second_dict.get(k,{})
                    if lack_stock > second_item.get('库存',0):
                        finish_order = False
                    second_p_cost += second_item.get('采购成本',0) * min(second_item.get('库存',0),lack_stock)
                    second_s_cost += second_item.get('仓储成本',0) * min(second_item.get('库存',0),lack_stock)
                    # second_d_cost += second_item.get('配送成本',0)
                    second_weight += float(weight) * min(second_item.get('库存',0),lack_stock)

                second_delivery_cost =  second_info['配送成本'].to_dict('records')
                second_store_kg_cost = 0
                second_store_stock_delivery_truck_type  = ''

                for row in second_delivery_cost:
                    weight_start = row['重量起始']
                    weight_end = row['重量结束']
                    truck_type = row['车型']
                    cost = row['成本']
                    
                    if second_weight > weight_start and second_weight <= weight_end:
                        second_store_kg_cost = cost
                        second_store_stock_delivery_truck_type = truck_type
                
                second_d_cost = second_store_kg_cost * second_weight
                first_cost = first_info['预估总成本(假设仓库发尽)']
                second_cost = second_d_cost + second_p_cost + second_s_cost

                total_cost = round(first_cost + second_cost + point_cost,3)
                second_d_cost = round(second_d_cost,5)
                second_p_cost = round(second_d_cost,5)
                second_s_cost = round(second_d_cost,5)

                first_weight= round(first_info['假设仓库发尽-重量'],3)
                second_weight= round(second_weight,3)
                first_period = first_info['总时效']
                first_period_ok = first_info['是否满足时效']

                second_period = second_info['总时效']
                second_period_ok = second_info['是否满足时效']
                total_period_ok = first_period_ok and second_period_ok


                ret.append({
                        '方案类型':'双仓',
                        '仓库名':f'{first}(主发)/{second}',
                        '是否可以发尽':finish_order,
                        '副仓是否发货':str(second_weight > 0),
                        '是否满足时效':f'{total_period_ok}',
                        '需求时效':remain_time,
                        '仓库时效':f'{int(max(first_period,second_period))}',
                        '发货重量':f'{first_weight+second_weight}({first_weight},{second_weight})',
                        '总成本':str(total_cost) +'('+  str(round(first_cost,2)) + ',' + str(round(second_cost,2)) + f',点位:{point_cost})',
                        '配送距离(km)':str(first_info['配送距离']) + ',' + str(second_info['配送距离']),
                        '车型':first_info['预估配送车型(假设仓库发尽)'] + ',' + second_store_stock_delivery_truck_type,
                        '配送费率':str(first_info['预估配送费率(假设仓库发尽)'])+ ',' + str(second_store_kg_cost),
                        '配送成本':str(first_info['预估配送成本(假设仓库发尽)'])+ ',' + str(second_d_cost),
                        '采购成本':str(first_info['预估采购成本(假设仓库发尽)'])+ ',' + str(second_p_cost),
                        '仓储成本':str(first_info['预估仓储成本(假设仓库发尽)'])+ ',' + str(second_s_cost),
                    })

            for first,second in combinations(store_name_list, 2):
                if first not in single_store_list:
                    build_case(try_route,first,second,supply_info['仓库信息'][first],supply_info['仓库信息'][second],result_conclusion['点位成本'])

                if second not in single_store_list:
                    build_case(try_route,second,first,supply_info['仓库信息'][second],supply_info['仓库信息'][first],result_conclusion['点位成本'])

            order_info['订单需求'] = order_skus_df

            return {
                '订单信息':order_info,
                '供应信息':supply_info,
                '分仓方案':result_info,
                '可行方案比较':try_route,
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
                                "url":'online',
                                "request_id":None,
                                "order_sn":'220304114941784736',
                                "request_order":1
                                }
                            )
