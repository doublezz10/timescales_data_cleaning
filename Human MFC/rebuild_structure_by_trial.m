%% Load data

clear

load('human_MFC.mat')
load('ha_spiketimes_by_trial.mat')
load('mfc_spiketimes_by_trial.mat')

cell_info_hc = {};
cell_info_amygdala = {};
cell_info_dACC = {};
cell_info_preSMA = {};

spiketimes_hc = {};
spiketimes_amygdala = {};
spiketimes_dACC = {};
spiketimes_preSMA = {};

%% loop through each unit, extracting relevant cell_info and spike times

for unit = 1:length(ha_units)

    field1 = 'Dataset'; value1 = 'Minxha';
    field2 = 'Species'; value2 = 'human';
    field3 = 'Brain_Area'; value3 = ha_units{unit}(1).BrainArea;
    field4 = 'Cluster'; value4 = ha_units{unit}(1).ClusterNumber;
    
    all_spikes = ha_spiketimes{unit};
    
    if strcmp(ha_units{unit}(1).BrainArea,'hippocampus') == 1
        cell_info_hc{end+1} = struct(field1,value1,field2,value2,field3,value3,field4,value4);
        spiketimes_hc{end+1} = all_spikes;
    elseif strcmp(ha_units{unit}(1).BrainArea,'amygdala') == 1
        cell_info_amygdala{end+1} = struct(field1,value1,field2,value2,field3,value3,field4,value4);
        spiketimes_amygdala{end+1} = all_spikes;
    end
end

for unit = 1:length(mfc_units)

    field1 = 'Dataset'; value1 = 'Minxha';
    field2 = 'Species'; value2 = 'human';
    field3 = 'Brain_Area'; value3 = mfc_units{unit}(1).BrainArea;
    field4 = 'Cluster'; value4 = mfc_units{unit}(1).ClusterNumber;
    
    all_spikes = mfc_spiketimes{unit};
    
    if strcmp(mfc_units{unit}(1).BrainArea,'dorsal ACC') == 1
        cell_info_dACC{end+1} = struct(field1,value1,field2,value2,field3,value3,field4,value4);
        spiketimes_dACC{end+1} = all_spikes;
    elseif strcmp(mfc_units{unit}(1).BrainArea,'preSMA') == 1
        cell_info_preSMA{end+1} = struct(field1,value1,field2,value2,field3,value3,field4,value4);
        spiketimes_preSMA{end+1} = all_spikes;
    end
end

%% Save .mat files

spikes = spiketimes_dACC; cell_info = cell_info_dACC;
save('dACC.mat','spikes','cell_info')

spikes = spiketimes_preSMA; cell_info = cell_info_preSMA;
save('preSMA.mat','spikes','cell_info')

spikes = spiketimes_hc; cell_info = cell_info_hc;
save('hippocampus.mat','spikes','cell_info')

spikes = spiketimes_amygdala; cell_info = cell_info_amygdala;
save('amygdala.mat','spikes','cell_info')