import os
from tools.rabbitmq.producer import Pika_Producer
from tools.data_stracture.packet import Data_packet as dp
from sensing.device.gsrplus import ShimmerGSRPlus
#from sensing.processing_module import signal_processing_module

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

    SAMPLING_RATE =  os.getenv('SAMPLING_RATE')
    if SAMPLING_RATE is None:
        print('SAMPLING_RATE Env Variable missing!')
        exit() 
    
    DEVICE_PORT =  os.getenv('DEVICE_PORT')
    if DEVICE_PORT is None:
        print('DEVICE_PORT Env Variable missing!')
        exit() 

    exchanges = ['HR','EDA']
    rabbit_params = {'user': RABBITMQ_USER,'password': RABBITMQ_PASSWORD,'host': RABBITMQ_HOST, 'port' : RABBITMQ_PORT}      
    publisher = Pika_Producer(rabbit_params,exchanges,retries=5)
    device = ShimmerGSRPlus(sampling_rate=SAMPLING_RATE)

    try:
        device.connect(DEVICE_PORT)      
        for n, reads in device.stream():
            if n > 0:
                for single_read in reads:
                    for i in range(0,len(single_read['timestamp'])):
                        data_type = 'readings'
                        publisher.publish(dp('HR',single_read['HR'][i],'readings',single_read['timestamp'][i]).dumps(),'HR')
                        publisher.publish(dp('EDA',single_read['EDA'][i],'readings',single_read['timestamp'][i]).dumps(),'EDA')
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('Exit by user')
    finally:
        device.disconnect()
        publisher.stop()
        
