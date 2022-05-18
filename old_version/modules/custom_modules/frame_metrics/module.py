import time
import cv2

class Service_Model():
    def __init__(self,*argv):
        self.frame_number = 0

    def eval(self,batch):
        frame = batch[0][0]
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        timestamp = time.time()
        frame = cv2.putText(frame, f'{timestamp}', (50,100), font,fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, f'{batch[0][1]}', (50,150), font,fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, f'{batch[0][2]}', (50,200), font,fontScale, color, thickness, cv2.LINE_AA)    
        cv2.imwrite(f'data_storage/stored_frames/frame_f{self.frame_number}_t{timestamp}.jpg', batch[0][0])
        self.frame_number +=1
        return [self.frame_number]