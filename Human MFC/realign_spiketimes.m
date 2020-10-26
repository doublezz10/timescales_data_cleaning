%% Load in data

clear

load('D:\Human medial frontal cortex\spikes\ha.mat')
load('D:\Human medial frontal cortex\spikes\mfc.mat')

%% Loop through rows in mfc and ha structures to pull out timeseries for single cells

% MFC

mfc_units = cell(1,length(data_mfc));

for row =1:length(data_mfc)
   
    session = data_mfc(row).sessionID;
    response_ts = data_mfc(row).ts.reply;
    cluster = data_mfc(row).cellinfo(2);
    brain_area = data_mfc(row).cellinfo(3);
    
    if brain_area == 1 || brain_area == 5
        brain_area = 'amygdala';
    elseif brain_area == 2 || brain_area == 6
        brain_area = 'dorsal ACC';
    elseif brain_area == 3 || brain_area == 7
        brain_area = 'hippocampus';
    elseif brain_area == 4 || brain_area == 8
        brain_area = 'preSMA';
    end
    
    % Convert trial-aligned spike times to "raw" spike times
    % By adding 10 sec b/w each trial
    
    for trial = 1:length(response_ts)
        
        response_ts{trial} = response_ts{trial} + 10*trial; 
        
    end
    
    row_struct = struct('SessionID',session,'ClusterNumber',cluster,'BrainArea',brain_area,'SpikeTimes',response_ts);
    
    mfc_units{row} = row_struct;
    
end

% Hippocampus and amygdala

ha_units = cell(1,length(data_ha));

for row =1:length(data_ha)
   
    session = data_ha(row).sessionID;
    response_ts = data_ha(row).ts.reply;
    cluster = data_ha(row).cellinfo(2);
    brain_area = data_ha(row).cellinfo(3);
    
    spikes = cell(1,1);
    spikes{1,1} = response_ts;
    
    if brain_area == 1 || brain_area == 5 % smaller value is left, larger is right
        brain_area = 'amygdala';
    elseif brain_area == 2 || brain_area == 6
        brain_area = 'dorsal ACC';
    elseif brain_area == 3 || brain_area == 7
        brain_area = 'hippocampus';
    elseif brain_area == 4 || brain_area == 8
        brain_area = 'preSMA';
    end
    
    for trial = 1:length(response_ts)
        
        response_ts{trial} = response_ts{trial} + 10*trial;
        
    end
    
    row_struct = struct('SessionID',session,'ClusterNumber',cluster,'BrainArea',brain_area,'SpikeTimes',response_ts);
    
    ha_units{row} = row_struct;
    
end

save('human_MFC.mat','mfc_units','ha_units')

%% What does the structure look like?
%{
    Each entry is a session
    Each session contains the following information:

        Session ID - to map back to original dataset
        ClusterNumber - in case two channels had spikes from the same cell
        BrainArea - which brain region was this from?
        SpikeTimes - response-aligned spike times, each cell is a trial;
        b/c these are aligned to responses, positive values occur during
        the 1-2sec ITI

%}