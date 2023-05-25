
from keras.utils import Sequence
import numpy as np
import cv2 as cv

class BatchGenerator(Sequence):

    def __init__(self, x_train, y_train, batch_size,class_names,image_size,cap = None):
        self.x_train = x_train
        self.y_train = y_train
        self.classes = class_names
        self.img_size = image_size
        self.batch_size = batch_size
        self.indices1 = np.arange(len(x_train))
        self.cap = cap
        np.random.shuffle(self.indices1)

    
    # Number of steps of gradient descent per epoch i.e. number of batches
    def __len__(self):
        return int(np.ceil(self.x_train.shape[0] / float(self.batch_size)))
 
    # Selects indices of data for next batch
    def __getitem__(self, idx):

        batch_x = self.x_train[self.indices1[idx * self.batch_size:(idx + 1) * self.batch_size]]
        batch_y = self.y_train[self.indices1[idx * self.batch_size:(idx + 1) * self.batch_size]]

        if self.cap is not None:
            for i in range(len(batch_x)):
                batch_x[i] = cv.resize(batch_x[i],(self.img_size,self.img_size))
                batch_x[i] = batch_x[i]/255.0

        return batch_x, batch_y

    # What to do to the data before returning it
    def on_epoch_end(self):
        np.random.shuffle(self.indices1)