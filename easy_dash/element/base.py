import uuid
from easy_dash.app import *

class Element():
    def __init__(self,id=None):
        self._id = id

    def id(self):
        if self._id is None:
            self._id = str(uuid.uuid4())
        return self._id
    
    def id_string(self):
        id = self.id()
        if isinstance(id,dict):
            base_id = id['type']
            index = id['index']
            return f'{base_id}={index}'
        else:
            return str(id)

    def store_id(self):
        return f'{self.id()}-store'

    def init_callback(self,app=None):
        pass

    def to_string(self):
        return ''

    def layout(self,app=None):
        return html.P(f"This is the content of {type(self)} element. desc:{self.to_string()} [{self.id_string()}]")