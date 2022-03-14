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
    concat(if(s.store_name is null,'',s.store_name),'.',if(wh.store_name is null,'',wh.store_name)) as `仓库名称`,
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
where  status = 1
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

db_url = 'mysql+pymysql://xpx_db:Aa112233445566@rm-bp17v62z92lrim3w2zo.mysql.rds.aliyuncs.com:3306/xpx_data'
iwn_store_watch_table_page = DBTablePage('algo_mysql','iwn_store_watch',db_url, store_sql,module_title='算法测表')
iwn_store_car_type_table_page = DBTablePage('algo_mysql','iwn_store_car_type',db_url,
  iwn_store_car_type_sql,module_title='算法测表'
)

iwn_store_car_type_point_table_page = DBTablePage('algo_mysql','iwn_store_car_type_point',db_url,
  iwn_store_car_type_point_sql,module_title='算法测表'
)
iwn_upstairs_effectiveness_table_page = DBTablePage('algo_mysql','iwn_upstairs_effectiveness',db_url,
  iwn_upstairs_effectiveness_sql,module_title='算法测表'
)
iwn_base_car_type_table_page = DBTablePage('algo_mysql','iwn_base_car_type',db_url,
  iwn_base_car_type_sql,module_title='算法测表'
)

iwn_storage_turnover_cost_table_page = DBTablePage('algo_mysql','iwn_storage_turnover_cost',db_url,
  iwn_storage_turnover_cost_sql,module_title='算法测表'
)
