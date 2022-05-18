
class Aggregator():
    def __init__(self,topics,batch_size=1):
        self.topics = topics
        self.batch_size = batch_size
        self.batch = []
        self.packet  = [None]*len(topics)
    
    def check_packet(self,packet):
        for item in packet:
            if item is None:
                return False
        return True

    def update_batch(self,reading):
        index = self.topics.index(reading.name)
        self.packet[index] = reading.value    
        if self.check_packet(self.packet):
            self.batch.append(self.packet)                 
            self.packet = [None]*len(self.topics)
        if len(self.batch) >= self.batch_size:         
            self.batch = self.batch[-self.batch_size:]
            print("Send ",self.batch)
            temp_batch = self.batch
            self.batch = []
            return temp_batch
        return None
