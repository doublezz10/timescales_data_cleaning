%% Build a structure for each unit

% Unit number in Steinmetz is the cluster number, and brain_area is
% determined based on the peak channel for that cluster.

field1 = 'dataset'; value1 = 'Steinmetz';
field2 = 'species'; value2 = 'mouse';
field3 = 'brain_area'; value3 = 'ACA';
field4 = 'unit_number'; value4 = 'x';
field5 = 'ITI_fixation_spikes'; value5 = 'trials*spike_times';
field6 = 'all_spikes'; value6 = 'trials*spike_times';

unit_x = struct(field1,value1,field2,value2,field3,value3,field4,value4,field5,value5,field6,value6);

%% Place each unit's structure into one big array for the whole dataset


big_struct = [unit_x unit_y unit_z];