import pika
import json
import pickle
import time

class Pika_Consumer():
    def __init__(self,rabbit_params,exchanges,queue,data_queue=None,callback=None,retries=5,socket_timeout=5):
        credentials = pika.PlainCredentials(rabbit_params['user'], rabbit_params['password'])
        config = pika.ConnectionParameters(rabbit_params['host'], rabbit_params['port'],'/',credentials)	
        config.socket_timeout = socket_timeout        
        self.connection = self.connect(config,retries)
        self.channel = self.connection.channel()
        self.exchanges = exchanges
        self.queue = queue
        self.channel.queue_declare(queue=f'{queue}.queue')
        for exchange in exchanges: 
            self.channel.queue_bind(exchange=f'{exchange}.exchange',queue=f'{queue}.queue')
            print(f'{exchange}.exchange') 
        if callback is None:
            callback = self.callback
        self.channel.basic_consume(f'{queue}.queue',callback, auto_ack=True)
        self.data_queue = data_queue
        

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

    def callback(self,ch, method, properties, body):       
        self.data_queue.put(body)


    def start(self):
        try:
            self.channel.start_consuming()
        except Exception as e:
            print(e)
        finally:
            self.stop()            

    def stop(self):           
        self.channel.queue_delete(queue=f'{self.queue}.queue')

        self.connection.close()



        
        


