import os
from  sqlalchemy import create_engine


engine_dict = {}

# 地址:rm-bp17v62z92lrim3w2zo.mysql.rds.aliyuncs.com
# 账号:xpx_db
# 密码:Aa112233445566
engine_url_dict = {
    'pre_mysql#xpx_data':"mysql+pymysql://xpx_db:Aa112233445566@rm-bp17v62z92lrim3w2zo.mysql.rds.aliyuncs.com:3306/xpx_data",
    'online_mysql#xpx_data':"mysql+pymysql://xpx_data_only:8C5bWCLkDW@rm-bp10h91kf7w6i19k0ko.mysql.rds.aliyuncs.com:3306/xpx_data"
}

test_adb_engine_instance = None
online_adb_engine_instance = None
sqlite_engine_instanace = None
test_adb_ecs_engine_instance = None

def conver_python_sql(sql):
    return str(sql).replace('%','%%')


def get_engine(name='pre_mysql#xpx_data'):
    global engine_dict
    global engine_url_dict
    instance = engine_dict.get(name,None)
    if instance is None:
        instance_url = engine_url_dict[name]
        engine_dict[name]=create_engine(instance_url)
    
    return engine_dict[name]


def get_pre_mysql_xpx_data_engine(name='pre_mysql#xpx_data'):
    return get_engine(name=name)

def get_online_mysql_xpx_data_engine(name='online_mysql#xpx_data'):
    return get_engine(name=name)

def get_xpx_data_engine(env=None):
    if env is None:
        env = os.getenv('XPX_DATA_ENGINE','online')

    if env== 'pre':
        return get_pre_mysql_xpx_data_engine()
    elif  env == 'test':
        return get_pre_mysql_xpx_data_engine()
    elif env == 'online':
        return get_online_mysql_xpx_data_engine()


def get_test_mysql_ecs_engine():
    global test_adb_ecs_engine_instance
    if test_adb_ecs_engine_instance is None:
        jdbc_url = "mysql+pymysql://ectouch:Vfr456789ol@rm-bp1457tgaf4pd3zn6to.mysql.rds.aliyuncs.com:3306/ectouch"
        test_adb_ecs_engine_instance = create_engine(jdbc_url)
    return test_adb_ecs_engine_instance

def get_test_adb_engine():
    global test_adb_engine_instance
    if test_adb_engine_instance is None:
        jdbc_url = "mysql+pymysql://ectouch:Vfr456789ol@rm-bp1457tgaf4pd3zn6to.mysql.rds.aliyuncs.com:3306/xpx_data"
        test_adb_engine_instance = create_engine(jdbc_url)
    return test_adb_engine_instance


def get_online_adb_engine():
    global online_adb_engine_instance
    if online_adb_engine_instance is None:
        jdbc_url = "mysql+pymysql://wangcenhan:tuEeVaJKq8@am-bp1y98h053h3267bh167320o.ads.aliyuncs.com:3306/ectouch?charset=utf8"
        online_adb_engine_instance = create_engine(jdbc_url)
    return online_adb_engine_instance


def get_online_adb_demo_01_engine():
    global online_adb_engine_instance
    if online_adb_engine_instance is None:
        jdbc_url = "mysql+pymysql://wangcenhan:tuEeVaJKq8@am-bp1y98h053h3267bh167320o.ads.aliyuncs.com:3306/demo_01?charset=utf8"
        online_adb_engine_instance = create_engine(jdbc_url)
    return online_adb_engine_instance

def get_sqlite_engine():
    global sqlite_engine_instanace
    if sqlite_engine_instanace is None:
        sqlite_engine_instanace = create_engine('sqlite:///algo.db')
    return sqlite_engine_instanace

def get_can_write_engine():
    return get_sqlite_engine()


def get_default_engine():
    return get_test_adb_engine()