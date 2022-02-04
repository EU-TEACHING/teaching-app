import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from tools.rabbitmq.consumer import Pika_Consumer
from tools.data_stracture.packet import Data_packet as dp

def store_on_db(sensor,influxdb_write_api):    
    if sensor is None:
        return    
    p = Point("Sensors").field(sensor.name, sensor.value)
    influxdb_write_api.write(bucket=INFLUXDB_BUCKET, record=p)

def callback(ch, method, properties, body): 
    packet = dp()        
    packet.loads(body) 
    store_on_db(packet,influxdb_write_api) 

if __name__ == '__main__':   

    SERVICE_NAME = os.getenv('SERVICE_NAME')
    if SERVICE_NAME is None:
        print('SERVICE_NAME Env Variable missing!')
        exit()       

    RABBITMQ_HOST = os.getenv('RABBIT_HOST')
    if RABBITMQ_HOST is None:
        print('RABBITMQ_HOST Env Variable missing!')
        exit()

    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    if RABBITMQ_PORT is None:
        print('RABBITMQ_PORT Env Variable missing!')
        exit()
    else:
        RABBITMQ_PORT = int(RABBITMQ_PORT)

    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
    if RABBITMQ_USER is None:
        print('RABBITMQ_USER Env Variable missing!')
        exit()
    
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
    if RABBITMQ_PASSWORD is None:
        print('RABBITMQ_PASSWORD Env Variable missing!')
        exit()
    
    INFLUXDB_HOST =os.getenv('INFLUXDB_HOST')
    if INFLUXDB_HOST is None:
        print('INFLUXDB_HOST Env Variable missing!')
        exit()
    
    INFLUXDB_PORT =os.getenv('INFLUXDB_PORT')
    if INFLUXDB_PORT is None:
        print('INFLUXDB_PORT Env Variable missing!')
        exit()
    else:
        INFLUXDB_PORT = int(INFLUXDB_PORT)        
    
    INFLUXDB_BUCKET =os.getenv('INFLUXDB_BUCKET')
    if INFLUXDB_BUCKET is None:
        print('INFLUXDB_BUCKET Env Variable missing!')
        exit()

    INFLUXDB_ORG =os.getenv('INFLUXDB_ORG')
    if INFLUXDB_ORG is None:
        print('INFLUXDB_ORG Env Variable missing!')
        exit()

    INFLUXDB_TOKEN =os.getenv('INFLUXDB_TOKEN')
    if INFLUXDB_TOKEN is None:
        print('INFLUXDB_TOKEN Env Variable missing!')
        exit()


    INPUT_TOPIC = os.getenv('INPUT_TOPIC')
    if INPUT_TOPIC is None:
        print("INPUT_TOPIC Env Variable missing! 'speed','ay'")
        exit()
    else:
        INPUT_TOPIC = INPUT_TOPIC.split(',') if ',' in INPUT_TOPIC  else [INPUT_TOPIC]

    rabbit_params = {'user': RABBITMQ_USER,'password': RABBITMQ_PASSWORD,'host': RABBITMQ_HOST, 'port' : RABBITMQ_PORT}      
    rb_mq_queue = f'{SERVICE_NAME}_q'   
    readings_consumer = Pika_Consumer(rabbit_params,INPUT_TOPIC,rb_mq_queue,callback=callback)
    client = InfluxDBClient(url=f'http://{INFLUXDB_HOST}:{INFLUXDB_PORT}', token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    influxdb_write_api = client.write_api(write_options=SYNCHRONOUS)
   
    try:       
        readings_consumer.start()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('Exit by user')
    finally:        
        readings_consumer.stop()
