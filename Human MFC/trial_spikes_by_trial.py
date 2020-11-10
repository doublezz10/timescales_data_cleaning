# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 12:00:31 2020

@author: zachz
"""

#%% Imports

import numpy as np
import scipy.io as spio

#%% Load in .mat

trial_spikes = spio.loadmat('/Users/zachz/Downloads/trial_spikes_no_realign.mat',simplify_cells=True)

ha_trial_spikes = trial_spikes['all_ha_units_trialspikes']
mfc_trial_spikes = trial_spikes['all_mfc_units_trialspikes']

#%% hstack

ha_by_trial = []

for unit in range(len(ha_trial_spikes)):
    
    unit_by_trial = ha_trial_spikes[unit]
    
    ha_by_trial.append(unit_by_trial)
    
mfc_by_trial = []

for unit in range(len(mfc_trial_spikes)):
    
    unit_by_trial = mfc_trial_spikes[unit]
    
    mfc_by_trial.append(unit_by_trial)
    
#%% Make dictionaries

ha_dict = {'ha_spiketimes': ha_by_trial}
mfc_dict = {'mfc_spiketimes': mfc_by_trial}
    
#%% Resave as mat

spio.savemat('ha_spiketimes_by_trial.mat',ha_dict)
spio.savemat('mfc_spiketimes_by_trial.mat',mfc_dict)