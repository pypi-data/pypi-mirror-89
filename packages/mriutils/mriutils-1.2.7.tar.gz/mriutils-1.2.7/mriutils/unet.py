#!/usr/bin/env python

from keras.layers import MaxPooling2D, Input, Conv2D, Dropout, UpSampling2D, Concatenate
from keras.models import Model
from keras.optimizers import Adam
import numpy as np
import os
from keras.models import load_model
from keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor='val_loss',patience=3)


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class UNet:
    def __init__(self, input_shape = (256, 256, 1), pretrained_weights = None):
        self.input_shape = input_shape
        self.pretrained_weights = pretrained_weights
        self.model = self.structure()
        self.model.compile(optimizer = Adam(lr = 1e-5), 
                                            loss = 'binary_crossentropy', 
                                            metrics = ['accuracy'])

    def structure(self):
        inputs = Input(self.input_shape)
        conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
        conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
        conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
        conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
        conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
        conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
        conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
        drop4 = Dropout(0.5)(conv4)
        pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

        conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
        conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
        drop5 = Dropout(0.5)(conv5)

        up6 = Conv2D(512, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(drop5))
        merge6 = Concatenate(axis = 3)([drop4,up6])
        conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge6)
        conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv6)

        up7 = Conv2D(256, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv6))
        merge7 = Concatenate(axis = 3)([conv3,up7])
        conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge7)
        conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv7)

        up8 = Conv2D(128, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv7))
        merge8 = Concatenate(axis = 3)([conv2,up8])
        conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge8)
        conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv8)

        up9 = Conv2D(64, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv8))
        merge9 = Concatenate(axis = 3)([conv1,up9])
        conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge9)
        conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
        conv9 = Conv2D(2, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
        outputs = Conv2D(1, 1, activation = 'sigmoid')(conv9)

        model = Model(inputs, outputs)
        
        model.summary()

        if(self.pretrained_weights):
    	    model.load_weights(self.pretrained_weights)

        return model

    def train(self, train_set, data_mode, label_mode, test_set, epochs = 100, batch_size = 4, save_interval = 10):
        X_train = np.resize(train_set[data_mode], (len(train_set[data_mode]),train_set[data_mode][0].shape[0], train_set[data_mode][0].shape[1], 1))
        Y_train = np.resize(train_set[label_mode], (len(train_set[label_mode]),train_set[label_mode][0].shape[0], train_set[label_mode][0].shape[1], 1))
        x_test = np.resize(test_set[data_mode], (len(test_set[data_mode]),test_set[data_mode][0].shape[0], test_set[data_mode][0].shape[1], 1))
        y_test = np.resize(test_set[label_mode], (len(test_set[label_mode]),test_set[label_mode][0].shape[0], test_set[label_mode][0].shape[1], 1))
        X_train = Normalization(X_train, 'train').norm()
        Y_train = Normalization(Y_train, 'label').norm()
        x_test = Normalization(x_test, 'train').norm()
        y_test = Normalization(y_test, 'label').norm()
        self.model.fit(X_train, Y_train, validation_data = (x_test, y_test), epochs = epochs, batch_size = batch_size, callbacks = [early_stopping])
        if not os.path.exists('saved_models'):
            os.makedir('saved_models')
        self.model.save_weights('saved_models/model_for_%s_unet.hdf5' %(data_mode), True)
    
    def evaluate(self, test_result, test_gt):
        return 
    
    def test(self, test_set, model_path, evaluate = None, test_gt = None):
        self.model = load_model(model_path)
        test_set = np.resize(test_set, (test_set.shape[0], test_set[0].shape[1], test_set[0].shape[2], test_set[0].shape[3], 1))
        test_result = self.model.predict(test_set)
        if evaluate != None:
            self.evaluate(test_result, test_gt)
        
        return test_result

if __name__ == '__main__':
    unet = UNet((256, 256, 1))