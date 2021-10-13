% BLA

for unit = 1:length(bla_spikes)
    
    bla_spikes{unit} = bla_spikes{unit}.';
    bla_spikes2{unit} = bla_spikes2{unit}.';
    bla_sleep_spikes{unit} = bla_sleep_spikes{unit}.';
    bla_sleep_spikes2{unit} = bla_sleep_spikes2{unit}.';
end

spikes = bla_spikes;
spikes2 = bla_spikes2;
sleep_spikes = bla_sleep_spikes;
sleep_spikes2 = bla_sleep_spikes2;

cell_info = bla_cell_info;

save 'buzsaki_bla.mat' spikes spikes2 sleep_spikes sleep_spikes2 cell_info

% Central nucleus of amygdala

for unit = 1:length(central_spikes)
    
    central_spikes{unit} = central_spikes{unit}.';
    central_spikes2{unit} = central_spikes2{unit}.';
    central_sleep_spikes{unit} = central_sleep_spikes{unit}.';
    central_sleep_spikes2{unit} = central_sleep_spikes2{unit}.';
end

spikes = central_spikes;
spikes2 = central_spikes2;
sleep_spikes = central_sleep_spikes;
sleep_spikes2 = central_sleep_spikes2;

cell_info = central_cell_info;

save 'buzsaki_central.mat' spikes spikes2 sleep_spikes sleep_spikes2 cell_info

% Hippocampus

for unit = 1:length(hippocampus_spikes)
    
    hippocampus_spikes{unit} = hippocampus_spikes{unit}.';
    hippocampus_spikes2{unit} = hippocampus_spikes2{unit}.';
    hippocampus_sleep_spikes{unit} = hippocampus_sleep_spikes{unit}.';
    hippocampus_sleep_spikes2{unit} = hippocampus_sleep_spikes2{unit}.';
end

spikes = hippocampus_spikes;
spikes2 = hippocampus_spikes2;
sleep_spikes = hippocampus_sleep_spikes;
sleep_spikes2 = hippocampus_sleep_spikes2;

cell_info = hippocampus_cell_info;

save 'buzsaki_hippocampus.mat' spikes cell_info spikes spikes2 sleep_spikes sleep_spikes2 cell_info