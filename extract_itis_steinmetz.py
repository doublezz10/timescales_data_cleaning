# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 15:17:19 2020

@author: zachz
"""

import numpy as np

#%% Load trials.intervals file from D drive

trials_included = np.load('D:/Steinmetz - Mice/Cori_2016-12-14/trials.included.npy')
trials_intervals = np.load('D:/Steinmetz - Mice/Cori_2016-12-14/trials.intervals.npy')

#%% Get 1s ITIs from trials.intervals

itis = np.zeros((len(trials_intervals),2))

for i in (range(len(trials_intervals))):
    if trials_included[i,0] == True:
    
        iti_start = trials_intervals[i,1] 
        iti_end = trials_intervals[i+1,0]
        
        itis[i,0] = iti_start
        itis[i,1] = iti_end
        
itis = np.delete(itis,np.where(itis<1),axis=0)