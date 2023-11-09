% epoching the preprocessed EEG data for temporally resolved analysis of aperiodic activity
% code takes continuous .set files and returns epoched .set files..............

clear all;

% add eeglab stuff to path
%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;
save_path = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/New_stage_trans/stims/';

%% paths for markers
path_stage      = '/home/b1044271/EEGsleep/SleepStaging/mat/';
path_data        = '/home/b1044271/Columbia/Preprocessed/Better_ica/';
path_sp            = '/home/b1044271/EEGsleep/EEGlab/Done/detections/SP-whole/spindleFeatures/spindleResults/Markers/34/';
remMarkers2   = '/home/b1044271/FSON_REM/REM_markers/recent_stages_BV/Markers_June23/';

%% load No-stimulation periods time points
load('/home/b1044271/EEGsleep/nostimdata/NoStimPeriod');
load('/home/b1044271/EEGsleep/nostimdata/NoStimPeriod2');
load('/home/b1044271/EEGsleep/nostimdata/NoStimPeriod3');
load('/home/b1044271/EEGsleep/nostimdata/NoStimPeriod4');
load('/home/b1044271/EEGsleep/nostimdata/NostimData');

%% STIMS
UFVSON1={'DIN100','DIN101','DIN102','DIN103','DIN104','DIN105','DIN12','DIN13','DIN81','DIN82','DIN15','DIN11'};

FVSON1={'DIN12','DIN106','DIN107','DIN108','DIN109','DIN110','DIN111','DIN21','DIN22','DIN23','DIN83','DIN84','DIN25'};

UFVUNs1={'DIN22','DIN112','DIN113','DIN114','DIN115','DIN116','DIN117','DIN32','DIN33','DIN85','DIN86'...
    'DIN124','DIN125','DIN126','DIN127','DIN128','DIN129','DIN52','DIN53','DIN89','DIN90','DIN35','DIN33','DIN55'};

FVUNs1={'DIN118','DIN119','DIN120','DIN121','DIN122','DIN123','DIN42','DIN43','DIN87','DIN88'...
    'DIN130','DIN131','DIN132','DIN133','DIN134','DIN135','DIN62','DIN63','DIN91','DIN92','DIN45','DIN34','DIN65'};

FVSON2=strcat(FVSON1,'_NA');
FVSON=[FVSON1 FVSON2];

UFVSON2=strcat(UFVSON1,'_NA');
UFVSON=[UFVSON1 UFVSON2];

FVUNs2=strcat(FVUNs1,'_NA');
FVUNs=[FVUNs1 FVUNs2];

UFVUNs2=strcat(UFVUNs1,'_NA');
UFVUNs=[UFVUNs1 FVUNs2];

FV=[FVSON FVUNs];
UFV=[UFVSON UFVUNs];

ALLStims = [FV UFV];


for subj = 18:19
        if subj==2 || subj==9
            continue
    elseif subj < 10
         VP=sprintf('VP0%d_notch2_ica_done.set',subj);
         SS=strcat(path_stage,sprintf('VP0%d_SS.txt',subj));      
     else
         VP=sprintf('VP%d_notch2_ica_done.set',subj);
         SS=strcat(path_stage,sprintf('VP%d_SS.txt',subj));
        end
    
    % read data (replace with arnod delorms new function)
   EEG=pop_loadset([path_data VP]); % load set data
   eventstruct=importevent(SS,EEG.event,EEG.srate,'fields',{'type','latency'},'timeunit',NaN);EEG.event=eventstruct;

   eeg_checkset(EEG,'eventconsistency'); %align the imported events

   %% Epoch events  (N2 transitions)
%    for i = 1:length({EEG.event.type})
%         EEG.event(i).type = sprintf(['%d_'  EEG.event(i).type], i) ;
%    end
%    
%        stage = {EEG.event.type};
%         X =find(~cellfun(@isempty,regexp({EEG.event(:).type},'stage_2')));
%         Y=stage(X+1);
% 
%         N1s =find(ismember(Y, 'stage_1'));
%         N3s =find(ismember(Y, 'stage_3'));
%         
%         X1 = find(~cellfun(@isempty,regexp(Y,'stage_1')));
%         X2 = find(~cellfun(@isempty,regexp(Y,'stage_2')));
%         X3 = find(~cellfun(@isempty,regexp(Y,'stage_3')));
%         XR = find(~cellfun(@isempty,regexp(Y,'stage_5')));
% 
%         N1s = Y(X1);   N2s = Y(X2);    N3s = Y(X3);  Rms = Y(XR); 
% 
%         N2_N1 = pop_epoch(EEG, N1s, [-90 90]);
%         N2_N3 = pop_epoch(EEG, N3s, [-90 90]);
%          N2_N2 = pop_epoch(EEG, N2s, [-90 90]);       
%                 N2_R = pop_epoch(EEG, Rms, [-90 90]);
% 
% 
%     pop_saveset(N2_N1,'filename', [EEG.setname(1:5) 'N2N1'], 'filepath', save_path);
%     pop_saveset(N2_N3,'filename', [EEG.setname(1:5) 'N2N3'], 'filepath', save_path);
%     pop_saveset(N2_N2,'filename', [EEG.setname(1:5) 'N2N2'], 'filepath', save_path);
%     pop_saveset(N2_R,'filename', [EEG.setname(1:5) 'N2R'], 'filepath', save_path);

    %% Epoch events (Stimuli vs no stimulation) (NREM2,3 and REM)    
    
     %split into stim and nostim
    hi_limit=[NoStimPeriod(subj,2), NoStimPeriod2(subj,2), NoStimPeriod3(subj,2), NoStimPeriod4(subj,2)];
    low_limit=[NoStimPeriod(subj,1), NoStimPeriod2(subj,1),NoStimPeriod3(subj,1),NoStimPeriod4(subj,1)];
    
    if subj == 13
        EEGstim=pop_select(EEG,'time',[0 low_limit(1)+4; hi_limit(1) low_limit(2)+4; hi_limit(2) low_limit(3)+4; hi_limit(3) low_limit(4)+4; hi_limit(4) EEG.xmax]);
        EEGnostim=pop_select(EEG,'time',[low_limit(1) hi_limit(1); low_limit(2) hi_limit(2); low_limit(3) hi_limit(3)]);
    else
        EEGstim=pop_select(EEG,'time',[0 low_limit(1)+4; hi_limit(1) low_limit(2)+4; hi_limit(2) low_limit(3)+4; hi_limit(3) low_limit(4)+4; hi_limit(4) EEG.xmax]);
        EEGnostim=pop_select(EEG,'time',[low_limit(1) hi_limit(1); low_limit(2) hi_limit(2); low_limit(3) hi_limit(3); low_limit(4) hi_limit(4)]);
    end
    
    % insert dummy markers in the nostim segments
    epochs=EEGnostim.xmax/4;
    x=length(EEGnostim.event);%index of last existing event 
    for i = 1:epochs-1 % 
        EEGnostim.event(1,x+i).type = 'St';
        EEGnostim.event(1,x+i).latency = i*512; %sampling freq = 128Hz, so 4 secs = steps of 1000 datapoints
        EEGnostim.event(1,x+i).urevent = 4;
    end
    eeg_checkset(EEGnostim,'eventconsistency');
    
    
    
    
    EEGSNR  = pop_epoch(EEGstim,{'stage_2', 'stage_3'},[-30 0]);
    EEGSRM  = pop_epoch(EEGstim,{'stage_5'},[-30 0]);
        
    EEGNNR  = pop_epoch(EEGnostim,{'stage_2', 'stage_3'},[-30 0]);
    EEGNRM  = pop_epoch(EEGnostim,{'stage_5'},[-30 0]);
    
        
    % get all stims in NREM and REM
    StimNR =  pop_epoch(EEGSNR,ALLStims,[-5 5]);
        StimRM =  pop_epoch(EEGSRM,ALLStims,[-5 5]);

    % get 10s epoch of no stimulation


    DummyNR = pop_epoch(EEGNNR,{'St'},[-5 5]);
    DummyRM = pop_epoch(EEGNRM,{'St'},[-5 5]);

%% SAVING
    pop_saveset(StimNR ,'filename', [EEG.setname(1:5) 'StimsN'], 'filepath', save_path);
    pop_saveset(StimRM ,'filename', [EEG.setname(1:5) 'StimsR'], 'filepath', save_path);
    pop_saveset(DummyNR,'filename', [EEG.setname(1:5) 'DummyN'], 'filepath', save_path);
    pop_saveset(DummyRM,'filename', [EEG.setname(1:5) 'DummyR'], 'filepath', save_path); 
    
    
        
end