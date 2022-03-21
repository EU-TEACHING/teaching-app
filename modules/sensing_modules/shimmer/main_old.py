from sensing.device.gsrplus import ShimmerGSRPlus
from sensing.processing_module import signal_processing_module
import os

SAMPLING_RATE = 64
DEVICE_PORT = os.getenv('DEVICE_PORT') # TODO: add the path to the device, e.g. /dev/ttyUSB0

MODE = 'process' # TODO: choose mode \in {'raw', 'process'}


if __name__ == '__main__':
    device = ShimmerGSRPlus(sampling_rate=SAMPLING_RATE)
    device.connect(DEVICE_PORT)

    if MODE == 'raw':
        for n, reads in device.stream():
            if n > 0:
                print(reads)                
                    
    
    if MODE == 'process':
        for hr_ppg_dict in signal_processing_module(device.stream, seconds_per_return=1, sampling_rate=SAMPLING_RATE):
            print(hr_ppg_dict)