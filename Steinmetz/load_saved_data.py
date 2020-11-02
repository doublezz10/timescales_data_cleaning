# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 10:49:33 2020

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

#%% Loop through good clusters. If a cluster is good, assign its brain area in
#   a new array of paired cluster numbers and brain areas

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

#%% Count number of clusters (i.e. units) for each brain area of interest

# ACA

subset_aca = good_clusters[good_clusters["Brain Region"] == 'ACA']
num_ACA_clusters = subset_aca.count()
num_ACA_clusters = num_ACA_clusters['Brain Region']

# ORB

subset_orb = good_clusters[good_clusters["Brain Region"] == 'ORB']
num_ORB_clusters = subset_aca.count()
num_ORB_clusters = num_ORB_clusters['Brain Region']

# BLA

subset_bla = good_clusters[good_clusters["Brain Region"] == 'BLA']
num_BLA_clusters = subset_bla.count()
num_BLA_clusters = num_BLA_clusters['Brain Region']

# ILA

subset_ila = good_clusters[good_clusters["Brain Region"] == 'ILA']
num_ILA_clusters = subset_ila.count()
num_ILA_clusters = num_ILA_clusters['Brain Region']

# PL

subset_pl = good_clusters[good_clusters["Brain Region"] == 'PL']
num_PL_clusters = subset_pl.count()
num_PL_clusters = num_PL_clusters['Brain Region']
  
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

subset_hc = subset_ca1.append([subset_ca2,subset_ca3,subset_dg],ignore_index=True)

num_HC_clusters = num_ca1_clusters + num_ca2_clusters + num_ca3_clusters + num_dg_clusters

# Renumber indices in each dataframe

subset_aca = subset_aca.reset_index(drop=True)
subset_bla = subset_bla.reset_index(drop=True)
subset_hc = subset_hc.reset_index(drop=True)
subset_ila = subset_ila.reset_index(drop=True)
subset_orb = subset_orb.reset_index(drop=True)
subset_pl = subset_pl.reset_index(drop=True)
subset_ca1 = subset_ca1.reset_index(drop=True)
subset_ca2 = subset_ca2.reset_index(drop=True)
subset_ca3 = subset_ca3.reset_index(drop=True)
subset_dg = subset_dg.reset_index(drop=True)


# Assemble prettier dataframe with all unit counts

cluster_count = [num_ACA_clusters, num_BLA_clusters, num_ILA_clusters, num_ORB_clusters, num_PL_clusters, num_HC_clusters, num_ca1_clusters, num_ca2_clusters, num_ca3_clusters, num_dg_clusters]
cluster_areas = ['ACA','BLA','ILA','ORB','PL','all_HC','CA1','CA2','CA3','DG']

cluster_tuples = list(zip(cluster_areas,cluster_count))

unit_counts = pd.DataFrame(cluster_tuples,columns=['Brain Region','Num units'])

# Clean up workspace :)

del cluster_count, cluster_areas, cluster_tuples, num_ACA_clusters, num_BLA_clusters
del num_ca1_clusters, num_ca2_clusters, num_ca3_clusters, num_dg_clusters, num_HC_clusters
del num_ILA_clusters, num_ORB_clusters, num_PL_clusters

#%% Remove trial/ITI intervals which were not included

all_included_intervals = []

for session in range(len(all_included)):
    
    session_intervals = []

    for trial in range(len(all_included[session])):
        
        if all_included[session][trial] == True:
            
            interval = all_intervals[session][trial]
            
            session_intervals.append(interval)
    
    all_included_intervals.append(session_intervals)
    
# Clean up workspace :)

del session, session_intervals, trial, interval, all_intervals, all_included

#%% Load in numpy files

# ACA

aca_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/aca_all_spikes.npy',allow_pickle=True)
aca_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/aca_iti_spikes.npy',allow_pickle=True)
aca_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/aca_task_spikes.npy',allow_pickle=True)

# BLA

bla_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/bla_all_spikes.npy',allow_pickle=True)
bla_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/bla_iti_spikes.npy',allow_pickle=True)
bla_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/bla_task_spikes.npy',allow_pickle=True)


# CA1

ca1_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca1_all_spikes.npy',allow_pickle=True)
ca1_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca1_iti_spikes.npy',allow_pickle=True)
ca1_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca1_task_spikes.npy',allow_pickle=True)


# CA2

ca2_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca2_all_spikes.npy',allow_pickle=True)
ca2_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca2_iti_spikes.npy',allow_pickle=True)
ca2_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca2_task_spikes.npy',allow_pickle=True)


# CA3

ca3_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca3_all_spikes.npy',allow_pickle=True)
ca3_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca3_iti_spikes.npy',allow_pickle=True)
ca3_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ca3_task_spikes.npy',allow_pickle=True)


# DG

dg_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/dg_all_spikes.npy',allow_pickle=True)
dg_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/dg_iti_spikes.npy',allow_pickle=True)
dg_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/dg_task_spikes.npy',allow_pickle=True)


# ILA

ila_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ila_all_spikes.npy',allow_pickle=True)
ila_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ila_iti_spikes.npy',allow_pickle=True)
ila_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/ila_task_spikes.npy',allow_pickle=True)


# ORB

orb_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/orb_all_spikes.npy',allow_pickle=True)
orb_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/orb_iti_spikes.npy',allow_pickle=True)
orb_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/orb_task_spikes.npy',allow_pickle=True)


# PL

pl_all = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/pl_all_spikes.npy',allow_pickle=True)
pl_iti = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/pl_iti_spikes.npy',allow_pickle=True)
pl_task = np.load('D:/timescales_data_cleaning/Steinmetz/npy files/pl_task_spikes.npy',allow_pickle=True)
