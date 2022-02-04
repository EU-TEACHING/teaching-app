import csv
import time
import os
import sys


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

    TRANSMIT_RATE =  os.getenv('TRANSMIT_RATE')
    if TRANSMIT_RATE is None:
        print('TRANSMIT_RATE Env Variable missing!')
        exit() 


    FILE_SOURCE = os.getenv('FILE_SOURCE')
    if FILE_SOURCE is None:
        print('FILE_SOURCE Env Variable missing!')
        exit() 
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
        
