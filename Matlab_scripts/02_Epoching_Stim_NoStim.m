% epoching the preprocessed EEG data for temporally resolved analysis of aperiodic activity
% code takes continuous .set files and returns epoched .set files..............

clear all;

% add eeglab stuff to path
%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;

save_path = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/Stim_NoStim/NEW/Artif_Rej/';
%% paths for markers
path_kc='/home/b1044271/EEGsleep/EEGlab/Done/detections/KC/new/KC_2019/';
path_stage      = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/Stage_Markers/';
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


%% Wake stims
UFVSON_W1 = {'DIN11','DIN10'};
UFVSON_W2 = strcat(UFVSON_W1,'_NA');
UFVSON_W   = [UFVSON_W1 UFVSON_W2];


FVSON_W1    = {'DIN12','DIN20'};
FVSON_W2    = strcat(FVSON_W1,'_NA');
FVSON_W      = [FVSON_W1 FVSON_W2];

UFVUN_W1 = {'DIN22','DIN33', 'DIN30','DIN50'};
UFVUN_W2 = strcat(UFVUN_W1,'_NA');
UFVUN_W   = [UFVUN_W1 UFVUN_W2];


FVUN_W1 = {'DIN23','DIN34', 'DIN40', 'DIN60'};
FVUN_W2 = strcat(FVUN_W1,'_NA');
FVUN_W   = [FVUN_W1 FVUN_W2];


FVW=[FVSON_W FVUN_W];
UFVW=[UFVSON_W UFVUN_W];

SONW=[FVSON_W UFVSON_W];
UNsW=[FVUN_W UFVUN_W];

ALLStimsW = [FVW UFVW];

for subj = 1:19
        if subj==2 || subj==9
            continue
    elseif subj < 10
         VP=sprintf('VP0%d_notch2_ica_done.set',subj);
            SS=strcat(path_stage,sprintf('VP0%d_SS_250x.txt',subj));
      
     else
         VP=sprintf('VP%d_notch2_ica_done.set',subj);
          SS=strcat(path_stage,sprintf('VP%d_SS_250x.txt',subj));

        end
    
    % read data (replace with arnod delorms new function)
   EEG=pop_loadset([path_data VP]); % load set data

   eventstruct=importevent(SS,EEG.event,EEG.srate,'fields',{'type','latency'},'timeunit',NaN);EEG.event=eventstruct;
   eeg_checkset(EEG,'eventconsistency'); %align the imported events

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
        EEGnostim.event(1,x+i).latency = i*1000; %sampling freq = 128Hz, so 4 secs = steps of 1000 datapoints
        EEGnostim.event(1,x+i).urevent = 4;
    end
    eeg_checkset(EEGnostim,'eventconsistency');
    
 
   %% Epoch events
    EEGSNR  = pop_epoch(EEGstim,{'stage_2', 'stage_3'},[-30 0]);
    EEGSRM  = pop_epoch(EEGstim,{'stage_5'},[-30 0]);
    
    EEGSW = pop_epoch(EEGstim,{'stage_0'},[-30 0]);

    
    EEGNNR  = pop_epoch(EEGnostim,{'stage_2', 'stage_3'},[-30 0]);
    EEGNRM  = pop_epoch(EEGnostim,{'stage_5'},[-30 0]);
    
    EEGNW  = pop_epoch(EEGnostim,{'stage_0'},[-30 0]);

    
        %% get all stims in NREM and REM
StimNR =  pop_epoch(EEGSNR,ALLStims,[-5 5]);
      [StimNR, rmepochs] = pop_autorej( StimNR,'nogui','on');epoch_props = epoch_properties( StimNR,1: StimNR.nbchan);
    BadEpochs   = min_z(epoch_props); StimNR = pop_rejepoch( StimNR, BadEpochs,0);
     
StimRM =  pop_epoch(EEGSRM,ALLStims,[-5 5]);
        [StimRM, rmepochs] = pop_autorej( StimRM,'nogui','on');epoch_props = epoch_properties( StimRM,1: StimRM.nbchan);
    BadEpochs   = min_z(epoch_props); StimRM = pop_rejepoch( StimRM, BadEpochs,0);   

StimW =  pop_epoch(EEGSW,ALLStimsW,[-5 5]);
        [StimW, rmepochs] = pop_autorej( StimW,'nogui','on');epoch_props = epoch_properties( StimW,1: StimW.nbchan);
    BadEpochs   = min_z(epoch_props); StimW = pop_rejepoch( StimW, BadEpochs,0);   

    % get 10s epoch of no stimulation
    DummyNR = pop_epoch(EEGNNR,{'St'},[-5 5]);
    [DummyNR, rmepochs] = pop_autorej( DummyNR,'nogui','on');epoch_props = epoch_properties( DummyNR,1: DummyNR.nbchan);
    BadEpochs   = min_z(epoch_props); DummyNR = pop_rejepoch( DummyNR, BadEpochs,0);     

    DummyRM = pop_epoch(EEGNRM,{'St'},[-5 5]);
     [DummyRM, rmepochs] = pop_autorej( DummyRM,'nogui','on');epoch_props = epoch_properties( DummyRM,1: DummyRM.nbchan);
    BadEpochs   = min_z(epoch_props); DummyRM = pop_rejepoch( DummyRM, BadEpochs,0);      
    
    
    DummyW = pop_epoch(EEGNW,{'St'},[-5 5]);
     [DummyW, rmepochs] = pop_autorej( DummyW,'nogui','on');epoch_props = epoch_properties( DummyW,1: DummyW.nbchan);
    BadEpochs   = min_z(epoch_props); DummyW = pop_rejepoch( DummyW, BadEpochs,0); 
        
        minE = min([length(StimNR.epoch) length(DummyNR.epoch) ]);
       minR =  min([ length(StimRM.epoch) length(DummyRM.epoch) ]);
              minW =  min([ length(StimW.epoch) length(DummyW.epoch) ]);

       
       trials(subj,1)=minE; trials(subj,2)=minR; trials(subj,3)=minW; 
        
       SNep=pop_select(StimNR,'trial',datasample(1:length(StimNR.epoch) ,minE,'Replace',false));
       DNep=pop_select(DummyNR,'trial',datasample(1:length(DummyNR.epoch) ,minE,'Replace',false));
       
       SRep=pop_select(StimRM,'trial',datasample(1:length(StimRM.epoch) ,minR,'Replace',false));
       DRep=pop_select(DummyRM,'trial',datasample(1:length(DummyRM.epoch) ,minR,'Replace',false));
       
       SWep=pop_select(StimW,'trial',datasample(1:length(StimW.epoch) ,minW,'Replace',false));
       DWep=pop_select(DummyW,'trial',datasample(1:length(DummyW.epoch) ,minW,'Replace',false));

       % SAVING
    pop_saveset(SNep ,'filename', [EEG.setname(1:5) 'StimsN'], 'filepath', save_path);
    pop_saveset(SRep ,'filename', [EEG.setname(1:5) 'StimsR'], 'filepath', save_path);
    pop_saveset(DNep,'filename', [EEG.setname(1:5) 'DummyN'], 'filepath', save_path);
    pop_saveset(DRep,'filename', [EEG.setname(1:5) 'DummyR'], 'filepath', save_path); 
    pop_saveset(SWep ,'filename', [EEG.setname(1:5) 'StimsW'], 'filepath', save_path);
    pop_saveset(DWep ,'filename', [EEG.setname(1:5) 'DummyW'], 'filepath', save_path);

end



