cell_info_scACC = {};
cell_info_amygdala = {};
cell_info_ventralStriatum = {};

spikes_scACC = {};
spikes_amygdala = {};
spikes_ventralStriatum = {};

for unit=1:length(units)
   
    dataset = 'Meg';
    species = 'Macaque';
    
    unit_name = units(unit).unitname;
    brain_area = units(unit).brainarea;
    
    ml_coord = units(unit).ML;
    ap_coord = units(unit).AP;
    total_depth = units(unit).total_depth;
    
    if strcmp(brain_area,'SC') == 1
        brain_area = 'scACC';
        cell_info_scACC{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
        
        all_spikes = units(unit).spikes/1000;
        
    spikes_scACC{end+1} = all_spikes;
        
    elseif strcmp(brain_area,'AMY') == 1
        brain_area = 'amygdala';
        cell_info_amygdala{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
        
        all_spikes = units(unit).spikes/1000;
        
    spikes_amygdala{end+1} = all_spikes;
    
    elseif strcmp(brain_area,'VS') == 1
        brain_area = 'ventralStriatum';
        cell_info_ventralStriatum{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
       
        all_spikes = units(unit).spikes/1000;
        
    spikes_ventralStriatum{end+1} = all_spikes;

    end
    
end


spikes = spikes_scACC; cell_info = cell_info_scACC;
save('meg_scACC.mat', 'spikes', 'cell_info')

spikes = spikes_amygdala; cell_info = cell_info_amygdala;
save('meg_amygdala.mat', 'spikes', 'cell_info')

spikes = spikes_ventralStriatum; cell_info = cell_info_ventralStriatum;
save('meg_ventralStriatum.mat', 'spikes', 'cell_info')