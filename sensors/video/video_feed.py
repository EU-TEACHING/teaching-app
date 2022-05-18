import os
import threading
from time import time

from base.node import TEACHINGNode
from base.communication.packet import DataPacket
from vidgear.gears import WriteGear,VideoGear,CamGear,StreamGear

output_params = {
    "-preset:v": "veryfast",
    "-tune" : "zerolatency", 
    "-g": 60,
    "-sc_threshold": 0,
    "-bufsize": "2500",
    "-f": "flv",
    "-input_framerate":30
    }
stream_params = {"-input_framerate": 1,
                "-livestream": True ,
                "-f": "flv",
                "-flvflags" : 'no_duration_filesize'}

class VideoFeed:
    
    def __init__(self):
        self._rtmp_server = os.environ['RTMP_SERVER']
        self._rtmp_topic = os.environ['RTMP_TOPIC']
        self._source = os.environ['VIDEO_SOURCE']
        #self._record = bool(os.environ['RECORD'])

        self._stream_in = None                               
        self._stream_url = None
        self._streamer = None
        #self._writer = None

    @TEACHINGNode(produce=True, consume=False)
    def __call__(self):
        thread = threading.Thread(target=self._start_streaming)
        thread.start()
        addr = f'rtmp://{self._rtmp_server}/live/stream'
        while True:
            yield DataPacket(topic='sensor.camera.stream_address', body={'address': addr})
            time.sleep(0.5)

    def _build(self):
        if self._source is not None:            
            if 'camera_' in self._source:
                self._source = int(self._source.split('_'))
                self._stream_in = CamGear(source=self._source).start()
            else:
                self._stream_in = VideoGear(source=self._source).start() 

        if self._rtmp_server is not None:
            self._stream_url = f'rtmp://{self._rtmp_server}/live/stream'
            self._streamer =  StreamGear(output=self._stream_url, **stream_params)
        
        #if self._record:
            #self.writer = WriteGear(output_filename=self.stream_url,logging=True,**output_params)
    
    def _start_streaming(self):
        #method for continues stream from source
        while True:
            frame = self._stream_in.read()
            if frame is None:
                break
            self._streamer.stream(frame)
            
    def stop(self):
        if self._stream_in is not None:  
            self._stream_in.stop()
        if self._rtmp_server is not None: 
            #self.writer.close()
            self._streamer.terminate()
