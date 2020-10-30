% Defined rest/fixation period as time from trial initiation until odor
% comes on

% Defined task period as time from odor coming on until reward is off

clear

load('/Users/zachz/downloads/rat_ofc_2.mat')

% Create arrays the same length as 'timeseries' to assign an animal and
% recording session to each unit

unit_per_session_n1 = [14 11 8 6 7 5 9 12 12 11 11 15 15 21 19 17 11 7 6 3 5 17];
unit_per_session_n48 = [8 15 14 15 14 13 11 11 18 8 13 10 16 9 6 4 3];
unit_per_session_n49 = [5 10 12 11 8 13 18 10 11 10 6 9 8];

all_sessions = [unit_per_session_n1 unit_per_session_n48 unit_per_session_n49];

unit_sessions = ones(1,14);

for session=2:length(all_sessions)

    unit_session = session*ones(1,all_sessions(session));
    
    unit_sessions = [unit_sessions unit_session];
    
end

unit_animals = ones(1,242); unit_animals = [unit_animals [2*ones(1,188)]];
unit_animals = [unit_animals [3*ones(1,131)]];

clear unit_per_session_n1 unit_per_session_n48 unit_per_session_n49 session

% Build structures with info we care about

cell_info = cell(1,length(timeseries));
task = cell(1,length(timeseries));
rest = cell(1,length(timeseries));

for unit=1:length(timeseries)
    
    dataset = 'Kepecs';
    species = 'rat';
    brain_area = 'OFC';
    animal = unit_animals(unit);
    session = unit_sessions(unit);
    unit_spikes = transpose(timeseries{unit})/1000;

    
    rest_spikes = [];
    task_spikes = [];
    
    for trial=1:length(trial_start{session})
    
        trialstart = trial_start{session}(trial);
        odor_on = odor_valve_on{session}(trial);
        water_off = water_valve_off{session}(trial);
        
       for spike=1:length(unit_spikes)

           if unit_spikes(spike) >= trialstart && unit_spikes(spike) <= trialstart + odor_on
               
               rest_spikes(end+1) = unit_spikes(spike);
           
           elseif unit_spikes(spike) >= trialstart + odor_on && unit_spikes(spike) <= trialstart + water_off
               
               task_spikes(end+1) = unit_spikes(spike);
          
            end
        end
    end
    
    rest{unit} = rest_spikes; 
    task{unit} = task_spikes;
    cell_info{unit} = struct('Dataset',dataset,'Species',species,'BrainArea',brain_area,'Animal_num',animal,'Session_num',session);
        
end

save('ofc_2.mat','task','rest','cell_info')