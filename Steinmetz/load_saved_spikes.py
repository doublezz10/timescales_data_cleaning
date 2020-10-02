# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 10:38:01 2020

@author: zachz
"""

# Info

"""
The steinmetz_spike_extraction makes .npy files for each of the brain areas we
care about. Below, is information about how these spikes are organized, and 
how to load them into memory
"""

#%% Imports 

import numpy as np
import scipy.io as spio

#%% Loading

aca_spikes = np.load('aca_spikes.npy',allow_pickle=True)
bla_spikes = np.load('bla_spikes.npy',allow_pickle=True)
hc_spikes = np.load('hc_spikes.npy',allow_pickle=True)
ila_spikes = np.load('ila_spikes.npy',allow_pickle=True)
orb_spikes = np.load('orb_spikes.npy',allow_pickle=True)
pl_spikes = np.load('pl_spikes.npy',allow_pickle=True)

#%% How are they organized?

"""
Each .npy file is a NumPy array of arrays of spike times. Each object in the
array is a unit, and it contains its spike times across the entire recording
session. In order to extract meaningful data about where exactly the electrodes
were, refer to the session and channel number given in the session_info.csv
files in this directory - the rows of those csv's are the same as objects in 
the spike arrays. These can be used to refer back to the original
Steinmetz dataset documentation.
"""

#%% Generate dictionaries for each brain region and save as .mat files
    
aca_dict = {'unit_index': range(len(aca_spikes)), 'spikes_aca': aca_spikes}
bla_dict = {'unit_index': range(len(bla_spikes)), 'spikes_bla': bla_spikes}
hc_dict = {'unit_index': range(len(hc_spikes)), 'spikes_hc': hc_spikes}
ila_dict = {'unit_index': range(len(ila_spikes)), 'spikes_ila': ila_spikes}
orb_dict = {'unit_index': range(len(orb_spikes)), 'spikes_orb': orb_spikes}
pl_dict = {'unit_index': range(len(pl_spikes)), 'spikes_pl': pl_spikes}

spio.savemat('aca_spikes.mat',aca_dict)
spio.savemat('bla_spikes.mat',bla_dict)
spio.savemat('hc_spikes.mat',hc_dict)
spio.savemat('ila_spikes.mat',ila_dict)
spio.savemat('orb_spikes.mat',orb_dict)
spio.savemat('pl_spikes.mat',pl_dict)