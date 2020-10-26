%% Load data

clear

load('human_MFC.mat')
load('ha_spiketimes.mat')
load('mfc_spiketimes.mat')

cell_info_hc = {};
cell_info_amygdala = {};
cell_info_dACC = {};
cell_info_preSMA = {};

task_hc = {};
task_amygdala = {};
task_dACC = {};
task_preSMA = {};

%% loop through each unit, extracting relevant cell_info and spike times

for unit = 1:length(ha_units)

    field1 = 'Dataset'; value1 = 'Minxha';
    field2 = 'Species'; value2 = 'human';
    field3 = 'Brain_Area'; value3 = ha_units{unit}(1).BrainArea;
    field4 = 'Cluster'; value4 = ha_units{unit}(1).ClusterNumber;
    
    all_spikes = ha_spiketimes{unit};
    
    if strcmp(ha_units{unit}(1).BrainArea,'hippocampus') == 1
        cell_info_hc{end+1} = struct(field1,value1,field2,value2,field3,value3,field4,value4);
        task_hc{end+1} = single(all_spikes);
    elseif strcmp(ha_units{unit}(1).BrainArea,'amygdala') == 1
        cell_info_amygdala{end+1} = struct(field1,value1,field2,value2,field3,value3,field4,value4);
        task_amygdala{end+1} = single(all_spikes);
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
        task_dACC{end+1} = single(all_spikes);
    elseif strcmp(mfc_units{unit}(1).BrainArea,'preSMA') == 1
        cell_info_preSMA{end+1} = struct(field1,value1,field2,value2,field3,value3,field4,value4);
        task_preSMA{end+1} = single(all_spikes);
    end
end

%% Save .mat files

task = task_dACC; cell_info = cell_info_dACC;
save('dACC.mat','task','cell_info')

task = task_preSMA; cell_info = cell_info_preSMA;
save('preSMA.mat','task','cell_info')

task = task_hc; cell_info = cell_info_hc;
save('hippocampus.mat','task','cell_info')

task = task_amygdala; cell_info = cell_info_amygdala;
save('amygdala.mat','task','cell_info')