clear

% Get filenames

filenames = getfn('D:\Human medial temporal lobe\Data\sorted');

data_per_file = cell(2,length(filenames));

% Second column is original ClusterID, third is timestamp in us
% Each row is a spike

% Loop through each file, and pull out original ClusterID and spiketimes
for file=1:length(filenames)
    
    this_file = filenames{file};
    
    load(this_file);
    
    data_per_file{1,file} = spikes(:,3);
    data_per_file{2,file} = spikes(:,2);
    
end

% Stack all of the spikes and all of the clusters

all_clusters = vertcat(data_per_file{2,:});
all_spikes = vertcat(data_per_file{1,:});

unique_clusters = unique(all_clusters);
num_clusters = length(unique_clusters);

spikes_per_unit = cell(1,num_clusters);

% Separate spikes by cluster

for cluster = 1:num_clusters
    
    cluster_spikes = [];
    
    for spike = 1:length(all_spikes)
        
        if all_clusters(spike) == unique_clusters(cluster)
            
            cluster_spikes(end+1) = all_spikes(spike);
        
        end
        
    end
    
    spikes_per_unit{cluster} = cluster_spikes;
    
end

%% Get brain areas
% column3 is original cluster ID, column4 is brain area (key below):
% 1=right hippocampus, 2=left hippocampus, 3=right amygdala, 4=left amygdala

filenames = getfn('D:\Human medial temporal lobe\Data\events','brainArea.mat$');

brain_area_info = {};

for file = 1:length(filenames)
    
    load(filenames{file})
    
    if exist('brainArea','var')
        
        brain_area_info{1,end+1} = brainArea(:,3);
        brain_area_info{2,end+1} = brainArea(:,4);
        
    end
    
end

brain_areas = [vertcat(brain_area_info{1,:}) vertcat(brain_area_info{2,:})];

brain_areas = sortrows(brain_areas);

brain_areas(brain_areas(:,1)==0,:) = [];

all_brain_areas = zeros(1,1203);
n_rows = size(brain_areas,1);

for cluster  = 1:num_clusters
    
    for row = 1:n_rows
        
        if brain_areas(row,1) == unique_clusters(cluster)
            
            all_brain_areas(1,cluster) = brain_areas(row,2);
            
        end
        
    end
    
end

%% Build structure

cell_info_hc = {};
cell_info_amygdala = {};

spikes_hc = {};
spikes_amygdala = {};

for unit = 1:num_clusters
    
    if all_brain_areas(unit) == 1
    
        cell_info_hc{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','hippocampus','Cluster',unique_clusters(cluster));
        spikes_hc{end+1} = spikes_per_unit{unit};
        
    elseif all_brain_areas(unit) == 2
        
        cell_info_hc{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','hippocampus','Cluster',unique_clusters(cluster));
        spikes_hc{end+1} = spikes_per_unit{unit};
        
    elseif all_brain_areas(unit) == 3
        
        cell_info_amygdala{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','amygdala','Cluster',unique_clusters(cluster));
        spikes_amygdala{end+1} = spikes_per_unit{unit};
        
    elseif all_brain_areas(unit) == 4
        
        cell_info_amygdala{end+1} = struct('Dataset','Faraut','Species','human','BrainArea','amygdala','Cluster',unique_clusters(cluster));
        spikes_amygdala{end+1} = spikes_per_unit{unit};
        
    end
    
end

%% Save!

spikes = spikes_hc;
cell_info = cell_info_hc;

save('faraut_hippocampus.mat','spikes','cell_info')

spikes = spikes_amygdala;
cell_info = cell_info_amygdala;

save('faraut_amygdala.mat','spikes','cell_info')