import csv
import time
import os
import sys

data_storage_path = ''
DOCKER_RUN = os.getenv('DOCKER_RUN')
if DOCKER_RUN is None:
    current_path = os.path.dirname(os.path.abspath(__file__))
    sub1 = os.path.abspath(os.path.join(current_path, os.pardir))
    sub2 = os.path.abspath(os.path.join(sub1, os.pardir))    
    sub3 = os.path.abspath(os.path.join(sub2, os.pardir)) 
    sub4 = os.path.abspath(os.path.join(sub3, os.pardir)) 
    final =os.path.abspath(os.path.join(sub2, os.pardir))
    sys.path.append(final) 
    data_storage_path = '../../../'

from tools.rabbitmq.producer import Pika_Producer
from tools.data_stracture.packet import Data_packet as dp


def start(publisher,readings,exchanges,interval):
    print(f'{SERVICE_NAME} started') 
    row = 0
    while True:                     
        for i,exchange in enumerate(exchanges):
            packet = dp(exchange,float(readings[row][i]),'readings')            
            packet.print()
            publisher.publish(packet.dumps(),exchange)      
        if row < len(readings)-1:
            row +=1
        else:
            row = 0
        time.sleep(interval)

if __name__ == '__main__':

    SERVICE_NAME = os.getenv('SERVICE_NAME')
    if SERVICE_NAME is None:
        SERVICE_NAME = 'file_sensor'

    RABBITMQ_HOST = os.getenv('RABBIT_HOST')
    if RABBITMQ_HOST is None:
        RABBITMQ_HOST = '127.0.0.1'

    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    if RABBITMQ_PORT is None:
        RABBITMQ_PORT = 5672
    else:
        RABBITMQ_PORT = int(RABBITMQ_PORT)

    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
    if RABBITMQ_USER is None:
        RABBITMQ_USER = 'user'
    
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
    if RABBITMQ_PASSWORD is None:
        RABBITMQ_PASSWORD = 'bitnami'

    TRANSMIT_RATE =  os.getenv('TRANSMIT_RATE')
    if TRANSMIT_RATE is None:
        TRANSMIT_RATE = 0.1
    else:
        TRANSMIT_RATE = float(TRANSMIT_RATE)


    FILE_SOURCE = os.getenv('FILE_SOURCE')
    if FILE_SOURCE is None:
        FILE_SOURCE = data_storage_path + 'data_storage/raw_data/carla/multisensor_carla.csv'

    try:    
        readings = []
        with open(os.path.dirname(os.path.abspath(__file__))+'/'+ FILE_SOURCE) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')           
            for row in csv_reader:
                readings.append(row) 
    except:
        print('Error on file')
        exit()

    exchanges = readings[0]        
    readings.pop(0)
    
    rabbit_params = {'user': RABBITMQ_USER,'password': RABBITMQ_PASSWORD,'host': RABBITMQ_HOST, 'port' : RABBITMQ_PORT}      
    publisher = Pika_Producer(rabbit_params,exchanges,retries=5)

    try:      
        start(publisher,readings,exchanges,TRANSMIT_RATE)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('Exit by user')
    finally:
        publisher.stop()
        
