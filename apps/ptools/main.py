
import pandas as pd
from easy_dash.app import EasyApp

from pages.detail_page import detail_page
from pages.test_page import test_page

app = EasyApp(title='样品记录',
    pages=[
    detail_page,
    test_page
])
app.normal()
app.run()