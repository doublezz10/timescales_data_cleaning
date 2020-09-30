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
            
            good_cluster_regions.append((session,cluster,brain_region))
            
# convert ugly list of tuples into pretty dataframe

good_clusters = pd.DataFrame.from_records(good_cluster_regions,columns = ['Session', 'Cluster', 'Brain Region'])

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

subset_dg = good_clusters[good_clusters["Brain Region"] == 'DG']
num_dg_clusters = subset_dg.count()
num_dg_clusters = num_dg_clusters['Brain Region']

num_HC_clusters = num_ca1_clusters + num_ca2_clusters + num_dg_clusters

# Clean up workspace :)

del subset_aca, subset_orb, subset_bla, subset_ila, subset_pl, subset_ca1
del subset_ca2, subset_dg

#%% Assemble prettier dataframe with all unit counts

cluster_count = [num_ACA_clusters, num_BLA_clusters, num_HC_clusters, num_ILA_clusters, num_ORB_clusters, num_PL_clusters]
cluster_areas = ['ACA','BLA','HC','ILA','ORB','PL']

cluster_tuples = list(zip(cluster_areas,cluster_count))

unit_counts = pd.DataFrame(cluster_tuples,columns=['Brain Region','Num units'])

# Clean up workspace :)

del cluster_count, cluster_areas, cluster_tuples, num_ACA_clusters, num_BLA_clusters
del num_ca1_clusters, num_ca2_clusters, num_dg_clusters, num_HC_clusters
del num_ILA_clusters, num_ORB_clusters, num_PL_clusters

#%% Separate spike times by unit

#%% Separate long arrays of spike times per unit into separate rows per trial

# ACA units