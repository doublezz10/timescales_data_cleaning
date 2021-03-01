% important_data = col 1: brain_area
%                  col 2: session_number
%                  col 3: spiketimes (converted to sec, 0-aligned)

important_data = cell(3,length(cellStatsAll));

for unit = 1:length(cellStatsAll)
    
    important_data{1,unit} = cellStatsAll(unit).brainAreaOfCell;
    important_data{2,unit} = cellStatsAll(unit).NOind;
    important_data{3,unit} = (cellStatsAll(unit).timestamps - cellStatsAll(unit).timestamps(1)) / 10^9;
    
end

cell_info_hc = {};
spikes_hc = {};

cell_info_amygdala = {};
spikes_amygdala = {};

for unit = 1:length(important_data)
    
    if important_data{1,unit} == 1
    
        cell_info_hc{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','hippocampus','session',important_data{2,unit},'hemisphere','l');
        spikes_hc{end+1} = important_data{3,unit};
        
    elseif important_data{1,unit} == 2
        
        cell_info_hc{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','hippocampus','session',important_data{2,unit},'hemisphere','r');
        spikes_hc{end+1} = important_data{3,unit};
        
    elseif important_data{1,unit} == 3
        
        cell_info_amygdala{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','amygdala','session',important_data{2,unit},'hemisphere','l');
        spikes_amygdala{end+1} = important_data{3,unit};
        
    elseif important_data{1,unit} == 4
        
        cell_info_amygdala{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','amygdala','session',important_data{2,unit},'hemisphere','r');
        spikes_amygdala{end+1} = important_data{3,unit};
        
    end
    
end

% Save spiketimes only!

spikes = spikes_hc;
cell_info = cell_info_hc;

save('faraut_hippocampus.mat','spikes','cell_info')

spikes = spikes_amygdala;
cell_info = cell_info_amygdala;

save('faraut_amygdala.mat','spikes','cell_info')
