import pika
import json
import pickle
import time

class Pika_Producer():
    def __init__(self,rabbit_params,exchanges,retries=5,socket_timeout=5):
        credentials = pika.PlainCredentials(rabbit_params['user'], rabbit_params['password'])
        config = pika.ConnectionParameters(rabbit_params['host'], rabbit_params['port'],'/',credentials)	
        config.socket_timeout = socket_timeout        
        self.connection = self.connect(config,retries)
        self.channel = self.connection.channel()
        self.exchanges = exchanges    
        for exchange in exchanges:            
            self.channel.exchange_declare(exchange=f'{exchange}.exchange',exchange_type='fanout') 
       

    def connect(self,config,retries):
        count = 0
        while count < retries:
            try:
                connection = pika.BlockingConnection(config)
                return connection
            except:
                print(f'Connection error try: {count+1}')
                count +=1
            
            time.sleep(10)
        exit()

    def publish(self,body,exchange):  
        self.channel.basic_publish(exchange= f'{exchange}.exchange', routing_key='', body=body)

    def stop(self):
        for exchange in self.exchanges:   
            self.channel.exchange_delete(exchange=f'{exchange}.exchange')  
        self.connection.close()




        


