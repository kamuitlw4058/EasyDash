
import requests
import pandas as pd
from easy_dash.app import EasyApp
from easy_dash.page.page import Page
from easy_dash.page.db_page import DBTablePage
from easy_dash.page.auto_detail_page import AutoDetailPage

store_sql = """
select 
    wh.store_id,
    wh.parent_id,
    concat(s.store_name,'.',wh.store_name) as `仓库名称`,
    wh.store_type,
    s.address as `地址`,
    s.xlocal,
    s.ylocal from (
select 
    store_id,
    parent_id,
    store_name,
    address,
    store_type,
    xlocal,
    ylocal 
from iwn_store_watch 
where parent_id != 0
    and status = 1
) wh
left join iwn_store_watch s on wh.parent_id = s.store_id 
"""
iwn_store_car_type_sql = """
select 
    isct.store_id,
    isw.parent_id,
    isw.store_name,
    isct.car_type_id,
    ibct.car_type_name,
    starting_mileage,
    starting_price,
    after_mileage_price,
    isct.full_load_weight

from 
    iwn_store_car_type isct 
left join  (
        select 
            wh.store_id,
            wh.parent_id,
            concat(if(s.store_name is null,'',s.store_name),'.',wh.store_name) as store_name,
            s.address,
            s.xlocal,
            s.ylocal 
        from (
    select 
        store_id,
        parent_id,
        store_name,
        address,
        xlocal,
        ylocal 
    from 
        iwn_store_watch 
    where 
        status = 1
    ) wh
    left join iwn_store_watch s on wh.parent_id = s.store_id
) isw on isct.store_id=isw.store_id
left join  iwn_base_car_type ibct on isct.car_type_id=ibct.car_type_id
where isct.status = 1
"""
iwn_base_car_type_sql = """select car_type_id,car_type_name,full_load_weight from iwn_base_car_type where status = 1"""

iwn_upstairs_effectiveness_sql = """select * from iwn_upstairs_effectiveness"""
iwn_store_car_type_point_sql = """
    select 
        isctp.order_attach,
        isctp.store_id,
        isw.store_name,
        isctp.order_weight_from,
        isctp.order_weight_to,
        isctp.match_car_type_id,
        isctp.rational_load_rate,
        isctp.point,
        ibct.car_type_name

    from iwn_store_car_type_point isctp
    left join  (
            select 
                wh.store_id,
                wh.parent_id,
                concat(if(s.store_name is null,'',s.store_name),'.',wh.store_name) as store_name,
                s.address,
                s.xlocal,
                s.ylocal 
            from (
        select 
            store_id,
            parent_id,
            store_name,
            address,
            xlocal,
            ylocal 
        from 
            iwn_store_watch 
        where 
            status = 1
        ) wh
        left join iwn_store_watch s on wh.parent_id = s.store_id
    ) isw on isctp.store_id=isw.store_id
    left join  iwn_base_car_type ibct on isctp.match_car_type_id=ibct.car_type_id
"""
iwn_storage_turnover_cost_sql = """
select * 
from 
    iwn_storage_turnover_cost  istc 
left join  (
        select 
            wh.store_id,
            wh.parent_id,
            concat(if(s.store_name is null,'',s.store_name),'.',wh.store_name) as store_name,
            s.address,
            s.xlocal,
            s.ylocal 
        from (
    select 
        store_id,
        parent_id,
        store_name,
        address,
        xlocal,
        ylocal 
    from 
        iwn_store_watch 
    where 
        status = 1
    ) wh
    left join iwn_store_watch s on wh.parent_id = s.store_id
) isw on istc.store_id=isw.store_id
where status = 1
"""

main_page = Page('main','main_page')
test_page = Page('test','test_page')
iwn_store_watch_table_page = DBTablePage('algo_mysql','iwn_store_watch',store_sql)
iwn_store_car_type_table_page = DBTablePage('algo_mysql','iwn_store_car_type',
  iwn_store_car_type_sql
)

iwn_store_car_type_point_table_page = DBTablePage('algo_mysql','iwn_store_car_type_point',
  iwn_store_car_type_point_sql
)
iwn_upstairs_effectiveness_table_page = DBTablePage('algo_mysql','iwn_upstairs_effectiveness',
  iwn_upstairs_effectiveness_sql
)
iwn_base_car_type_table_page = DBTablePage('algo_mysql','iwn_base_car_type',
  iwn_base_car_type_sql
)

iwn_storage_turnover_cost_table_page = DBTablePage('algo_mysql','iwn_storage_turnover_cost',
  iwn_storage_turnover_cost_sql
)

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
app = EasyApp(pages=[
    iwn_store_watch_table_page,
    iwn_store_car_type_table_page,
    iwn_store_car_type_point_table_page,
    iwn_base_car_type_table_page,
    iwn_upstairs_effectiveness_table_page,
    iwn_storage_turnover_cost_table_page,
    log_list_page,
    detail_page
])
app.normal()
app.run()