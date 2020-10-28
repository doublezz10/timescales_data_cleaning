% Filenames is a 1 x n_units cell array with each unit's timeseries
% Other variables are 1 x n_sessions and each contain 1 x n_trials for
% each session

clear

filenames = getfn('D:\CRCNS OFC 1 - Rats\data');

timeseries = {};
num_trials = [];
trial_start = {};
odor_valve_on = {};
water_valve_off = {};

for file = 1:length(filenames)
   
    this_file = filenames{file};
    
    load(this_file);
    
    if exist('TS','var')
        
        timeseries{end+1} = TS;
        
    elseif exist('TrialStart','var')
        
        num_trials(end+1) = length(TrialStart);
        trial_start{end+1} = TrialStart;
        odor_valve_on{end+1} = OdorValveOn;
        water_valve_off{end+1} = WaterValveOff;
        
    end 
    
    clearvars -except filenames timeseries num_trials trial_start odor_valve_on water_valve_off
    
end

save('rat_ofc_1.mat','num_trials','odor_valve_on','timeseries','trial_start','water_valve_off')