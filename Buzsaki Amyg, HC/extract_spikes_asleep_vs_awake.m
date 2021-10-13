clear all

bla_spikes = {};
bla_spikes2 = {};
bla_sleep_spikes = {};
bla_sleep_spikes2 = {};
bla_cell_info = {};

central_spikes = {};
central_spikes2 = {};
central_sleep_spikes = {};
central_sleep_spikes2 = {};
central_cell_info = {};

hippocampus_spikes = {};
hippocampus_spikes2 = {};
hippocampus_sleep_spikes = {};
hippocampus_sleep_spikes2 = {};
hippocampus_cell_info = {};

xmls = getfn('E:\hc-14\Rat08','xml$');

xmls = xmls(cellfun('isempty',strfind(xmls,'p')));
xmls = xmls(cellfun('isempty',strfind(xmls,'run')));
xmls = xmls(cellfun('isempty',strfind(xmls,'smell')));

bla_locations = readmatrix('E:\hc-14\Rat08\Rat08-Info\bla_locations.csv');
central_locations = readmatrix('E:\hc-14\Rat08\Rat08-Info\central_nucleus_locations.csv');

for session = 1:length(xmls)

    SetCurrentSession(xmls{session})
    
    run_start = {};
    run_end = {};
    sleep_start = {};
    sleep_end = {};
    
    names = GetEvents('output','descriptions');
    times = GetEvents;

    for name = 1:length(names)

        if contains(names{name},'beginning') == 1 && contains(names{name},'run') == 1

            run_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'run') == 1

            run_end{end+1} = times(name);

        elseif contains(names{name},'beginning') == 1 && contains(names{name},'sleep') == 1

            sleep_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'sleep') == 1

            sleep_end{end+1} = times(name);

        end

    end

    % Get All Spikes
    spikes1=GetSpikeTimes('output','numbered');
    spikes2=GetSpikeTimes('output','full');
    spikes=[spikes2 spikes1(:,2)];
    spikes(spikes(:,3)==0,:)=[];
    spikes(spikes(:,3)==1,:)=[];

    % Remnumber IDs after removing MUA and artifacts
    ids=unique(spikes(:,4));
    for ii=1:length(ids)
      spikes(spikes(:,4)==ids(ii),4)=ii;
    end
    idx=unique(spikes(:,2:4),'rows'); % shank / cell/ ID

    if min(idx(:,3))==1 && sum(diff(idx(:,3))-1)==0
      disp('Renumbering OK')
    else
      error('Problem with index : aborting')
    end
    
    restrict_bla = bla_locations(:,1) == session;
    
    bla_list = bla_locations(restrict_bla,:);
    
    restrict_central = central_locations(:,1) == session;
    
    central_list = central_locations(restrict_central,:);

    for cell_id = 1:length(idx)

        rule = spikes(:,4) == idx(cell_id,3);

        cell_spikes = spikes(rule);
        
        % run_1 spikes, run_2, sleep_1, sleep_2 using
        % (run_start,run_end,etc.)

        cell_spikes_only = cell_spikes(:,1);
                
        run_1_spikes = cell_spikes_only(cell_spikes_only > run_start{1} & cell_spikes_only < run_end{1});
        
        if length(run_start) > 1
            
            run_2_spikes = cell_spikes_only(cell_spikes_only > run_start{2} & cell_spikes_only < run_end{2});
            
        else
            
            run_2_spikes = [];
            
        end
        
        sleep_1_spikes = cell_spikes_only(cell_spikes_only > sleep_start{1} & cell_spikes_only < sleep_end{1});
        
        if length(sleep_start) > 1
            
            sleep_2_spikes = cell_spikes_only(cell_spikes_only > sleep_start{2} & cell_spikes_only < sleep_end{2});
            
        else
            
            sleep_2_spikes = [];
            
        end

        shank_n = idx(cell_id,1);

        if 1 <= shank_n && shank_n <= 4

            hippocampus_spikes{end+1} = run_1_spikes;
            hippocampus_spikes2{end+1} = run_2_spikes;
            
            hippocampus_sleep_spikes{end+1} = sleep_1_spikes;
            hippocampus_sleep_spikes2{end+1} = sleep_2_spikes;
            
            hippocampus_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','hippocampus','session',session,'rat',8,'cell_id',cell_id);
            
        elseif ismember(shank_n,bla_list) == 1
            
            bla_spikes{end+1} = run_1_spikes;
            bla_spikes2{end+1} = run_2_spikes;
            
            bla_sleep_spikes{end+1} = sleep_1_spikes;
            bla_sleep_spikes2{end+1} = sleep_2_spikes;
            
            bla_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','bla','session',session,'rat',8,'cell_id',cell_id);
            
        elseif ismember(shank_n,central_list) == 1
            
            central_spikes{end+1} = run_1_spikes;
            central_spikes2{end+1} = run_2_spikes;
            
            central_sleep_spikes{end+1} = sleep_1_spikes;
            central_sleep_spikes2{end+1} = sleep_2_spikes;
            
            central_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','central','session',session,'rat',8,'cell_id',cell_id);
            
        end

    end

end

xmls = getfn('E:\hc-14\Rat09','xml$');

xmls = xmls(cellfun('isempty',strfind(xmls,'p')));
xmls = xmls(cellfun('isempty',strfind(xmls,'run')));
xmls = xmls(cellfun('isempty',strfind(xmls,'smell')));

bla_locations = load('E:\hc-14\Rat09\Rat09-Info\Structures\BLA.mat').BLA;
central_locations = load('E:\hc-14\Rat09\Rat09-Info\Structures\CeCM.mat').CeCM;

for session = 1:length(xmls)

    SetCurrentSession(xmls{session})
    
    run_start = {};
    run_end = {};
    sleep_start = {};
    sleep_end = {};
    
    names = GetEvents('output','descriptions');
    times = GetEvents;

    for name = 1:length(names)

        if contains(names{name},'beginning') == 1 && contains(names{name},'run') == 1

            run_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'run') == 1

            run_end{end+1} = times(name);

        elseif contains(names{name},'beginning') == 1 && contains(names{name},'sleep') == 1

            sleep_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'sleep') == 1

            sleep_end{end+1} = times(name);

        end

    end
    
    % Get All Spikes
    spikes1=GetSpikeTimes('output','numbered');
    spikes2=GetSpikeTimes('output','full');
    spikes=[spikes2 spikes1(:,2)];
    spikes(spikes(:,3)==0,:)=[];
    spikes(spikes(:,3)==1,:)=[];

    % Remnumber IDs after removing MUA and artifacts
    ids=unique(spikes(:,4));
    for ii=1:length(ids)
      spikes(spikes(:,4)==ids(ii),4)=ii;
    end
    idx=unique(spikes(:,2:4),'rows'); % shank / cell/ ID

    if min(idx(:,3))==1 && sum(diff(idx(:,3))-1)==0
      disp('Renumbering OK')
    else
      error('Problem with index : aborting')
    end
    
    restrict_bla = bla_locations(:,1) == session;
    
    bla_list = bla_locations(restrict_bla,:);
    
    restrict_central = central_locations(:,1) == session;
    
    central_list = central_locations(restrict_central,:);

    for cell_id = 1:length(idx)

        rule = spikes(:,4) == idx(cell_id,3);

        cell_spikes = spikes(rule);

        cell_spikes_only = cell_spikes(:,1);
        if length(run_start) > 0
            
            run_1_spikes = cell_spikes_only(cell_spikes_only > run_start{1} & cell_spikes_only < run_end{1});

            if length(run_start) > 1

                run_2_spikes = cell_spikes_only(cell_spikes_only > run_start{2} & cell_spikes_only < run_end{2});

            else

                run_2_spikes = [];

            end

            sleep_1_spikes = cell_spikes_only(cell_spikes_only > sleep_start{1} & cell_spikes_only < sleep_end{1});

            if length(sleep_start) > 1
                sleep_2_spikes = cell_spikes_only(cell_spikes_only > sleep_start{2} & cell_spikes_only < sleep_end{2});

            else

                sleep_2_spikes = [];

            end

            shank_n = idx(cell_id,1);

            if ismember(shank_n,bla_list) == 1

                bla_spikes{end+1} = run_1_spikes;
                bla_spikes2{end+1} = run_2_spikes;

                bla_sleep_spikes{end+1} = sleep_1_spikes;
                bla_sleep_spikes2{end+1} = sleep_2_spikes;

                bla_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','bla','session',session,'rat',9,'cell_id',cell_id);

            elseif ismember(shank_n,central_list) == 1

                central_spikes{end+1} = run_1_spikes;
                central_spikes2{end+1} = run_2_spikes;

                central_sleep_spikes{end+1} = sleep_1_spikes;
                central_sleep_spikes2{end+1} = sleep_2_spikes;

                central_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','central','session',session,'rat',9,'cell_id',cell_id);

            end
            
        end

    end

end

xmls = getfn('E:\hc-14\Rat10','xml$');

xmls = xmls(cellfun('isempty',strfind(xmls,'p')));
xmls = xmls(cellfun('isempty',strfind(xmls,'run')));
xmls = xmls(cellfun('isempty',strfind(xmls,'smell')));

bla_locations = load('E:\hc-14\Rat10\Rat10-Info\Structures\BLA.mat').BLA;
central_locations = load('E:\hc-14\Rat10\Rat10-Info\Structures\CeCM.mat').CeCM;
hippo_locations = load('E:\hc-14\Rat10\Rat10-Info\Structures\Hpc.mat').Hpc;

for session = 1:length(xmls)

    SetCurrentSession(xmls{session})
    
    run_start = {};
    run_end = {};
    sleep_start = {};
    sleep_end = {};
    
    names = GetEvents('output','descriptions');
    times = GetEvents;

    for name = 1:length(names)

        if contains(names{name},'beginning') == 1 && contains(names{name},'run') == 1

            run_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'run') == 1

            run_end{end+1} = times(name);

        elseif contains(names{name},'beginning') == 1 && contains(names{name},'sleep') == 1

            sleep_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'sleep') == 1

            sleep_end{end+1} = times(name);

        end

    end

    % Get All Spikes
    spikes1=GetSpikeTimes('output','numbered');
    spikes2=GetSpikeTimes('output','full');
    spikes=[spikes2 spikes1(:,2)];
    spikes(spikes(:,3)==0,:)=[];
    spikes(spikes(:,3)==1,:)=[];

    % Remnumber IDs after removing MUA and artifacts
    ids=unique(spikes(:,4));
    for ii=1:length(ids)
      spikes(spikes(:,4)==ids(ii),4)=ii;
    end
    idx=unique(spikes(:,2:4),'rows'); % shank / cell/ ID

    if min(idx(:,3))==1 && sum(diff(idx(:,3))-1)==0
      disp('Renumbering OK')
    else
      error('Problem with index : aborting')
    end
    
    restrict_bla = bla_locations(:,1) == session;
    
    bla_list = bla_locations(restrict_bla,:);
    
    restrict_central = central_locations(:,1) == session;
    
    central_list = central_locations(restrict_central,:);
    
    restrict_hippo = hippo_locations(:,1) == session;
    
    hippo_list = hippo_locations(restrict_hippo,:);

    for cell_id = 1:length(idx)

        rule = spikes(:,4) == idx(cell_id,3);

        cell_spikes = spikes(rule);

        cell_spikes_only = cell_spikes(:,1);
        
        run_1_spikes = cell_spikes_only(cell_spikes_only > run_start{1} & cell_spikes_only < run_end{1});
        
        if length(run_start) > 1
            
            run_2_spikes = cell_spikes_only(cell_spikes_only > run_start{2} & cell_spikes_only < run_end{2});
            
        else
            
            run_2_spikes = [];
            
        end
        
        sleep_1_spikes = cell_spikes_only(cell_spikes_only > sleep_start{1} & cell_spikes_only < sleep_end{1});
        
        if length(sleep_start) > 1
            
            sleep_2_spikes = cell_spikes_only(cell_spikes_only > sleep_start{2} & cell_spikes_only < sleep_end{2});
            
        else
            
            sleep_2_spikes = [];
            
        end

        shank_n = idx(cell_id,1);
            
        if ismember(shank_n,bla_list) == 1
            
            bla_spikes{end+1} = run_1_spikes;
            bla_spikes2{end+1} = run_2_spikes;
            
            bla_sleep_spikes{end+1} = sleep_1_spikes;
            bla_sleep_spikes2{end+1} = sleep_2_spikes;
            
            bla_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','bla','session',session,'rat',10,'cell_id',cell_id);
            
        elseif ismember(shank_n,central_list) == 1
            
            central_spikes{end+1} = run_1_spikes;
            central_spikes2{end+1} = run_2_spikes;
            
            central_sleep_spikes{end+1} = sleep_1_spikes;
            central_sleep_spikes2{end+1} = sleep_2_spikes;
            
            central_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','central','session',session,'rat',10,'cell_id',cell_id);
            
        elseif ismember(shank_n,hippo_list) == 1
            
            hippocampus_spikes{end+1} = run_1_spikes;
            hippocampus_spikes2{end+1} = run_2_spikes;
            
            hippocampus_sleep_spikes{end+1} = sleep_1_spikes;
            hippocampus_sleep_spikes2{end+1} = sleep_2_spikes;
            
            hippocampus_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','hippocampus','session',session,'rat',10,'cell_id',cell_id);
            
        end

    end

end  

xmls = getfn('E:\hc-14\Rat11','xml$');

xmls = xmls(cellfun('isempty',strfind(xmls,'p')));
xmls = xmls(cellfun('isempty',strfind(xmls,'run')));
xmls = xmls(cellfun('isempty',strfind(xmls,'smell')));

bla_locations = readmatrix('E:\hc-14\Rat11\Rat11-Info\rat_11_bla.csv');
central_locations = readmatrix('E:\hc-14\Rat11\Rat11-Info\rat_11_central.csv');

for session = 1:length(xmls)

    SetCurrentSession(xmls{session})
    
    run_start = {};
    run_end = {};
    sleep_start = {};
    sleep_end = {};
    
    names = GetEvents('output','descriptions');
    times = GetEvents;

    for name = 1:length(names)

        if contains(names{name},'beginning') == 1 && contains(names{name},'run') == 1

            run_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'run') == 1

            run_end{end+1} = times(name);

        elseif contains(names{name},'beginning') == 1 && contains(names{name},'sleep') == 1

            sleep_start{end+1} = times(name);

        elseif contains(names{name},'end') == 1 && contains(names{name},'sleep') == 1

            sleep_end{end+1} = times(name);

        end

    end

    % Get All Spikes
    spikes1=GetSpikeTimes('output','numbered');
    spikes2=GetSpikeTimes('output','full');
    spikes=[spikes2 spikes1(:,2)];
    spikes(spikes(:,3)==0,:)=[];
    spikes(spikes(:,3)==1,:)=[];

    % Remnumber IDs after removing MUA and artifacts
    ids=unique(spikes(:,4));
    for ii=1:length(ids)
      spikes(spikes(:,4)==ids(ii),4)=ii;
    end
    idx=unique(spikes(:,2:4),'rows'); % shank / cell/ ID

    if min(idx(:,3))==1 && sum(diff(idx(:,3))-1)==0
      disp('Renumbering OK')
    else
      error('Problem with index : aborting')
    end
    
    restrict_bla = bla_locations(:,1) == session;
    
    bla_list = bla_locations(restrict_bla,:);
    
    restrict_central = central_locations(:,1) == session;
    
    central_list = central_locations(restrict_central,:);
    
    for cell_id = 1:length(idx)

        rule = spikes(:,4) == idx(cell_id,3);

        cell_spikes = spikes(rule);

        cell_spikes_only = cell_spikes(:,1);
        
        run_1_spikes = cell_spikes_only(cell_spikes_only > run_start{1} & cell_spikes_only < run_end{1});
        
        if length(run_start) > 1
            
            run_2_spikes = cell_spikes_only(cell_spikes_only > run_start{2} & cell_spikes_only < run_end{2});
            
        else
            
            run_2_spikes = [];
            
        end
        
        sleep_1_spikes = cell_spikes_only(cell_spikes_only > sleep_start{1} & cell_spikes_only < sleep_end{1});
        
        if length(sleep_start) > 1
            
            sleep_2_spikes = cell_spikes_only(cell_spikes_only > sleep_start{2} & cell_spikes_only < sleep_end{2});
            
        else
            
            sleep_2_spikes = [];
            
        end

        shank_n = idx(cell_id,1);
            
        if ismember(shank_n,bla_list) == 1
            
            bla_spikes{end+1} = run_1_spikes;
            bla_spikes2{end+1} = run_2_spikes;
            
            bla_sleep_spikes{end+1} = sleep_1_spikes;
            bla_sleep_spikes2{end+1} = sleep_2_spikes;
            
            bla_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','bla','session',session,'rat',11,'cell_id',cell_id);
            
        elseif ismember(shank_n,central_list) == 1
            
            central_spikes{end+1} = run_1_spikes;
            central_spikes2{end+1} = run_2_spikes;
            
            central_sleep_spikes{end+1} = sleep_1_spikes;
            central_sleep_spikes2{end+1} = sleep_2_spikes;
            
            central_cell_info{end+1} = struct('dataset','buzsaki_2','species','rat','brain_area','central','session',session,'rat',11,'cell_id',cell_id);
            
        end

    end

end  