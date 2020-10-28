clear

% load('D:\Data from Meg\units_for_Zach.mat')
load('/Users/zachz/Downloads/units_for_Zach.mat')


cell_info_scACC = {};
cell_info_amygdala = {};
cell_info_ventralStriatum = {};

task_scACC = {};
task_amygdala = {};
task_ventralStriatum = {};

rest_scACC = {};
rest_amygdala = {};
rest_ventralStriatum = {};

for unit=1:length(units)
   
    dataset = 'Meg';
    species = 'Macaque';
    
    unit_name = units(unit).unitname;
    brain_area = units(unit).brainarea;
    
    ml_coord = units(unit).ML;
    ap_coord = units(unit).AP;
    total_depth = units(unit).total_depth;
    
    fixation_spikes = [];
    trial_spikes = [];
    
    if strcmp(brain_area,'SC') == 1
        brain_area = 'scACC';
        cell_info_scACC{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
        
        for trial = 1:length(units(unit).fixOn)
        
            fixation_start = units(unit).fixOn(trial);
            fixation_end = units(unit).stimOn(trial);
            task_start = units(unit).stimOn(trial);
            task_end = units(unit).rewardTime(trial);
            spikes = units(unit).spikes;
            
            for spike = 1:length(spikes)
                if spikes(spike) >= fixation_start && spikes(spike) <= fixation_end
                    fixation_spikes(end+1) = spikes(spike);
                
                elseif spikes(spike) >= task_start && spikes(spike) <= task_end
                    trial_spikes(end+1) = spikes(spike);
                    
                end
                
            end
            
            
        end
        
    rest_scACC{end+1} = fixation_spikes;
    task_scACC{end+1} = trial_spikes;
        
    elseif strcmp(brain_area,'AMY') == 1
        brain_area = 'amygdala';
        cell_info_amygdala{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
        
        fixation_spikes = [];
        trial_spikes = [];
        
        for trial = 1:length(units(unit).fixOn)
        
            fixation_start = units(unit).fixOn(trial);
            fixation_end = units(unit).stimOn(trial);
            task_start = units(unit).stimOn(trial);
            task_end = units(unit).rewardTime(trial);
            spikes = units(unit).spikes;
            
            for spike = 1:length(spikes)
                if spikes(spike) >= fixation_start && spikes(spike) <= fixation_end
                    fixation_spikes(end+1) = spikes(spike);

                elseif spikes(spike) >= task_start && spikes(spike) <= task_end
                    trial_spikes(end+1) = spikes(spike);
                end
                
            end
            
        end
        
    rest_amygdala{end+1} = fixation_spikes;
    task_amygdala{end+1} = trial_spikes;
    
    elseif strcmp(brain_area,'VS') == 1
        brain_area = 'ventralStriatum';
        cell_info_ventralStriatum{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth);
        
        fixation_spikes = [];
        trial_spikes = [];
        
        for trial = 1:length(units(unit).fixOn)
        
            fixation_start = units(unit).fixOn(trial);
            fixation_end = units(unit).stimOn(trial);
            task_start = units(unit).stimOn(trial);
            task_end = units(unit).rewardTime(trial);
            spikes = units(unit).spikes;
            
            for spike = 1:length(spikes)
                if spikes(spike) >= fixation_start && spikes(spike) <= fixation_end
                    fixation_spikes(end+1) = spikes(spike);

                elseif spikes(spike) >= task_start && spikes(spike) <= task_end
                    trial_spikes(end+1) = spikes(spike);
                end
                
            end
            
        end
        
    rest_ventralStriatum{end+1} = fixation_spikes;
    task_ventralStriatum{end+1} = trial_spikes;
    
    end
    
end


task = task_scACC; fixation = rest_scACC; cell_info = cell_info_scACC;
save('meg_scACC.mat', 'task', 'fixation', 'cell_info')

task = task_amygdala; fixation = rest_amygdala; cell_info = cell_info_amygdala;
save('meg_amygdala.mat', 'task', 'fixation', 'cell_info')

task = task_ventralStriatum; fixation = rest_ventralStriatum; cell_info = cell_info_ventralStriatum;
save('meg_ventralStriatum.mat', 'task', 'fixation', 'cell_info')