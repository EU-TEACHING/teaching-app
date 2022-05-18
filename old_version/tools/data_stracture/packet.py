import json
import time

class Data_packet():

    def __init__(self,name = None,value = None,data_type = None,timestamp = None):
        self.name = name
        self.value = value
        self.timestamp = time.time() if timestamp is None else timestamp
        self.data_type = data_type

    def loads(self,bytes):
        data = json.loads(bytes)
        if self.__dict__.keys() != data.keys():
            print('Wrong data format on packet')
        else:        
            self.__dict__ = data
        
    
    def print(self):
        print(self.__dict__)

    def dumps(self):        
        return json.dumps(self.__dict__)
