clear

load('hunt_monkey_ofc.mat')
load('region_indices.mat')

acc_units = ACC_units; clear ACC_units
dlpfc_units = DLPFC_units; clear DLPFC_units
ofc_units = OFC_units; clear OFC_units
vmpfc_units = VMPFC_units; clear VMPFC_units

% ACC

all_fixation_acc = {1,length(acc_units)};
all_response_acc = {1,length(acc_units)};
cell_info_acc = {1,length(acc_units)};

for unit = 1:length(acc_units)
    
    all_fixation_acc{unit} = fixation_matrices{acc_units(unit)};
    all_response_acc{unit} = response_matrices{acc_units(unit)};
    cell_info_acc{unit} = struct('Dataset','Hunt','Species','Macaque','Unit_Index',unit,'Brain_area','ACC');
    
end

fixation = all_fixation_acc; task = all_response_acc; cell_info = cell_info_acc;

save('hunt_acc.mat','fixation','task','cell_info')

% DLPFC

all_fixation_dlpfc = {1,length(dlpfc_units)};
all_response_dlpfc = {1,length(dlpfc_units)};
cell_info_dlpfc = {1,length(dlpfc_units)};

for unit = 1:length(dlpfc_units)
    
    all_fixation_dlpfc{unit} = fixation_matrices{dlpfc_units(unit)};
    all_response_dlpfc{unit} = response_matrices{dlpfc_units(unit)};
    cell_info_dlpfc{unit} = struct('Dataset','Hunt','Species','Macaque','Unit_Index',unit,'Brain_area','DLPFC');
    
end

fixation = all_fixation_dlpfc; task = all_response_dlpfc; cell_info = cell_info_dlpfc;

save('hunt_dlpfc.mat','fixation','task','cell_info')

% OFC

all_fixation_ofc = {1,length(ofc_units)};
all_response_ofc = {1,length(ofc_units)};
cell_info_ofc = {1,length(ofc_units)};

for unit = 1:length(ofc_units)
    
    all_fixation_ofc{unit} = fixation_matrices{ofc_units(unit)};
    all_response_ofc{unit} = response_matrices{ofc_units(unit)};
    cell_info_ofc{unit} = struct('Dataset','Hunt','Species','Macaque','Unit_Index',unit,'Brain_area','OFC');
    
end

fixation = all_fixation_ofc; task = all_response_ofc; cell_info = cell_info_ofc;

save('hunt_ofc.mat','fixation','task','cell_info')

% unknown

all_fixation_unknown = {1,length(unknown_units)};
all_response_unknown = {1,length(unknown_units)};
cell_info_unknown = {1,length(unknown_units)};

for unit = 1:length(unknown_units)
    
    all_fixation_unknown{unit} = fixation_matrices{unknown_units(unit)};
    all_response_unknown{unit} = response_matrices{unknown_units(unit)};
    cell_info_unknown{unit} = struct('Dataset','Hunt','Species','Macaque','Unit_Index',unit,'Brain_area','unknown');
    
end

fixation = all_fixation_unknown; task = all_response_unknown; cell_info = cell_info_unknown;

save('hunt_unknown.mat','fixation','task','cell_info')

% VMPFC

all_fixation_vmpfc = {1,length(vmpfc_units)};
all_response_vmpfc = {1,length(vmpfc_units)};
cell_info_vmpfc = {1,length(vmpfc_units)};

for unit = 1:length(vmpfc_units)
    
    all_fixation_vmpfc{unit} = fixation_matrices{vmpfc_units(unit)};
    all_response_vmpfc{unit} = response_matrices{vmpfc_units(unit)};
    cell_info_vmpfc{unit} = struct('Dataset','Hunt','Species','Macaque','Unit_Index',unit,'Brain_area','VMPFC');
    
end

fixation = all_fixation_vmpfc; task = all_response_vmpfc; cell_info = cell_info_vmpfc;

save('hunt_vmpfc.mat','fixation','task','cell_info')