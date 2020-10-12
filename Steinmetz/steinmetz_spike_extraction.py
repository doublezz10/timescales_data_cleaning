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
            
#%% Separate long arrays of spike times per unit into separate rows per trial

## ACA units

aca_spikes = [] # rows are units, in each row is spike times in ms
                      # row indices match row index in subset_aca dataframe

# Loop through each row of aca dataframe
# If the session and cluster match a spike from the all_spike_clusters array,
# add it to the unit_spikes
# Then create a list of all unit spikes called aca_spikes

for index, row in subset_aca.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    aca_spikes.append(unit_spikes)
    
# Clean up workspace

del index, row, session, cluster, unit_spikes, spike

## BLA units

bla_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_bla.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    bla_spikes.append(unit_spikes)
    
# Clean up workspace

del index, row, session, cluster, unit_spikes, spike

## ILA units

ila_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_ila.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    ila_spikes.append(unit_spikes)
    
# Clean up workspace

del index, row, session, cluster, unit_spikes, spike
    
## ORB units

orb_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_orb.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    orb_spikes.append(unit_spikes)
    
# Clean up workspace

del index, row, session, cluster, unit_spikes, spike

## PL units

pl_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_pl.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    pl_spikes.append(unit_spikes)
    
# CA1

ca1_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_ca1.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    ca1_spikes.append(unit_spikes)
    
# CA2

ca2_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_ca2.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    ca2_spikes.append(unit_spikes)
    
# CA3

ca3_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_ca3.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    ca3_spikes.append(unit_spikes)
    
# DG

dg_spikes = [] # rows are units, in each row is spike times in ms

for index, row in subset_dg.iterrows():
    
    session = row['Session']
    cluster = row['Cluster']
    
    unit_spikes = []
    
    for spike in range(len(all_spike_clusters[session])):
        
        if all_spike_clusters[session][spike] == cluster:
            
            unit_spikes.append(all_spike_times[session][spike][0])
            
    dg_spikes.append(unit_spikes)
    
# Clean up workspace

del index, row, session, cluster, unit_spikes, spike


#%% Restrict spike times to only those in ITIs

## ACA

aca_iti_spikes = []

for unit in range(len(aca_spikes)):
    
    unit_spikes = []
    
    session = subset_aca['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(aca_spikes[unit])):
            
            if aca_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(aca_spikes[unit][spike])
                
    aca_iti_spikes.append(unit_spikes)
    
## BLA

bla_iti_spikes = []

for unit in range(len(bla_spikes)):
    
    unit_spikes = []
    
    session = subset_bla['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(bla_spikes[unit])):
            
            if bla_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(bla_spikes[unit][spike])
                
    bla_iti_spikes.append(unit_spikes)
    
    
## ILA

ila_iti_spikes = []

for unit in range(len(ila_spikes)):
    
    unit_spikes = []
    
    session = subset_ila['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(ila_spikes[unit])):
            
            if ila_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(ila_spikes[unit][spike])
                
    ila_iti_spikes.append(unit_spikes)
    
## ORB

orb_iti_spikes = []

for unit in range(len(orb_spikes)):
    
    unit_spikes = []
    
    session = subset_orb['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(orb_spikes[unit])):
            
            if orb_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(orb_spikes[unit][spike])
                
    orb_iti_spikes.append(unit_spikes)
     
## PL

pl_iti_spikes = []

for unit in range(len(pl_spikes)):
    
    unit_spikes = []
    
    session = subset_pl['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(pl_spikes[unit])):
            
            if pl_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(pl_spikes[unit][spike])
                
    pl_iti_spikes.append(unit_spikes)
    
## CA1

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
    
## CA2

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
    
## CA3

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
    
## DG

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
    
# Clean up workspace :)

del unit, session, session_itis, unit_spikes, spike, trial

#%% Restrict spike times to only those during task

## ACA

aca_task_spikes = []

for unit in range(len(aca_spikes)):
    
    unit_spikes = []
    
    session = subset_aca['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(aca_spikes[unit])):
            
            if aca_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(aca_spikes[unit][spike])
                
    aca_task_spikes.append(unit_spikes)
    
## BLA

bla_task_spikes = []

for unit in range(len(bla_spikes)):
    
    unit_spikes = []
    
    session = subset_bla['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(bla_spikes[unit])):
            
            if bla_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(bla_spikes[unit][spike])
                
    bla_task_spikes.append(unit_spikes)
    
    
## ILA

ila_task_spikes = []

for unit in range(len(ila_spikes)):
    
    unit_spikes = []
    
    session = subset_ila['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(ila_spikes[unit])):
            
            if ila_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(ila_spikes[unit][spike])
                
    ila_task_spikes.append(unit_spikes)
    
## ORB

orb_task_spikes = []

for unit in range(len(orb_spikes)):
    
    unit_spikes = []
    
    session = subset_orb['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(orb_spikes[unit])):
            
            if orb_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(orb_spikes[unit][spike])
                
    orb_task_spikes.append(unit_spikes)
     
## PL

pl_task_spikes = []

for unit in range(len(pl_spikes)):
    
    unit_spikes = []
    
    session = subset_pl['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(pl_spikes[unit])):
            
            if pl_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(pl_spikes[unit][spike])
                
    pl_task_spikes.append(unit_spikes)
    
## CA1

ca1_task_spikes = []

for unit in range(len(ca1_spikes)):
    
    unit_spikes = []
    
    session = subset_ca1['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(ca1_spikes[unit])):
            
            if ca1_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(ca1_spikes[unit][spike])
                
    ca1_task_spikes.append(unit_spikes)
    
## CA2

ca2_task_spikes = []

for unit in range(len(ca2_spikes)):
    
    unit_spikes = []
    
    session = subset_ca2['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(ca2_spikes[unit])):
            
            if ca2_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(ca2_spikes[unit][spike])
                
    ca2_task_spikes.append(unit_spikes)

## CA3

ca3_task_spikes = []

for unit in range(len(ca3_spikes)):
    
    unit_spikes = []
    
    session = subset_ca3['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(ca3_spikes[unit])):
            
            if ca3_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(ca3_spikes[unit][spike])
                
    ca3_task_spikes.append(unit_spikes)
    
## DG

dg_task_spikes = []

for unit in range(len(dg_spikes)):
    
    unit_spikes = []
    
    session = subset_dg['Session'][unit]
    
    session_intervals = all_included_intervals[session]
    
    for trial in range(len(session_intervals)):
        
        for spike in range(len(dg_spikes[unit])):
            
            if dg_spikes[unit][spike] <= session_intervals[trial][1] and spike >= session_intervals[trial][0]:
                
                unit_spikes.append(dg_spikes[unit][spike])
                
    dg_task_spikes.append(unit_spikes)
    
    
# Clean up workspace :)

del unit, session, session_intervals, unit_spikes, spike, trial

#%% Save arrays as numpy

# ACA

aca_spikes = np.array(aca_spikes,dtype=object)
aca_iti_spikes = np.array(aca_iti_spikes,dtype=object)
aca_task_spikes = np.array(aca_task_spikes,dtype=object)

np.save('aca_all_spikes.npy',aca_spikes)
np.save('aca_iti_spikes.npy',aca_iti_spikes)
np.save('aca_task_spikes.npy',aca_task_spikes)

# BLA

bla_spikes = np.array(bla_spikes,dtype=object)
bla_iti_spikes = np.array(bla_iti_spikes,dtype=object)
bla_task_spikes = np.array(bla_task_spikes,dtype=object)

np.save('bla_all_spikes.npy',bla_spikes)
np.save('bla_iti_spikes.npy',bla_iti_spikes)
np.save('bla_task_spikes.npy',bla_task_spikes)

# ILA

ila_spikes = np.array(ila_spikes,dtype=object)
ila_iti_spikes = np.array(ila_iti_spikes,dtype=object)
ila_task_spikes = np.array(ila_task_spikes,dtype=object)

np.save('ila_all_spikes.npy',ila_spikes)
np.save('ila_iti_spikes.npy',ila_iti_spikes)
np.save('ila_task_spikes.npy',ila_task_spikes)

# ORB

orb_spikes = np.array(orb_spikes,dtype=object)
orb_iti_spikes = np.array(orb_iti_spikes,dtype=object)
orb_task_spikes = np.array(orb_task_spikes,dtype=object)

np.save('orb_all_spikes.npy',orb_spikes)
np.save('orb_iti_spikes.npy',orb_iti_spikes)
np.save('orb_task_spikes.npy',orb_task_spikes)

# PL

pl_spikes = np.array(pl_spikes,dtype=object)
pl_iti_spikes = np.array(pl_iti_spikes,dtype=object)
pl_task_spikes = np.array(pl_task_spikes,dtype=object)

np.save('pl_all_spikes.npy',pl_spikes)
np.save('pl_iti_spikes.npy',pl_iti_spikes)
np.save('pl_task_spikes.npy',pl_task_spikes)

# CA1

ca1_spikes = np.array(ca1_spikes,dtype=object)
ca1_iti_spikes = np.array(ca1_iti_spikes,dtype=object)
ca1_task_spikes = np.array(ca1_task_spikes,dtype=object)

np.save('ca1_all_spikes.npy',ca1_spikes)
np.save('ca1_iti_spikes.npy',ca1_iti_spikes)
np.save('ca1_task_spikes.npy',ca1_task_spikes)

# CA2

ca2_spikes = np.array(ca2_spikes,dtype=object)
ca2_iti_spikes = np.array(ca2_iti_spikes,dtype=object)
ca2_task_spikes = np.array(ca2_task_spikes,dtype=object)

np.save('ca2_all_spikes.npy',ca2_spikes)
np.save('ca2_iti_spikes.npy',ca2_iti_spikes)
np.save('ca2_task_spikes.npy',ca2_task_spikes)

# CA3

ca3_spikes = np.array(ca3_spikes,dtype=object)
ca3_iti_spikes = np.array(ca3_iti_spikes,dtype=object)
ca3_task_spikes = np.array(ca3_task_spikes,dtype=object)

np.save('ca3_all_spikes.npy',ca3_spikes)
np.save('ca3_iti_spikes.npy',ca3_iti_spikes)
np.save('ca3_task_spikes.npy',ca3_task_spikes)

# DG

dg_spikes = np.array(dg_spikes,dtype=object)
dg_iti_spikes = np.array(dg_iti_spikes,dtype=object)
dg_task_spikes = np.array(dg_task_spikes,dtype=object)

np.save('dg_all_spikes.npy',dg_spikes)
np.save('dg_iti_spikes.npy',dg_iti_spikes)
np.save('dg_task_spikes.npy',dg_task_spikes)

#%% Save MATLAB files

# ACA

aca_task_dict = {'aca_task': aca_task_spikes}
aca_iti_dict = {'aca_iti': aca_iti_spikes}
spio.savemat('aca_iti.mat',aca_iti_dict)
spio.savemat('aca_task.mat',aca_task_dict)

# BLA

bla_task_dict = {'bla_task': bla_task_spikes}
bla_iti_dict = {'bla_iti': bla_iti_spikes}
spio.savemat('bla_iti.mat',bla_iti_dict)
spio.savemat('bla_task.mat',bla_task_dict)

# ILA

ila_task_dict = {'ila_task': ila_task_spikes}
ila_iti_dict = {'ila_iti': ila_iti_spikes}
spio.savemat('ila_iti.mat',ila_iti_dict)
spio.savemat('ila_task.mat',ila_task_dict)

# ORB

orb_task_dict = {'orb_task': orb_task_spikes}
orb_iti_dict = {'orb_iti': orb_iti_spikes}
spio.savemat('orb_iti.mat',orb_iti_dict)
spio.savemat('orb_task.mat',orb_task_dict)

# PL

pl_task_dict = {'pl_task': pl_task_spikes}
pl_iti_dict = {'pl_iti': pl_iti_spikes}
spio.savemat('pl_iti.mat',pl_iti_dict)
spio.savemat('pl_task.mat',pl_task_dict)

# CA1

ca1_task_dict = {'ca1_task': ca1_task_spikes}
ca1_iti_dict = {'ca1_iti': ca1_iti_spikes}
spio.savemat('ca1_iti.mat',ca1_iti_dict)
spio.savemat('ca1_task.mat',ca1_task_dict)

# CA2

ca2_task_dict = {'ca2_task': ca2_task_spikes}
ca2_iti_dict = {'ca2_iti': ca2_iti_spikes}
spio.savemat('ca2_iti.mat',ca2_iti_dict)
spio.savemat('ca2_task.mat',ca2_task_dict)

# CA3

ca3_task_dict = {'ca3_task': ca3_task_spikes}
ca3_iti_dict = {'ca3_iti': ca3_iti_spikes}
spio.savemat('ca3_iti.mat',ca3_iti_dict)
spio.savemat('ca3_task.mat',ca3_task_dict)

# DG

dg_task_dict = {'dg_task': dg_task_spikes}
dg_iti_dict = {'dg_iti': dg_iti_spikes}
spio.savemat('dg_iti.mat',dg_iti_dict)
spio.savemat('dg_task.mat',dg_task_dict)