#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:42:15 2020

@author: kuangmeng
"""
import os
import SimpleITK as sitk
import skimage.io as skio
from skimage.transform import resize
import numpy as np
import platform

class Normalization():
    def __init__(self, data, mode):
        self.data = data
        self.mode = mode
        self.sysstr = platform.system()

    def norm(self):
        data = self.data
        if self.mode == 'data':
            if np.max(data) > 1:
                data /= 255
            data -= data.mean()
            data /= data.std() 
        elif self.mode == 'label':
            if np.max(data) > 1:
                data /= 255
            data[data > data.mean()] = 1
            data[data <= data.mean()] = 0
        return data

    
    
    
    
    
    
    
    
    
    