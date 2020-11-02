clear

% ACC

load('hunt_acc.mat')

all_fixation_spiketimes = cell(1,length(fixation));

for unit = 1:length(fixation)
    
    fixation_spikes = [];
    
    for trial = 1:size(fixation{unit},1)
        
        for bin = 1:size(fixation{unit},2)
            
           if fixation{unit}(trial,bin) == 1
               
               fixation_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_fixation_spiketimes{unit} = fixation_spikes;
        
end

fixation = all_fixation_spiketimes;

all_task_spiketimes = cell(1,length(task));

for unit = 1:length(task)
    
    task_spikes = [];
    
    for trial = 1:size(task{unit},1)
        
        for bin = 1:size(task{unit},2)
            
           if task{unit}(trial,bin) == 1
               
               task_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_task_spiketimes{unit} = task_spikes;
        
end

all_task_spiketimes = task;

save('hunt_acc_spiketimes.mat','fixation','task','cell_info')

% DLPFC

load('hunt_dlpfc.mat')

all_fixation_spiketimes = cell(1,length(fixation));

for unit = 1:length(fixation)
    
    fixation_spikes = [];
    
    for trial = 1:size(fixation{unit},1)
        
        for bin = 1:size(fixation{unit},2)
            
           if fixation{unit}(trial,bin) == 1
               
               fixation_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_fixation_spiketimes{unit} = fixation_spikes;
        
end

fixation = all_fixation_spiketimes;

all_task_spiketimes = cell(1,length(task));

for unit = 1:length(task)
    
    task_spikes = [];
    
    for trial = 1:size(task{unit},1)
        
        for bin = 1:size(task{unit},2)
            
           if task{unit}(trial,bin) == 1
               
               task_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_task_spiketimes{unit} = task_spikes;
        
end

all_task_spiketimes = task;

save('hunt_dlpfc_spiketimes.mat','fixation','task','cell_info')

% OFC

load('hunt_ofc.mat')

all_fixation_spiketimes = cell(1,length(fixation));

for unit = 1:length(fixation)
    
    fixation_spikes = [];
    
    for trial = 1:size(fixation{unit},1)
        
        for bin = 1:size(fixation{unit},2)
            
           if fixation{unit}(trial,bin) == 1
               
               fixation_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_fixation_spiketimes{unit} = fixation_spikes;
        
end

fixation = all_fixation_spiketimes;

all_task_spiketimes = cell(1,length(task));

for unit = 1:length(task)
    
    task_spikes = [];
    
    for trial = 1:size(task{unit},1)
        
        for bin = 1:size(task{unit},2)
            
           if task{unit}(trial,bin) == 1
               
               task_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_task_spiketimes{unit} = task_spikes;
        
end

all_task_spiketimes = task;

save('hunt_ofc_spiketimes.mat','fixation','task','cell_info')

% unknown

load('hunt_unknown.mat')

all_fixation_spiketimes = cell(1,length(fixation));

for unit = 1:length(fixation)
    
    fixation_spikes = [];
    
    for trial = 1:size(fixation{unit},1)
        
        for bin = 1:size(fixation{unit},2)
            
           if fixation{unit}(trial,bin) == 1
               
               fixation_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_fixation_spiketimes{unit} = fixation_spikes;
        
end

fixation = all_fixation_spiketimes;

all_task_spiketimes = cell(1,length(task));

for unit = 1:length(task)
    
    task_spikes = [];
    
    for trial = 1:size(task{unit},1)
        
        for bin = 1:size(task{unit},2)
            
           if task{unit}(trial,bin) == 1
               
               task_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_task_spiketimes{unit} = task_spikes;
        
end

all_task_spiketimes = task;

save('hunt_unknown_spiketimes.mat','fixation','task','cell_info')

% VMPFC

load('hunt_vmpfc.mat')

all_fixation_spiketimes = cell(1,length(fixation));

for unit = 1:length(fixation)
    
    fixation_spikes = [];
    
    for trial = 1:size(fixation{unit},1)
        
        for bin = 1:size(fixation{unit},2)
            
           if fixation{unit}(trial,bin) == 1
               
               fixation_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_fixation_spiketimes{unit} = fixation_spikes;
        
end

fixation = all_fixation_spiketimes;

all_task_spiketimes = cell(1,length(task));

for unit = 1:length(task)
    
    task_spikes = [];
    
    for trial = 1:size(task{unit},1)
        
        for bin = 1:size(task{unit},2)
            
           if task{unit}(trial,bin) == 1
               
               task_spikes(end+1) = trial*bin;
               
           end
            
       end
        
    end
   
    all_task_spiketimes{unit} = task_spikes;
        
end

all_task_spiketimes = task;

save('hunt_vmpfc_spiketimes.mat','fixation','task','cell_info')