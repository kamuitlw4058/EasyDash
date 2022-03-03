
import sys
import requests
import pandas as pd
from easy_dash.app import EasyApp
from easy_dash.page.page import Page
from easy_dash.page.db_page import DBTablePage
from easy_dash.page.auto_detail_page import AutoDetailPage
# sys.path.append("../../")
# print(sys.path)

from db_pages import *
from log_pages import *


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