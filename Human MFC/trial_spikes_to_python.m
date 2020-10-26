load('human_MFC.mat')    

all_mfc_units_trialspikes = cell(1,length(mfc_units));

for unit = 1:length(mfc_units)
        
    mfc_trial_spikes = cell(1,length(mfc_units{unit}));

    for trial = 1:length(mfc_units{unit})

        mfc_trial_spikes{trial} = mfc_units{unit}(trial).SpikeTimes;

    end

    all_mfc_units_trialspikes{unit} = mfc_trial_spikes;
end

all_ha_units_trialspikes = cell(1,length(ha_units));

for unit = 1:length(ha_units)

   ha_trial_spikes = cell(1,length(ha_units{unit}));

   for trial = 1:length(ha_units{unit})

       ha_trial_spikes{trial} = ha_units{unit}(trial).SpikeTimes;

   end
   
   all_ha_units_trialspikes{unit} = ha_trial_spikes;

end

save('trial_spikes.mat','all_mfc_units_trialspikes','all_ha_units_trialspikes')