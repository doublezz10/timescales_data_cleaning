# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:29:47 2020

@author: zachz
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
all_ap_coords = []
all_dv_coords = []
all_lr_coords = []

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
        
        brain_coords = pd.read_csv(f_name,sep='\t',header=0,names=['A_P','D_V','L_R','brain_region'])
        
        brain_areas = brain_coords.brain_region
        ant_post = brain_coords.A_P
        dors_vent = brain_coords.D_V
        left_right = brain_coords.L_R
        
        
        brain_areas = brain_areas.tolist()
        ant_post = ant_post.tolist()
        dors_vent = dors_vent.tolist()
        left_right = left_right.tolist()
        
        all_brain_areas.append(brain_areas)
        all_ap_coords.append(ant_post)
        all_dv_coords.append(dors_vent)
        all_lr_coords.append(left_right)
        
# Clean up workspace :)
        
del brain_areas, dirname, dirnames, f_name, filename, filenames, good_clusters
del included, interval, peak, root, spike_clusters, spike_times, brain_coords
del absolute_filenames, ant_post, dors_vent, left_right

#%% Loop through good clusters. If a cluster is good, assign its brain area in
#   a new array of paired cluster numbers and brain areas

good_cluster_regions = []

for session in range(len(all_good_clusters)):
    for cluster in range(len(all_good_clusters[session])):
        if all_good_clusters[session][cluster] >= 2:
            peak = int(all_peak_channels[session][cluster][0])
            brain_region = all_brain_areas[session][peak-1]
            ap_pos = all_ap_coords[session][peak-1]
            dv_pos = all_dv_coords[session][peak-1]
            lr_pos = all_lr_coords[session][peak-1]
            
            good_cluster_regions.append((session,cluster,peak,brain_region,ap_pos,dv_pos,lr_pos))
            
# convert ugly list of tuples into pretty dataframe

location_info = pd.DataFrame.from_records(good_cluster_regions,columns = ['Session', 'Cluster', 'Peak Channel', 'Brain Region', 'A/P', 'D/V', 'L/R'])

# Clean up workspace :)

del good_cluster_regions, session, cluster, peak, brain_region, ap_pos, dv_pos, lr_pos
del all_ap_coords, all_dv_coords, all_lr_coords, all_brain_areas, all_included
del all_intervals, all_spike_times

#%% Subset location_info by brain area

aca_locations = location_info[location_info["Brain Region"] == 'ACA']
bla_locations = location_info[location_info["Brain Region"] == 'BLA']
ila_locations = location_info[location_info["Brain Region"] == 'ILA']
orb_locations = location_info[location_info["Brain Region"] == 'ORB']
pl_locations = location_info[location_info["Brain Region"] == 'PL']
ca1_locations = location_info[location_info["Brain Region"] == 'CA1']
ca2_locations = location_info[location_info["Brain Region"] == 'CA2']
ca3_locations = location_info[location_info["Brain Region"] == 'CA3']
dg_locations = location_info[location_info["Brain Region"] == 'DG']

#%% Save location info as .mat

aca_locations.to_csv('aca_locations.csv')
bla_locations.to_csv('bla_locations.csv')
ila_locations.to_csv('ila_locations.csv')
orb_locations.to_csv('orb_locations.csv')
pl_locations.to_csv('pl_locations.csv')
ca1_locations.to_csv('ca1_locations.csv')
ca2_locations.to_csv('ca2_locations.csv')
ca3_locations.to_csv('ca3_locations.csv')
dg_locations.to_csv('dg_locations.csv')