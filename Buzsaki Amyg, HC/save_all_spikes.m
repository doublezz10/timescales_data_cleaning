% BLA

for unit = 1:length(bla_spikes)
    
    bla_spikes{unit} = bla_spikes{unit}.';
    
end

spikes = bla_spikes;
cell_info = bla_cell_info;

save 'buzsaki_bla.mat' spikes cell_info

% Central nucleus of amygdala

for unit = 1:length(central_spikes)
    
    central_spikes{unit} = central_spikes{unit}.';
    
end

spikes = central_spikes;
cell_info = central_cell_info;

save 'buzsaki_central.mat' spikes cell_info

% Hippocampus

for unit = 1:length(hippocampus_spikes)
    
    hippocampus_spikes{unit} = hippocampus_spikes{unit}.';
    
end

spikes = hippocampus_spikes;
cell_info = hippocampus_cell_info;

save 'buzsaki_hippocampus.mat' spikes cell_info