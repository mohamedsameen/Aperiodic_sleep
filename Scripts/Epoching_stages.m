clear all;

toolPath = 'D:\Mohamed\Codes\';
filePath = '/home/b1044271/FSON/FSON_raw';
save_path = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/';


% add eeglab stuff to path
%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;


cd (filePath)
files = dir('*.set');
path_stage= '/home/b1044271/EEGsleep/SleepStaging/mat/';
path_data  = '/home/b1044271/FSON/FSON_files/';

for subj = 1:numel(files)
        if subj==2 || subj==9
            continue
    elseif subj < 10
         VP=sprintf('VP0%d_all_newica.set',subj);
            SS=strcat(path_stage,sprintf('VP0%d_SS.txt',subj));        
     else
         VP=sprintf('VP%d_all_newica.set',subj);
            SS=strcat(path_stage,sprintf('VP%d_SS.txt',subj));
    end
    % read data (replace with arnod delorms new function)
    EEG=pop_loadset([path_data VP]); % load set data
    eventstruct=importevent(SS,EEG.event,EEG.srate,'fields',{'type','latency'},'timeunit',NaN);EEG.event=eventstruct;

    for i = 1:length({EEG.event.type})
        EEG.event(i).type = sprintf(['%d_'  EEG.event(i).type], i) ;
    end
    
        stage = {EEG.event.type};
        X =find(~cellfun(@isempty,regexp({EEG.event(:).type},'stage_2')));
        Y=stageN(X+1);
        Z = X+1;
        N1s =find(ismember(Y, 'stage_1'));
        N3s =find(ismember(Y, 'stage_3'));
    
        N21= Z(N1s);
        N23= Z(N3s);

    %create dummy markers every second
    epochs = 2:2:EEG.xmax;
    x=length(EEG.event);%index of last existing event 
    for i = 1:length(epochs) % \
        t = epochs(i);
        EEG.event(1,x+i).type = 'St';
        EEG.event(1,x+i).latency = t*EEG.srate; %sampling freq = 128Hz, so 4 secs = steps of 1000 datapoints
        EEG.event(1,x+i).urevent = 4;
    end
    eeg_checkset(EEG,'eventconsistency');
    
    %% Epoching finally the whole N2_Nx sequence
        N2_N1 = pop_epoch(EEG, stage(N21), [-60 20]);
        N2_N3 = pop_epoch(EEG, stage(N23), [-60 20]);
        
        N2_N1_ep =  pop_epoch(N2_N1,{'St'},[0 20]);
        N2_N3_ep =  pop_epoch(N2_N3,{'St'},[0 20]);
        
        pop_saveset(N2_N1_ep,'filename', EEG.setname, 'filepath', save_path);


    
    
end