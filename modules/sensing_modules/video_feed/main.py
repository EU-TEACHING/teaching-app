import os
import sys
import asyncio

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
        SERVICE_NAME = 'dash_cam_video'

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
      
    RTMP_SERVER = os.getenv('RTMP_SERVER')
    if RTMP_SERVER is None:
        RTMP_SERVER = '127.0.0.1'

    RTMP_TOPIC = os.getenv('RTMP_TOPIC')
    if RTMP_TOPIC is None:
        RTMP_TOPIC = 'dash_cam_video'  

    VIDEO_SOURCE = os.getenv('VIDEO_SOURCE')
    if VIDEO_SOURCE is None:
        VIDEO_SOURCE = data_storage_path + 'data_storage/videos/drive.mp4'  
    
    OUTPUT_TOPIC = os.getenv('OUTPUT_TOPIC')
    if OUTPUT_TOPIC is None:
        OUTPUT_TOPIC = ['dash_cam_video']
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
        