import tensorflow as tf
import numpy as np

class Service_Model():
    def __init__(self,model_path):
        self.model = tf.keras.models.load_model(model_path)

    def eval(self,batch):
        batch = np.asarray(batch)
        predictions = self.model.predict(batch)
        action = np.argmax(predictions[0])
        return [action.item()]