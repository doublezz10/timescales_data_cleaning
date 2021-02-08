clear all

filenames_sp = getfn('/Users/zachz/Downloads/Peyrache/mPFC_Data','SpikeData.dat$');
filenames_cell = getfn('/Users/zachz/Downloads/Peyrache/mPFC_Data','CellType.dat$');

spikes = {};
cell_info = {};

for file = 1:length(filenames_sp)
    
    sp_data = readtable(filenames_sp{file});
    cell_data = readtable(filenames_cell{file});
    
    for cell = 1:height(cell_data)
        
        cell_type = table2array(cell_data(cell,1));
        brain_region = 'mPFC';
        species = 'rat';
        dataset = 'LeMerre';
        
        if cell_type == 2
            cell_type = 'interneuron';
        elseif cell_type == 1
            cell_type = 'pyramidal';
        elseif cell_type == 0
            cell_type = 'unknown';
        end
        
        cell_info{end+1} = struct('dataset',dataset,'species',species,'brain_region',brain_region,'cell_type',cell_type);
        
        unit_spikes = (table2array(sp_data(sp_data.Var2 == cell,1)))/1000;
        
        spikes{end+1} = unit_spikes;
        
    end
    
end

save 'peyrache.mat' 'cell_info' 'spikes'