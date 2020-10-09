# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 16:46:14 2020

@author: zachz
"""

#%% Imports 

import numpy as np
import os
import pandas as pd
import scipy.io as spio

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
        
# Clean up workspace :)
        
del brain_areas, dirname, dirnames, f_name, filename, filenames, good_clusters
del included, interval, peak, root, spike_clusters, spike_times, brain_coords
del absolute_filenames

#%% Session, cluster, peak channel, brain region

good_cluster_regions = []

for session in range(len(all_good_clusters)):
    for cluster in range(len(all_good_clusters[session])):
        if all_good_clusters[session][cluster] >= 2:
            peak = int(all_peak_channels[session][cluster][0])
            brain_region = all_brain_areas[session][peak-1]
            
            good_cluster_regions.append((session,cluster,peak,brain_region))
            
# convert ugly list of tuples into pretty dataframe

good_clusters = pd.DataFrame.from_records(good_cluster_regions,columns = ['Session', 'Cluster', 'Peak Channel', 'Brain Region'])

# Clean up workspace :)

del good_cluster_regions, session, cluster, peak, brain_region

#%% Subset

# HC

subset_ca1 = good_clusters[good_clusters["Brain Region"] == 'CA1']
num_ca1_clusters = subset_ca1.count()
num_ca1_clusters = num_ca1_clusters['Brain Region']

subset_ca2 = good_clusters[good_clusters["Brain Region"] == 'CA2']
num_ca2_clusters = subset_ca2.count()
num_ca2_clusters = num_ca2_clusters['Brain Region']

subset_ca3 = good_clusters[good_clusters["Brain Region"] == 'CA3']
num_ca3_clusters = subset_ca3.count()
num_ca3_clusters = num_ca3_clusters['Brain Region']

subset_dg = good_clusters[good_clusters["Brain Region"] == 'DG']
num_dg_clusters = subset_dg.count()
num_dg_clusters = num_dg_clusters['Brain Region']

subset_ca1 = subset_ca1.reset_index(drop=True)
subset_ca2 = subset_ca2.reset_index(drop=True)
subset_ca3 = subset_ca3.reset_index(drop=True)
subset_dg = subset_dg.reset_index(drop=True)

#%% Spike times

# ca1

ca1_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_ca1.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    ca1_spikes.append(unit_spikes)
    
# ca2

ca2_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_ca2.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    ca2_spikes.append(unit_spikes)
    
# ca3

ca3_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_ca3.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    ca3_spikes.append(unit_spikes)
    
# dg

dg_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_dg.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    dg_spikes.append(unit_spikes)
    
#%% Convert all_intervals into all_itis

all_itis = []
session_iti = []

for session in range(len(all_intervals)):
            
    n_trials = len(all_intervals[session])
        
    session_iti = np.zeros((n_trials-1,2))
    
    for trial in range(len(all_intervals[session])-1):
        
        iti_start = all_intervals[session][trial,1] 
        iti_end = all_intervals[session][trial+1,0]
        
        session_iti[trial,0] = iti_start
        session_iti[trial,1] = iti_end
        
    all_itis.append(session_iti)
    
# Clean up workspace :)

del iti_start, iti_end, n_trials, session_iti, session, trial

#%% Restrict spike times to only those in ITIs

## ca1

ca1_iti_spikes = []

for unit in range(len(ca1_spikes)):
    
    unit_spikes = []
    
    session = subset_ca1['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(ca1_spikes[unit])):
            
            if ca1_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(ca1_spikes[unit][spike])
                
    ca1_iti_spikes.append(unit_spikes)
    
## ca2

ca2_iti_spikes = []

for unit in range(len(ca2_spikes)):
    
    unit_spikes = []
    
    session = subset_ca2['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(ca2_spikes[unit])):
            
            if ca2_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(ca2_spikes[unit][spike])
                
    ca2_iti_spikes.append(unit_spikes)
    
## ca3

ca3_iti_spikes = []

for unit in range(len(ca3_spikes)):
    
    unit_spikes = []
    
    session = subset_ca3['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(ca3_spikes[unit])):
            
            if ca3_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(ca3_spikes[unit][spike])
                
    ca3_iti_spikes.append(unit_spikes)
    
## dg

dg_iti_spikes = []

for unit in range(len(dg_spikes)):
    
    unit_spikes = []
    
    session = subset_dg['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(dg_spikes[unit])):
            
            if dg_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(dg_spikes[unit][spike])
                
    dg_iti_spikes.append(unit_spikes)
    
#%% Bigger .mat files: all spikes and ITI spikes

# ca1

ca1_dict = {'ca1_spikes_all': ca1_spikes}
spio.savemat('ca1_spikes.mat',ca1_dict)

ca1_iti = np.array(ca1_iti_spikes,dtype=object)
ca1_iti_dict = {'ca1_spikes_iti': ca1_iti}
spio.savemat('ca1_spikes_with_iti.mat',ca1_iti_dict)

# ca2

ca2_dict = {'ca2_spikes_all': ca2_spikes}
spio.savemat('ca2_spikes.mat',ca2_dict)

ca2_iti = np.array(ca2_iti_spikes,dtype=object)
ca2_iti_dict = {'ca2_spikes_iti': ca2_iti}
spio.savemat('ca2_spikes_with_iti.mat',ca2_iti_dict)

# ca3

ca3_dict = {'ca3_spikes_all': ca3_spikes}
spio.savemat('ca3_spikes.mat',ca3_dict)

ca3_iti = np.array(ca3_iti_spikes,dtype=object)
ca3_iti_dict = {'ca3_spikes_iti': ca3_iti}
spio.savemat('ca3_spikes_with_iti.mat',ca3_iti_dict)

# dg

dg_dict = {'dg_spikes_all': dg_spikes}
spio.savemat('dg_spikes.mat',dg_dict)

dg_iti = np.array(dg_iti_spikes,dtype=object)
dg_iti_dict = {'dg_spikes_iti': dg_iti}
spio.savemat('dg_spikes_with_iti.mat',dg_iti_dict)

#%% Make all arrays saveable

# ca1

fixed_ca1_spike_times = np.array(ca1_spikes,dtype=object)
    
np.save('ca1_spikes.npy',fixed_ca1_spike_times)

# ca2

fixed_ca2_spike_times = np.array(ca2_spikes,dtype=object)
    
np.save('ca2_spikes.npy',fixed_ca2_spike_times)

# ca3

fixed_ca3_spike_times = np.array(ca3_spikes,dtype=object)
    
np.save('ca3_spikes.npy',fixed_ca3_spike_times)

# dg

fixed_dg_spike_times = np.array(dg_spikes,dtype=object)
    
np.save('dg_spikes.npy',fixed_dg_spike_times)