clear

% Get session names

d = dir('D:\Human medial temporal lobe\Data\sorted');
dfolders = d([d(:).isdir]);
dfolders = dfolders(~ismember({dfolders(:).name},{'.','..'}));

all_data = cell(1,length(dfolders));
events_info = {};

for n_session = 1:length(dfolders)
    
    units_dir = strcat(dfolders(n_session).folder,'\',dfolders(n_session).name);
    
    events_dir = strcat('D:\Human medial temporal lobe\Data\events\',dfolders(n_session).name);
    
    session = dfolders(n_session).name;
    
    units = getfn(units_dir);
    
    spikes_per_session = cell(2,length(units));
    
    for unit = 1:length(units)
        
        this_file = units{unit};
        
        load(this_file)
        
        unit_spikes = spikes(:,3);
        unit_clusters = spikes(:,2);
        
        spikes_per_session{1,unit} = unit_spikes;
        spikes_per_session{2,unit} = unit_clusters;
        
    end
    
    session_spikes = vertcat(spikes_per_session{1,:});
    session_clusters = vertcat(spikes_per_session{2,:});
    
    unique_clusters = unique(session_clusters);
    num_clusters = length(unique_clusters);

    spikes_per_unit = cell(1,num_clusters);

% Separate spikes by cluster

    for cluster = 1:num_clusters
    
        cluster_spikes = [];
    
        for spike = 1:length(session_spikes)
        
            if session_clusters(spike) == unique_clusters(cluster)
            
                cluster_spikes(end+1) = session_spikes(spike);
        
            end
        
        end
    
        spikes_per_unit{cluster} = cluster_spikes;
    
    end
        
    load(strcat(events_dir,'\NO\','brainArea.mat'))
    load(strcat(events_dir,'\NO\','eventsRaw.mat'))
    
    % column3 is original cluster ID, column4 is brain area (key below):
    % 1=right hippocampus, 2=left hippocampus, 3=right amygdala, 4=left amygdala
    
    brain_area_cluster = brainArea(:,3);
    brain_area_id = brainArea(:,4);
    
    % get trial breaks for each session
    
    responses = [];
    
    for event = 1:length(events)
        
        if events(event,2) == 6

            responses(end+1) = events(event,1);

        events_info{n_session} = responses;

        end
    end
    
    brain_areas = [vertcat(brain_area_id{1,:}) vertcat(brain_area_cluster{2,:})];

    brain_areas = sortrows(brain_areas);

    brain_areas(brain_areas(:,1)==0,:) = [];
    
    for cluster = 1:num_clusters
    
        cluster_spikes = [];
    
        for spike = 1:length(all_spikes)
        
            if all_clusters(spike) == unique_clusters(cluster)
            
                cluster_spikes(end+1) = all_spikes(spike);
        
            end
        
        end
    
        spikes_per_unit{cluster} = cluster_spikes;
    
    end
    
end
    
    
    
    