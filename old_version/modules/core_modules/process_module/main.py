import os
from tools.rabbitmq.consumer import Pika_Consumer
from tools.rabbitmq.producer import Pika_Producer
from tools.data_stracture.packet import Data_packet as dp
from tools.video_streamer.streamer import Video_feed_handler
from tools.aggregator.aggregator import Aggregator
from module import Service_Model

def check_if_in_list(item, list):
    try:
        pos = list.index(item)
        return pos
    except:
        return None

def callback(ch, method, properties, body): 
    packet = dp()        
    packet.loads(body)
    if packet.data_type == 'video_stream':
        pos = check_if_in_list(packet.name, video_consumers_names)
        if pos is not None:
            packet.value = video_consumers[pos].get_frame()
        else:
            video_consumers.append(Video_feed_handler(source=packet.value))
            video_consumers_names.append(packet.name)
            pos = check_if_in_list(packet.name, video_consumers_names)
            packet.value = video_consumers[pos].get_frame()
    batch =  aggregator.update_batch(packet)
    if batch is not None:               
        output = service.eval(batch)
        for i,item in enumerate(output):
            data_type = 'readings'
            packet = dp(OUTPUT_TOPIC[i],item,data_type)            
            packet.print()
            publisher.publish(packet.dumps(),OUTPUT_TOPIC[i])

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

    INPUT_TOPIC = os.getenv('INPUT_TOPIC')
    if INPUT_TOPIC is None:
        print('INPUT_TOPIC Env Variable missing!')
        exit() 
    else:
        INPUT_TOPIC = INPUT_TOPIC.split(',') if ',' in INPUT_TOPIC  else [INPUT_TOPIC]
    
    BATCH_SIZE = os.getenv('BATCH_SIZE')
    if BATCH_SIZE is None:
        print('BATCH_SIZE Env Variable missing!')
        exit() 
    else:
        BATCH_SIZE = int(BATCH_SIZE)

    MODEL_PATH = os.getenv('MODEL_PATH')
    if MODEL_PATH is None:
        print('MODEL_PATH Env Variable missing!')
        exit() 

    OUTPUT_TOPIC = os.getenv('OUTPUT_TOPIC')
    if OUTPUT_TOPIC is None:
        print('OUTPUT_TOPIC Env Variable missing!')
        exit() 
    else:
        OUTPUT_TOPIC = OUTPUT_TOPIC.split(',') if ',' in OUTPUT_TOPIC  else [OUTPUT_TOPIC]    
             
    rb_mq_queue = f'{SERVICE_NAME}_q'     
    rabbit_params = {'user': RABBITMQ_USER,'password': RABBITMQ_PASSWORD,'host': RABBITMQ_HOST, 'port' : RABBITMQ_PORT} 
    consumer = Pika_Consumer(rabbit_params,INPUT_TOPIC,rb_mq_queue,callback=callback)    
    publisher = Pika_Producer(rabbit_params,OUTPUT_TOPIC,retries=5)
    aggregator = Aggregator(INPUT_TOPIC,batch_size=1)
    service =  Service_Model(MODEL_PATH)

    video_consumers = []
    video_consumers_names= []    
    try:
        consumer.start()        
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('Exit by user')
    finally:        
        consumer.stop()
        publisher.stop()