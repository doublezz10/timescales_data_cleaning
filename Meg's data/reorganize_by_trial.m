clear

load('D:\Data from Meg\units_for_Zach.mat')
% load('/Users/zachz/Downloads/units_for_Zach.mat')


cell_info_scACC = {};
cell_info_amygdala = {};
cell_info_ventralStriatum = {};

task_scACC = {};
task_amygdala = {};
task_ventralStriatum = {};

rest_scACC = {};
rest_amygdala = {};
rest_ventralStriatum = {};

by_trial_scACC = {};
by_trial_amygdala = {};
by_trial_ventralStriatum = {};

for unit=1:length(units)
   
    dataset = 'Meg';
    species = 'Macaque';
    
    unit_name = units(unit).unitname;
    brain_area = units(unit).brainarea;
    
    ml_coord = units(unit).ML;
    ap_coord = units(unit).AP;
    total_depth = units(unit).total_depth;
    
    fixation_times = units(unit).fixOn;
    stim_times = units(unit).stimOn;
    
    fixation_spikes = [];
    trial_spikes = [];
    fix_spikes_by_trial = {};
    
    if strcmp(brain_area,'SC') == 1
        brain_area = 'scACC';
        cell_info_scACC{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth,'fix_on',fixation_times,'stim_on',stim_times);
        
        for trial = 1:length(units(unit).fixOn)
        
            fixation_start = units(unit).fixOn(trial);
            fixation_end = units(unit).stimOn(trial);
            task_start = units(unit).stimOn(trial);
            task_end = units(unit).rewardTime(trial);
            spikes = units(unit).spikes;
            
            trial_fix_spikes = [];
            
            for spike = 1:length(spikes)
                if spikes(spike) >= fixation_start && spikes(spike) <= fixation_end
                    fixation_spikes(end+1) = spikes(spike);
                    
                    trial_fix_spikes(end+1) = spikes(spike) - fixation_start;
                
                elseif spikes(spike) >= task_start && spikes(spike) <= task_end
                    trial_spikes(end+1) = spikes(spike);
                    
                end
                
            end
            
            fix_spikes_by_trial{end+1} = trial_fix_spikes;
            
            
        end
        
    rest_scACC{end+1} = fixation_spikes;
    task_scACC{end+1} = trial_spikes;
    by_trial_scACC{end+1} = fix_spikes_by_trial;
        
    elseif strcmp(brain_area,'AMY') == 1
        brain_area = 'amygdala';
        cell_info_amygdala{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth,'fix_on',fixation_times,'stim_on',stim_times);
        
        fixation_spikes = [];
        trial_spikes = [];
        fix_spikes_by_trial = {};
        
        for trial = 1:length(units(unit).fixOn)
        
            fixation_start = units(unit).fixOn(trial);
            fixation_end = units(unit).stimOn(trial);
            task_start = units(unit).stimOn(trial);
            task_end = units(unit).rewardTime(trial);
            spikes = units(unit).spikes;
            
            trial_fix_spikes = [];
            
            for spike = 1:length(spikes)
                if spikes(spike) >= fixation_start && spikes(spike) <= fixation_end
                    fixation_spikes(end+1) = spikes(spike);
                    
                    trial_fix_spikes(end+1) = spikes(spike) - fixation_start;

                elseif spikes(spike) >= task_start && spikes(spike) <= task_end
                    trial_spikes(end+1) = spikes(spike);
                end
                
            end
            
            fix_spikes_by_trial{end+1} = trial_fix_spikes;
            
        end
        
    rest_amygdala{end+1} = fixation_spikes;
    task_amygdala{end+1} = trial_spikes;
    by_trial_amygdala{end+1} = fix_spikes_by_trial;
    
    elseif strcmp(brain_area,'VS') == 1
        brain_area = 'ventralStriatum';
        cell_info_ventralStriatum{end+1} = struct('Dataset',dataset,'Species',species,'Unit_name',unit_name,'Brain_area',brain_area,'AP',ap_coord,'ML',ml_coord,'total_depth',total_depth,'fix_on',fixation_times,'stim_on',stim_times);
        
        fixation_spikes = [];
        trial_spikes = [];
        fix_spikes_by_trial = {};
        
        for trial = 1:length(units(unit).fixOn)
        
            fixation_start = units(unit).fixOn(trial);
            fixation_end = units(unit).stimOn(trial);
            task_start = units(unit).stimOn(trial);
            task_end = units(unit).rewardTime(trial);
            spikes = units(unit).spikes;
            
            trial_fix_spikes = [];
            
            for spike = 1:length(spikes)
                if spikes(spike) >= fixation_start && spikes(spike) <= fixation_end
                    fixation_spikes(end+1) = spikes(spike);
                    
                    trial_fix_spikes(end+1) = spikes(spike) - fixation_start;

                elseif spikes(spike) >= task_start && spikes(spike) <= task_end
                    trial_spikes(end+1) = spikes(spike);
                end
                
            end
            
            fix_spikes_by_trial{end+1} = trial_fix_spikes;
            
        end
        
    rest_ventralStriatum{end+1} = fixation_spikes;
    task_ventralStriatum{end+1} = trial_spikes;
    by_trial_ventralStriatum{end+1} = fix_spikes_by_trial;
    
    end
    
end


spikes = by_trial_scACC; cell_info = cell_info_scACC;
save('meg_scACC.mat', 'spikes', 'cell_info')

spikes = by_trial_amygdala; cell_info = cell_info_amygdala;
save('meg_amygdala.mat', 'spikes', 'cell_info')

spikes = by_trial_ventralStriatum; cell_info = cell_info_ventralStriatum;
save('meg_ventralStriatum.mat', 'spikes', 'cell_info')