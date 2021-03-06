% Defined rest/fixation period as time from trial initiation until odor
% comes on

% Defined task period as time from odor coming on until reward is off

% clear

% load('/Users/zachz/downloads/rat_ofc_1.mat')

% Create arrays the same length as 'timeseries' to assign an animal and
% recording session to each unit

unit_per_session_n1 = [12 7 2 1 3 1 7 10 7 6 8 10 14 17 17 13 9 6 5 3 5 13];
unit_per_session_p5 = [2 3 18 6 3 5 1];
unit_per_session_p9 = [15 7 9 7 6 3 1 7 4 6 7 2 1];
unit_per_session_t5 = [10 18 14 14 6 7 8 6 12 7 3 2];
unit_per_session_w1 = [8 12 14 7 21 13 8 11 9 9 3 10 1];

all_sessions = [unit_per_session_n1 unit_per_session_p5 unit_per_session_p9 unit_per_session_t5 unit_per_session_w1];

unit_sessions = ones(1,12);

for session=2:length(all_sessions)

    unit_session = session*ones(1,all_sessions(session));
    
    unit_sessions = [unit_sessions unit_session];
    
end

unit_animals = ones(1,176); unit_animals = [unit_animals [2*ones(1,38)]];
unit_animals = [unit_animals [3*ones(1,75)]]; unit_animals = [unit_animals [4*ones(1,107)]];
unit_animals = [unit_animals [5*ones(1,126)]];

clear unit_per_session_n1 unit_per_session_p5 unit_per_session_p9 unit_per_session_t5 unit_per_session_w1 session

% Build structures with info we care about

cell_info = cell(1,length(timeseries));
spikes = cell(1,length(timeseries));
trialstart = cell(1,length(timeseries));
odoron = cell(1,length(timeseries));
wateroff = cell(1,length(timeseries));

for unit=1:length(timeseries)
    
    dataset = 'Feierstein';
    species = 'rat';
    brain_area = 'OFC';
    animal = unit_animals(unit);
    session = unit_sessions(unit);
    unit_spikes = transpose(timeseries{unit})/1000;

    spikes{unit} = unit_spikes;
    trialstart{unit} = trial_start{session};
    odoron{unit} = odor_valve_on{session};
    wateroff{unit} = water_valve_off{session};
    
    cell_info{unit} = struct('Dataset',dataset,'Species',species,'BrainArea',brain_area,'Animal_num',animal,'Session_num',session);
        
end

save('ofc_1.mat','spikes','trialstart', 'odoron', 'wateroff', 'cell_info')