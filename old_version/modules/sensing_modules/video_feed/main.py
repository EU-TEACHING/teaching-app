import os
import sys
import asyncio


from tools.rabbitmq.producer import Pika_Producer
from tools.data_stracture.packet import Data_packet as dp
from tools.video_streamer.streamer import Video_feed_handler

def start(video_handler):
    video_handler.start_streaming()
    
async def report_rtmp(publisher,video_handler):
    print(f'{SERVICE_NAME} started') 
    loop = asyncio.get_event_loop()    
    loop.run_in_executor(None, start,video_handler)    
    packet = dp(OUTPUT_TOPIC[0],f'rtmp://{RTMP_SERVER}/live/{RTMP_TOPIC}','video_stream')  
    while True:
        publisher.publish(packet.dumps(),OUTPUT_TOPIC[0])   
        await asyncio.sleep(0.001)
        
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
      
    RTMP_SERVER = os.getenv('RTMP_SERVER')
    if RTMP_SERVER is None:
        print('RTMP_SERVER Env Variable missing!')
        exit() 

    RTMP_TOPIC = os.getenv('RTMP_TOPIC')
    if RTMP_TOPIC is None:
        print('RTMP_TOPIC Env Variable missing!')
        exit() 

    VIDEO_SOURCE = os.getenv('VIDEO_SOURCE')
    if VIDEO_SOURCE is None:
        print('VIDEO_SOURCE Env Variable missing!')
        exit() 

    OUTPUT_TOPIC = os.getenv('OUTPUT_TOPIC')
    if OUTPUT_TOPIC is None:
        print('OUTPUT_TOPIC Env Variable missing!')
        exit() 
    else:
        OUTPUT_TOPIC = OUTPUT_TOPIC.split(',') if ',' in OUTPUT_TOPIC  else [OUTPUT_TOPIC]        

    rabbit_params = {'user': RABBITMQ_USER,'password': RABBITMQ_PASSWORD,'host': RABBITMQ_HOST, 'port' : RABBITMQ_PORT} 
    publisher = Pika_Producer(rabbit_params,OUTPUT_TOPIC,retries=5)
    video_handler = Video_feed_handler(rtmp_server=RTMP_SERVER, rtmp_topic=RTMP_TOPIC,source=VIDEO_SOURCE)
    loop = asyncio.get_event_loop()
    print("Video feed started")
    try:
        result = loop.run_until_complete(report_rtmp(publisher,video_handler))
        #asyncio.run(report_rtmp(publisher,video_handler))         
        
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('Exit by user')
    finally:
        publisher.stop()
        video_handler.stop()
        