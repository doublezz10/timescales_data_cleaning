# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:23:58 2020

@author: zachz
"""

#%% Imports 

import numpy as np
import scipy.io as spio
import pandas as pd
import os

#%% Loading

aca_spikes = np.load('aca_spikes.npy',allow_pickle=True)
bla_spikes = np.load('bla_spikes.npy',allow_pickle=True)
hc_spikes = np.load('hc_spikes.npy',allow_pickle=True)
ila_spikes = np.load('ila_spikes.npy',allow_pickle=True)
orb_spikes = np.load('orb_spikes.npy',allow_pickle=True)
pl_spikes = np.load('pl_spikes.npy',allow_pickle=True)

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

# Clean up workspace :)

del subset_ca1, subset_ca2, subset_ca3, subset_dg

# Assemble prettier dataframe with all unit counts

cluster_count = [num_ACA_clusters, num_BLA_clusters, num_HC_clusters, num_ILA_clusters, num_ORB_clusters, num_PL_clusters]
cluster_areas = ['ACA','BLA','HC','ILA','ORB','PL']

cluster_tuples = list(zip(cluster_areas,cluster_count))

unit_counts = pd.DataFrame(cluster_tuples,columns=['Brain Region','Num units'])

# Clean up workspace :)

del cluster_count, cluster_areas, cluster_tuples, num_ACA_clusters, num_BLA_clusters
del num_ca1_clusters, num_ca2_clusters, num_ca3_clusters, num_dg_clusters, num_HC_clusters
del num_ILA_clusters, num_ORB_clusters, num_PL_clusters


#%% Delete extraneous variables

del all_brain_areas, all_good_clusters, all_included, all_intervals
del all_peak_channels, all_spike_clusters,all_spike_times, good_clusters

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
    
## HC

hc_iti_spikes = []

for unit in range(len(hc_spikes)):
    
    unit_spikes = []
    
    session = subset_hc['Session'][unit]
    
    session_itis = all_itis[session]
    
    for trial in range(len(session_itis)):
        
        for spike in range(len(hc_spikes[unit])):
            
            if hc_spikes[unit][spike] <= session_itis[trial,1] and spike >= session_itis[trial,0]:
                
                unit_spikes.append(hc_spikes[unit][spike])
                
    hc_iti_spikes.append(unit_spikes)
    
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
    
# Clean up workspace :)

del unit, session, session_itis, unit_spikes, spike, trial

#%% Bigger .mat files: all spikes and ITI spikes

# ACA

aca_dict = {'aca_spikes_all': aca_spikes}
spio.savemat('aca_spikes.mat',aca_dict)

aca_iti = np.array(aca_iti_spikes,dtype=object)
aca_iti_dict = {'aca_spikes_iti': aca_iti}
spio.savemat('aca_spikes_with_iti.mat',aca_iti_dict)

# BLA

bla_dict = {'bla_spikes_all': bla_spikes}
spio.savemat('bla_spikes.mat',bla_dict)

bla_iti = np.array(bla_iti_spikes,dtype=object)
bla_iti_dict = {'bla_spikes_iti': bla_iti}
spio.savemat('bla_spikes_with_iti.mat',bla_iti_dict)

# HC - had to split in half because so big

hc_dict = {'hc_spikes_all': hc_spikes}
spio.savemat('hc_spikes.mat',hc_dict)

hc_iti = np.array(hc_iti_spikes,dtype=object)
hc_iti_dict = {'hc_spikes_iti': hc_iti}

hc_iti_dict_1 = dict(list(hc_iti_dict.items())[len(hc_iti_dict)//2:]) 
hc_iti_dict_2 = dict(list(hc_iti_dict.items())[:len(hc_iti_dict)//2]) 
# spio.savemat('hc_spikes_with_iti_1.mat',hc_iti_dict_1)
# spio.savemat('hc_spikes_with_iti_2.mat',hc_iti_dict_2)

# ILA

ila_dict = {'ila_spikes_all': ila_spikes}
spio.savemat('ila_spikes.mat',ila_dict)

ila_iti = np.array(ila_iti_spikes,dtype=object)
ila_iti_dict = {'ila_spikes_iti': ila_iti}
spio.savemat('ila_spikes_with_iti.mat',ila_iti_dict)

# ORB

orb_dict = {'orb_spikes_all': orb_spikes}
spio.savemat('orb_spikes.mat',orb_dict)

orb_iti = np.array(orb_iti_spikes,dtype=object)
orb_iti_dict = {'orb_spikes_iti': orb_iti}
spio.savemat('orb_spikes_with_iti.mat',orb_iti_dict)

# PL

pl_dict = {'pl_spikes_all': pl_spikes}
spio.savemat('pl_spikes.mat',pl_dict)

pl_iti = np.array(pl_iti_spikes,dtype=object)
pl_iti_dict = {'pl_spikes_iti': pl_iti}
spio.savemat('pl_spikes_with_iti.mat',pl_iti_dict)

#%% Save ITIs for each session

iti_dict = {'ITIs': all_itis}
spio.savemat('itis_by_session.mat',iti_dict)