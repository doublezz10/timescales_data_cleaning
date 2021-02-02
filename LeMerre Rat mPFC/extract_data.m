% Load in silicon probe data

spiketimes = spike_data.Cell_SpikeTimes;

spikes = cell(1,length(spiketimes));
cell_info = cell(1,length(spiketimes));

for unit = 1:length(spiketimes)
    
    spikes{unit} = spiketimes{unit}{1} / 30000;
    
    cell_number = spike_data.Cell_Number(unit);
    brain_area = 'mPFC';
    regular_spiking = spike_data.Cell_RS(unit);
    coords = spike_data.Cell_Coordinates(unit,:);
    % spike_type = 1 -> regular spiking
    % spike_type = 0 -> fast spiking
    
    cell_info{unit} = struct('dataset','LeMerre','species','rat','cell_number',cell_number,'brain_area',brain_area,'regular_spiking',regular_spiking,'coords_ML_AP_depth',coords);
    
end

save 'lemerre.mat' 'spikes' 'cell_info'