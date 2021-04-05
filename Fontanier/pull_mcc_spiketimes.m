clear all

filenames = getfn('/Users/zachz/Downloads/Fontanier', 'txt$');

neuron_info = readtable('/Users/zachz/Downloads/fontanier_neuron_info.csv');

mcc_spikes = {};
mcc_cell_info = {};

lpfc_spikes = {};
lpfc_cell_info = {};

for unit = 1:height(neuron_info)
    
    unit_num = neuron_info{unit,1};
    
    brain_area = neuron_info{unit,6};
    
    animal = neuron_info{unit,7};
    
    strings = ['/Users/zachz/Downloads/Fontanier/',num2str(unit_num),'.txt'];
    
    filename = join(strings);
    
    cell_spikes = load(filename);
    
    cell_spikes = cell_spikes / 100000;
    
    if strcmp(brain_area,'MCC') == 1
    
        mcc_cell_info{end+1} = struct('unit',unit_num,'brain_area',brain_area,'animal_id',animal);

        mcc_spikes{end+1} = cell_spikes;
        
    elseif strcmp(brain_area,'LPFC') == 1
        
        lpfc_cell_info{end+1} = struct('unit',unit_num,'brain_area',brain_area,'animal_id',animal);

        lpfc_spikes{end+1} = cell_spikes;
        
    end

end

cell_info = mcc_cell_info;
spikes = mcc_spikes;

spikes = spikes.';

save 'fontanier_mcc.mat' cell_info spikes

cell_info = lpfc_cell_info;
spikes = lpfc_spikes;

spikes = spikes.';

save 'fontanier_lpfc.mat' cell_info spikes

