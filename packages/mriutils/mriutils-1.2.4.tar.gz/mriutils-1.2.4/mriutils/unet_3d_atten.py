#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 01:12:02 2020

@author: kuangmeng
"""

from keras.layers import Concatenate, LeakyReLU, Conv3D, UpSampling3D, Input, BatchNormalization, MaxPooling3D, Multiply
from keras.models import Model
from keras.optimizers import Adam
import numpy as np
import os
from keras.models import load_model
from mriutils.metrics import Metrics
from mriutils.tonii import SaveNiiFile
from keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor='val_loss',patience=3)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class UNet3D_Atten():
    def __init__(self, input_shape):
        self.input_shape = input_shape
        self.layers = input_shape[0]
        self.size = input_shape[1] * input_shape[2]
        self.width = input_shape[1]
        self.height = input_shape[2]
        self.model = self.structure()
        self.model.compile(optimizer = Adam(lr = 1e-5), 
                           loss = 'binary_crossentropy', 
                           metrics = ['accuracy'])
        
    def structure(self):
        inputs = Input(self.input_shape)
        
        conv1 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 32)(inputs)
        conv1 = BatchNormalization()(conv1)
        meg1 = LeakyReLU()(conv1)
        conv1 = MaxPooling3D(pool_size=(1, 2, 2))(meg1)
        
        conv2 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 128)(conv1)
        conv2 = BatchNormalization()(conv2)
        meg2 = LeakyReLU()(conv2)
        conv2 = MaxPooling3D(pool_size=(1, 2, 2))(meg2)

        
        conv3 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 512)(conv2)
        conv3 = BatchNormalization()(conv3)
        meg3 = LeakyReLU()(conv3)
        conv3 = MaxPooling3D(pool_size=(1, 2, 2))(meg3)
        
        conv4 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 1024)(conv3)
        conv4 = BatchNormalization()(conv4)
        meg4 = LeakyReLU()(conv4)
        conv4 = MaxPooling3D(pool_size=(1, 2, 2))(meg4)

        atten_in = conv4
        atten_probs = Conv3D(kernel_size = (1, 1, 1), padding = 'same', filters = 1024)(conv4)
        atten_out = Multiply()([atten_in, atten_probs])        
        
        up1 = UpSampling3D(size = (1, 2, 2))(atten_out)
        up1 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 512)(up1)
        up1 = BatchNormalization()(up1)
        up1 = LeakyReLU()(up1)
        up1 = Concatenate(axis = -1)([meg4,up1])

        up2 = UpSampling3D(size = (1, 2, 2))(up1)
        up2 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 256)(up2)
        up2 = BatchNormalization()(up2)
        up2 = LeakyReLU()(up2)
        up2 = Concatenate(axis = -1)([meg3,up2])

        
        up3 = UpSampling3D(size = (1, 2, 2))(up2)
        up3 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 128)(up3)
        up3 = BatchNormalization()(up3)
        up3 = LeakyReLU()(up3)
        up3 = Concatenate(axis = -1)([meg2, up3])

        up4 = UpSampling3D(size = (1, 2, 2))(up3)
        up4 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 32)(up4)
        up4 = BatchNormalization()(up4)
        up4 = LeakyReLU()(up4)
        up4 = Concatenate(axis = -1)([meg1, up4])

        up5 = Conv3D(kernel_size = (3, 3, 3), padding = 'same', filters = 1)(up4)
        outputs = LeakyReLU()(up5)
        
        model = Model(inputs, outputs)
        
        model.summary()
        
        return model

    def train(self, train_set, data_mode, label_mode, test_set, epochs = 15, batch_size = 8, save_interval = 5):
        X_train = np.resize(train_set[data_mode], (len(train_set[data_mode]),train_set[data_mode][0].shape[0], train_set[data_mode][0].shape[1], train_set[data_mode][0].shape[2], 1))
        Y_train = np.resize(train_set[label_mode], (len(train_set[label_mode]),train_set[label_mode][0].shape[0], train_set[label_mode][0].shape[1], train_set[label_mode][0].shape[2], 1))
        x_test = np.resize(test_set[data_mode], (len(test_set[data_mode]),test_set[data_mode][0].shape[0], test_set[data_mode][0].shape[1], test_set[data_mode][0].shape[2], 1))
        y_test = np.resize(test_set[label_mode], (len(test_set[label_mode]),test_set[label_mode][0].shape[0], test_set[label_mode][0].shape[1], test_set[label_mode][0].shape[2], 1))
        X_train = Normalization(X_train, 'train').norm()
        Y_train = Normalization(Y_train, 'label').norm()
        x_test = Normalization(x_test, 'train').norm()
        y_test = Normalization(y_test, 'label').norm()
        self.model.fit(X_train, Y_train, validation_data = (x_test, y_test), epochs = epochs, batch_size = batch_size, callbacks = [early_stopping])
        if not os.path.exists("saved_models"):
            os.makedirs("saved_models")
        self.model.save_weights("saved_models/model_for_%s_unet3d.hdf5" %(data_mode), True)

    def evaluate(self, pred_dir, gt_dir):
        metrics = Metrics()
        metrics.metrics_on_dir(gt_dir, pred_dir)
        
    def test(self, test_dir, predict_dir, model_path, evaluate = None, test_gt_dir = None):
        self.model = load_model(model_path)
        test_files = os.listdir(test_dir)
        nii_file = SaveNiiFile()
        test_set = []
        for file in test_files:
            if file[0] != '.':
                test_data, _, _ = nii_file.load_nii(os.path.join(test_dir, file))
                test_set.append(test_data)
        test_set = np.resize(test_set, (test_set.shape[0], test_set[0].shape[1], test_set[0].shape[2], test_set[0].shape[3], 1))
        test_result = self.model.predict(test_set)
        for i in range(len(test_files)):
            nii_file.save_nii(test_result[i], os.path.join(predict_dir, test_files[1]))
        if evaluate != None:
            self.evaluate(predict_dir, test_gt_dir)
        return test_result

if __name__ == "__main__":
    unet_3d = UNet3D_Atten((4, 128, 128, 1))
    from preprocessing import LoadData
    npy_dir = './processed'
    ld = LoadData(npy_dir)
    ld.load_data_dict()
    train, test, _ = ld.data_split()
    unet_3d.train(train, 'ED', 'ED_GT', test)
        
        
        
        
        
    
        