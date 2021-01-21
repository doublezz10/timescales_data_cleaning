clear

filenames = getfn('/Users/zachz/Downloads/Buzsaki OFC data');

all_spikes = {};
animal_name = {};

for file = 1:length(filenames)
   
    this_file = filenames{file};
    
    load(this_file);
    
    units = spikes.times;
    
    for unit = 1:length(units)
        
        all_spikes{end+1} = units{unit};
    
        split_filename = split(filenames{file},"/");
    
        split_again = split(split_filename{end},".");
    
        animal_name{end+1} = split_again(1);
        
    end
    
end

spikes = all_spikes;

save all_buzsaki_spikes.mat 'spikes' 'animal_name'