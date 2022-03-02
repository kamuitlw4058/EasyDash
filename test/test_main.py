from easy_dash.app import EasyApp
from easy_dash.page.page import Page
from easy_dash.page.db_page import DBTablePage

main_page = Page('main','main_page')
test_page = Page('test','test_page')
iwn_store_car_type_table_page = DBTablePage('algo_mysql','iwn_store_car_type',"select * from iwn_store_car_type")
iwn_store_watch_table_page = DBTablePage('algo_mysql','iwn_store_watch',"select * from iwn_store_watch")



app = EasyApp(pages=[
    main_page,
    test_page,
    iwn_store_watch_table_page,
    iwn_store_car_type_table_page
])
app.normal()
app.run()