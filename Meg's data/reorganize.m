load('D:\Data from Meg\units_for_Zach.mat')

cell_info_scACC = {};
cell_info_amygdala = {};
cell_info_ventralStriatum = {};

task_scACC = {};
task_amygdala = {};
task_ventralStriatum = {};

rest_scACC = {};
rest_amygdala = {};
rest_ventralStriatum = {};

for unit=1:len(units)
   
    dataset = 'Meg';
    species = 'Macaque';
    
    unit_name = units.unit.unitname;
    brain_area = units.unit.brainarea;
    
    ml_coord = units.unit.ML;
    ap_coord = units.unit.AP;
    depth = units.unit.total_depth;
    
    if strcmp(brain_area,'SC') == 1
        brain_area = 'scACC';
        cell_info_scACC{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
        
        fiaxtion_spikes = 
        task_spikes = 
    
    end
    
    if strcmp(brain_area,'AMY') == 1
        brain_area = 'amygdala';
        cell_info_amygdala{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
    end
    
    if strcmp(brain_area,'SC') == 1
        brain_area = 'ventral striatum';
        cell_info_ventralStriatum{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
    end
end