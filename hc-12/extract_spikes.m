clear

filenames = getfn('/Users/zachz/Downloads/CRCNS_scripts/hc-12/data');

d = dir('/Users/zachz/Downloads/CRCNS_scripts/hc-12/data');
d(1:2) = [];

spikes = cell(1,length(filenames));

spikes_by_trial = cell(1,length(filenames));

cell_info = cell(1,length(filenames));

for file_n = 1:length(filenames)
    
    this_file = filenames{file_n};
    
    load(this_file)
    
    if isfield(file,'elec') == 1
    
        all_spikes = file.elec;

        % spiketimes are already in seconds :)

        spikes{1,file_n} = all_spikes;
    
        fix_start = [];
        fix_end = [];

        % pull trial_start and joystick move times ("fixation" period)
        
        if isfield(file,'newallo') == 1

            for trial = 1:height(file.newallo.codematrix)

                for code = 1:length(file.newallo.codematrix(trial,:))

                    if file.newallo.codematrix(trial,code) == 21

                        fix_start(trial) = file.newallo.timematrix(trial,code);

                    elseif file.newallo.codematrix(trial,code) == 3

                        fix_end(trial) = file.newallo.timematrix(trial,code);

                    end

                end

            end

            spikes_by_trials = {};

            for trial = 1:length(fix_start)

                trial_spikes = [];

                for spike = 1:length(file.elec)

                    if file.elec(spike) > fix_start(trial) && file.elec(spike) < fix_end(trial)

                        trial_spikes(end+1) = file.elec(spike);

                    end

                end

                spikes_by_trials{end+1} = trial_spikes;

            end

            spikes_by_trial{1,file_n} = spikes_by_trials;

            % get monkey id from filename

            if contains(d(file_n).name,'ke') == 1

                monkey_num = 1;

            elseif contains(d(file_n).name,'sn') == 1

                monkey_num = 2;

            end

            cell_info{1,file_n} = struct('dataset','Wirth','species','monkey','individual',monkey_num,'brain_area','hippocampus','coords',file.reclocation);

        end    
        
    end
        
end

save 'wirth.mat' spikes cell_info
save 'wirth_by_trial.mat' spikes_by_trial cell_info