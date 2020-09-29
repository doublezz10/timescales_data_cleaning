# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 15:51:10 2020

@author: zachz
"""

#%% What does this do?
"""
This file will loop through all of the folders (i.e. recording sessions) in the
Steinmetz dataset. It will make 3d NumPy arrays of each of the following
variables, organized in this way (n_rows,n_cols,n_z's):

all_intervals-      size: trials x 2 x sessions
                    data: for each trial, contains start and end times of ITI
                           
all_included-       size: trials x 1 x sessions
                    data: for each trial, True or False for whether trial was
                    analysed in orignial paper

all_spike_times-    size: n_spikes x sessions
                    data: one long array of every spike time on the probe
                    (irrespective of brain area)

all_spike_clusters- size: n_spikes x sessions
                    data: one long array of which cluster (i.e. unit) each spike
                    belongs to

all_good_clusters-  size: n_clusters x sessions
                    data: rates each cluster on quality of spike sorting
                    0 = noise, 1 = probably multiple neurons
                    2 = good, 3 = unsorted
                    
all_peak_channels-  size: n_clusters x sessions
                    data: peak channel number for each cluster, used for
                    mapping brain areas onto cluster numbers
                    
all_brain_areas-    size: n_channels x sessions
                    data: string of abbreviated brain area for each channel
"""

#%% Imports 

import numpy as np
import os
import pandas as pd

#%% Loop through each recording session to extract itis and trial_included

all_intervals = []
all_included = []
all_spike_times = []
all_spike_clusters = []
all_good_clusters = []
all_peak_channels = []
all_brain_areas = []

root = 'D:/Steinmetz - Mice'

absolute_filenames = []

for dirname, dirnames, filenames in os.walk(root):
    
    for filename in filenames:
    
        absolute_filenames.append(os.path.join(dirname,filename))
    
                              
#%% Loop through files in directory to extract relevant variables

for f_name in absolute_filenames:

    if f_name.endswith('trials.intervals.npy'):
        
        interval = np.load(f_name)
        
        all_intervals.append(interval)
        
    elif f_name.endswith('trials.included.npy'):
        
        included = np.load(f_name)
        
        all_included.append(included)
        
    elif f_name.endswith('spikes.times.npy'):
        
        spike_times = np.load(f_name)
        
        all_spike_times.append(spike_times)
        
    elif f_name.endswith('spikes.clusters.npy'):
        
        spike_clusters = np.load(f_name)
        
        all_spike_clusters.append(spike_clusters)
        
    elif f_name.endswith('clusters._phy_annotation.npy'):
        
        good_clusters = np.load(f_name)
        
        all_good_clusters.append(good_clusters)
        
    elif f_name.endswith('clusters.peakChannel.npy'):
        
        peak = np.load(f_name)
        
        all_peak_channels.append(peak)
        
    elif f_name.endswith('channels.brainLocation.tsv'):
        
        brain_coords = pd.read_csv(f_name,sep='\t',header=0,names=['A/P','D/V','L/R','brain_region'])
        
        brain_areas = brain_coords.brain_region
        
        brain_areas = brain_areas.tolist()
        
        all_brain_areas.append(brain_areas)

        
#%% Save relevant variables

# uncompressed .npz is about 5gb

np.savez('steinmetz_relevant_data',all_brain_areas,all_good_clusters,
          all_included,all_intervals,all_peak_channels,all_spike_clusters,
          all_spike_times)