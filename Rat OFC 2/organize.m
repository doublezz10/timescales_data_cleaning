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
spikes = cell(1,length(timeseries));

for unit=1:length(timeseries)
    
    dataset = 'Kepecs';
    species = 'rat';
    brain_area = 'OFC';
    animal = unit_animals(unit);
    session = unit_sessions(unit);
    unit_spikes = transpose(timeseries{unit})/1000;

    
    rest_spikes = [];
    task_spikes = [];
    
    spikes{unit} = unit_spikes; 
    cell_info{unit} = struct('Dataset',dataset,'Species',species,'BrainArea',brain_area,'Animal_num',animal,'Session_num',session);
        
end

save('ofc_2.mat','spikes','cell_info')