from  sqlalchemy import create_engine

engine_dict = {'default':{ 'url':'sqlite:///data/data.db'}}

def get_engine(name='default'):
    global engine_dict
    instance = engine_dict.get(name,None)
    if instance is None:
        raise Exception(f'unknown engine:{name}')
    
    url = instance['url']
    engine = instance.get('engine',None)
    if engine is None:
        engine = create_engine(url)
        instance['engine'] = engine
    return engine