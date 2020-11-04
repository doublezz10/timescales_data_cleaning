%% Key for each field

% Field 1: Dataset: which dataset is this data from?
% Field 2: Species: mouse/rat/monkey/human
% Field 3: Brain Area: species-specific abbreviation for brain area
% Field 4: Unit Index: relative index of unit within area
% Field 5: Rest Spikes:  1d array of spike times from ITI/fixation
% Field 6: All Spikes: 1d array of spike times from whole session
% Field 7: Coordinates: a/p, d/v, l/r coords according to Allen Brain atlas

%% Load in data

clear

load('D:\timescales_data_cleaning\Steinmetz\mat files\itis_by_session.mat')

load('D:\timescales_data_cleaning\Steinmetz\mat files\aca_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\bla_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\ca1_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\ca2_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\ca3_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\dg_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\ila_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\orb_spikes.mat')
load('D:\timescales_data_cleaning\Steinmetz\mat files\pl_spikes.mat')

aca_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\aca_locations.csv');
bla_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\bla_locations.csv');
ca1_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\ca1_locations.csv');
ca2_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\ca2_locations.csv');
ca3_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\ca3_locations.csv');
dg_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\dg_locations.csv');
ila_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\ila_locations.csv');
orb_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\orb_locations.csv');
pl_coords = readtable('D:\timescales_data_cleaning\Steinmetz\csv files\pl_locations.csv');

%% For each region, make cell array of structures with all of the info

% ACA - anterior cingulate area

aca_units = cell(1,length(aca_spikes_all));

for i=1:length(aca_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'ACA';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [aca_coords{i,6} aca_coords{i,7} aca_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    aca_units{i} = unit_struct;
    
end

save('aca_unit_info.mat','aca_units')

% BLA - basolateral amygdala

bla_units = cell(1,length(bla_spikes_all));

for i=1:length(bla_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'BLA';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [bla_coords{i,6} bla_coords{i,7} bla_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    bla_units{i} = unit_struct;
    
end

save('bla_unit_info.mat','bla_units')

% ILA - infralimbic area

ila_units = cell(1,length(ila_spikes_all));

for i=1:length(ila_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'ILA';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [ila_coords{i,6} ila_coords{i,7} ila_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    ila_units{i} = unit_struct;
    
end

save('ila_unit_info.mat','ila_units')

% ORB - orbital cortex

orb_units = cell(1,length(orb_spikes_all));

for i=1:length(orb_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'ORB';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [orb_coords{i,6} orb_coords{i,7} orb_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    orb_units{i} = unit_struct;
    
end

save('orb_unit_info.mat','orb_units')

% PL - prelimbic cortex

pl_units = cell(1,length(pl_spikes_all));

for i=1:length(pl_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'PL';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [pl_coords{i,6} pl_coords{i,7} pl_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    pl_units{i} = unit_struct;
    
end

save('pl_unit_info.mat','pl_units')

% CA1 subfield of hippocampus

ca1_units = cell(1,length(ca1_spikes_all));

for i=1:length(ca1_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'CA1';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [ca1_coords{i,6} ca1_coords{i,7} ca1_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    ca1_units{i} = unit_struct;
    
end

save('ca1_unit_info.mat','ca1_units')

% CA2 subfield of hippocampus

ca2_units = cell(1,length(ca2_spikes_all));

for i=1:length(ca2_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'CA2';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [ca2_coords{i,6} ca2_coords{i,7} ca2_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    ca2_units{i} = unit_struct;
    
end

save('ca2_unit_info.mat','ca2_units')

% CA3 subfield of hippocampus

ca3_units = cell(1,length(ca3_spikes_all));

for i=1:length(ca3_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'CA3';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [ca3_coords{i,6} ca3_coords{i,7} ca3_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    ca3_units{i} = unit_struct;
    
end

save('ca3_unit_info.mat','ca3_units')

% DG - dentate gyrus of hippocampus

dg_units = cell(1,length(dg_spikes_all));

for i=1:length(dg_spikes_all)
    
    field1 = 'Dataset'; value1 = 'Steinmetz';
    field2 = 'Species'; value2 = 'mouse';
    field3 = 'Brain_Area'; value3 = 'DG';
    field4 = 'Unit_Index'; value4 = i;
    field7 = 'Coordinates'; value7 = [dg_coords{i,6} dg_coords{i,7} dg_coords{i,8}];
    
    unit_struct = struct(field1,value1,field2,value2,field3,value3,field4,value4,field7,value7);
    
    dg_units{i} = unit_struct;
    
end

save('dg_unit_info.mat','dg_units')