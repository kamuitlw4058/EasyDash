from easy_dash.model.options import Option
from easy_dash.element.layout.page import Page
from easy_dash.element.params.dict_params import DictParams
from easy_dash.element.table.item_list import ItemList
from easy_dash.element.layout.rows import Rows
from easy_dash.element.form.key_value import KeyValueElement
from easy_dash.element.form.button import CollapseP
from easy_dash.app import *

item_list =  ItemList(data = [
    {
    'item1':123,
    'item2':'xxx',
},    
{
    'item1':1423,
    'item2':'xxxff',
},
{
    'item1':1423,
    'item2':'xxxff',
},
{
    'item1':1423,
    'item2':'xxxff',
},
{
    'item1':744,
    'item2':'xxxff',
},
{
    'item1':66,
    'item2':'xxxff',
},
{
    'item1':55,
    'item2':'xxxff',
},
{
    'item1':33,
    'item2':'xxxff',
},
{
    'item1':334,
    'item2':'xxxff',
},
{
    'item1':55555,
    'item2':'xxxff',
},
])

def params_update_func(kwargs):
    print('enter update func')
    print(kwargs)
    test2= kwargs['test2']
    options = [{'label':'gggg',"value":'sss'},
    {'label':'cccc',"value":'22'}
    ]
    if test2:
        options.append({'label':test2,"value":test2})
    # return Option(options)
    return item_list

dict_element =  DictParams({'test':'test',
'test2':Option([
    {'label':'ttt',"value":'2222'},
    {'label':'sdd',"value":'3333'}
])},update_func=params_update_func, 
# content= Option([{'label':'gggg',"value":'sss'}])
content= item_list

)


rows_element = Rows([
    KeyValueElement('test','tttt',display_name='显示名'),
    KeyValueElement('test2','tttt34',display_name='显示名2'),
    CollapseP()
])



test_page= Page('procurement','test_age',
                            module_title='采购',
                            page_title="测试",
                            content=rows_element,
                            # content=dict_element
                            )