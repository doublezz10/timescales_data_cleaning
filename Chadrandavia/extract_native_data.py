#%%

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 11:45:16 2021

@author: zachz
"""

import numpy as np
import scipy.io as spio
import os
import os.path
import hdf5storage
import pandas as pd

TIME_SCALING = 10**6

def extra_brain_area(brain_area_mat, channel_id):
    area_mapping = {1: 'RH', 2: 'LH', 3: 'RA', 4: 'LA', 13: 'LH', 18: 'RH'}
    brain_area = [brain_area_mat['brainArea'][:, 0] == channel_id, 3][0]
    return area_mapping[brain_area]

area_mapping = {1: 'RH', 2: 'LH', 3: 'RA', 4: 'LA', 13: 'LH', 18: 'RH'}

# Get Unit data
all_spike_cluster_ids = []
all_selected_time_stamps = []
all_channel_id = []
all_oriClusterIDs = []
all_channel_numbers = []
all_brain_area = []
all_sessions = []

path_to_data = '/Users/zachz/Downloads/NativeData'

sessions = [name for name in os.listdir('/Users/zachz/Downloads/NativeData/Data/Sorted')]
sessions.pop(13)

for session in range(len(sessions)):

    brain_area_file_path = os.path.join(path_to_data, 'Data', 'events', sessions[session],'NO', 'brainArea.mat')
    spikes_file_path = os.path.join(path_to_data, 'Data', 'sorted', sessions[session],'NO')
    
    brain_area_mat = spio.loadmat(brain_area_file_path)
                
    brain_areas = np.array(brain_area_mat['brainArea'])
                
    unit_id = 0
    
    channel_ids = os.listdir(spikes_file_path)
    
    for channel_id in channel_ids:
        
        cell_file_path = os.path.join(spikes_file_path, channel_id)
        
        cell_mat = spio.loadmat(cell_file_path)
        
        spikes = cell_mat['spikes']

        spike_cluster_id = np.asarray([spike[1] for spike in spikes]) # Each Cluster ID of the spike
        spike_timestamps = (np.asarray([spike[2] for spike in spikes]))/(TIME_SCALING) # Timestamps of spikes for each ClusterID
        unique_cluster_ids = np.unique(spike_cluster_id)


        # If there are more than one cluster.
        for id in unique_cluster_ids:

            # Grab brain area
            brain_area_row = brain_areas[brain_areas[:,2] == int(id)]
            
            if len(brain_area_row) > 0:
            
                brain_area_id = brain_area_row[0,3]
                            
                brain_area = area_mapping[brain_area_id]
    
                selected_spike_timestamps = spike_timestamps[spike_cluster_id == id]
    
                # Append unit data
                all_spike_cluster_ids.append(id)
                all_selected_time_stamps.append(selected_spike_timestamps)
                all_channel_id.append(channel_id)
                all_oriClusterIDs.append(int(id))
                all_channel_numbers.append(channel_id)
                all_brain_area.append(brain_area)
                all_sessions.append(sessions[session])

            unit_id += 1
            
hc_cell_info = []
hc_spikes = []

amyg_cell_info = []
amyg_spikes = []
            
for unit in range(len(all_selected_time_stamps)):
    
    if (all_brain_area[unit] == 'LH') | (all_brain_area[unit] == 'RH'):
        
        hc_cell_info.append(('Chandravadia','human','hippocampus',unit,all_sessions[unit],all_channel_id[unit],all_oriClusterIDs[unit]))
        
        hc_spikes.append(all_selected_time_stamps[unit])
        
    elif (all_brain_area[unit] == 'LA') | (all_brain_area[unit] == 'RA'):
        
        amyg_cell_info.append(('Chandravadia','human','amygdala',unit,all_sessions[unit],all_channel_id[unit],all_oriClusterIDs[unit]))
        
        amyg_spikes.append(all_selected_time_stamps[unit])
        
hc_cell_info = pd.DataFrame(hc_cell_info,columns=['Dataset','species','brain_area','unit_n','session','channel_id','original_cluster_id'])

amyg_cell_info = pd.DataFrame(amyg_cell_info,columns=['Dataset','species','brain_area','unit_n','session','channel_id','original_cluster_id'])

hc_cell_info.to_csv('/Users/zachz/Documents/timescales_analysis/1000iter results/by_individual/chadrandavia_hc_map.csv')
amyg_cell_info.to_csv('/Users/zachz/Documents/timescales_analysis/1000iter results/by_individual/chadrandavia_amyg_map.csv')
# %%
