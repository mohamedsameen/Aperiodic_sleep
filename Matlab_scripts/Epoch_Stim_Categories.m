% epoching the preprocessed EEG data for temporally resolved analysis of aperiodic activity
% code takes continuous .set files and returns epoched .set files..............

clear all;

% add eeglab stuff to path
%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;



save_path = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/Categories/';
%% paths for markers
path_stage      = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/Stage_Markers/';
path_data        = '/home/b1044271/Columbia/Preprocessed/Better_ica/';



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

SON=[FVSON UFVSON];
UNs=[FVUNs UFVUNs];

ALLStims = [FV UFV];

for subj = 8:19
        
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


      %% Epoch events
    EEGN  = pop_epoch(EEG,{'stage_2', 'stage_3'},[-30 0]);
    EEGR  = pop_epoch(EEG,{'stage_5'},[-30 0]);
    
    
    %% REM
    
    FVR=pop_epoch(EEGR,[FV],[-5 5]);
    [FVR, rmepochs] = pop_autorej( FVR,'nogui','on');epoch_props = epoch_properties( FVR,1: FVR.nbchan);
    BadEpochs   = min_z(epoch_props); FVR = pop_rejepoch( FVR, BadEpochs,0);
%     
    UFVR=pop_epoch(EEGR,[UFV],[-5 5]);
    [UFVR, rmepochs] = pop_autorej( UFVR,'nogui','on');epoch_props = epoch_properties( UFVR,1: UFVR.nbchan);
    BadEpochs   = min_z(epoch_props); UFVR = pop_rejepoch( UFVR, BadEpochs,0);
%         
    SONR=pop_epoch(EEGR,[SON],[-5 5]);
    [SONR, rmepochs] = pop_autorej( SONR,'nogui','on');epoch_props = epoch_properties( SONR,1: SONR.nbchan);
    BadEpochs   = min_z(epoch_props); SONR = pop_rejepoch( SONR, BadEpochs,0);
%        
    UNR=pop_epoch(EEGR,[UNs],[-5 5]);
    [UNR, rmepochs] = pop_autorej( UNR,'nogui','on');epoch_props = epoch_properties( UNR,1: UNR.nbchan);
    BadEpochs   = min_z(epoch_props); UNR = pop_rejepoch( UNR, BadEpochs,0);
%         
    minR = min([length(FVR.epoch) length(UFVR.epoch) length(SONR.epoch) length(UNR.epoch)]);
%         
    FVRep=pop_select(FVR,'trial',datasample(1:length(FVR.epoch) ,minR,'Replace',false));
    UFVRep=pop_select(UFVR,'trial',datasample(1:length(UFVR.epoch) ,minR,'Replace',false));
    SONRep=pop_select(SONR,'trial',datasample(1:length(SONR.epoch) ,minR,'Replace',false));
    UNRep=pop_select(UNR,'trial',datasample(1:length(UNR.epoch) ,minR,'Replace',false));
      
%% NREM

        FVN=pop_epoch(EEGN,[FV],[-5 5]);
            [FVN, rmepochs] = pop_autorej( FVN,'nogui','on');epoch_props = epoch_properties( FVN,1: FVN.nbchan);
    BadEpochs   = min_z(epoch_props); FVN = pop_rejepoch( FVN, BadEpochs,0);
%     
        UFVN=pop_epoch(EEGN,[UFV],[-5 5]);
            [UFVN, rmepochs] = pop_autorej( UFVN,'nogui','on');epoch_props = epoch_properties( UFVN,1: UFVN.nbchan);
    BadEpochs   = min_z(epoch_props); UFVN = pop_rejepoch( UFVN, BadEpochs,0);
%         
    SONN=pop_epoch(EEGN,[SON],[-5 5]);
        [SONN, rmepochs] = pop_autorej( SONN,'nogui','on');epoch_props = epoch_properties( SONN,1: SONN.nbchan);
    BadEpochs   = min_z(epoch_props); SONN = pop_rejepoch( SONN, BadEpochs,0);
%         
    UNN=pop_epoch(EEGN,[UNs],[-5 5]);
            [UNN, rmepochs] = pop_autorej( UNN,'nogui','on');epoch_props = epoch_properties( UNN,1: UNN.nbchan);
    BadEpochs   = min_z(epoch_props); UNN = pop_rejepoch( UNN, BadEpochs,0);
% 
    minN = min([length(FVN.epoch) length(UFVN.epoch) length(SONN.epoch) length(UNN.epoch)]);
    
    FVNep=pop_select(FVN,'trial',datasample(1:length(FVN.epoch) ,minN,'Replace',false));
    UFVNep=pop_select(UFVN,'trial',datasample(1:length(UFVN.epoch) ,minN,'Replace',false));
    SONNep=pop_select(SONN,'trial',datasample(1:length(SONN.epoch) ,minN,'Replace',false));
    UNNep=pop_select(UNN,'trial',datasample(1:length(UNN.epoch) ,minN,'Replace',false));
 
        %% SAVING
        pop_saveset(FVNep ,'filename', [EEG.setname(1:5) 'FVN'], 'filepath', save_path);
                pop_saveset(UFVNep ,'filename', [EEG.setname(1:5) 'UFVN'], 'filepath', save_path);
        pop_saveset(SONNep ,'filename', [EEG.setname(1:5) 'SONN'], 'filepath', save_path);
        pop_saveset(UNNep ,'filename', [EEG.setname(1:5) 'UNN'], 'filepath', save_path);

        pop_saveset(FVRep ,'filename', [EEG.setname(1:5) 'FVR'], 'filepath', save_path);
                pop_saveset(UFVRep ,'filename', [EEG.setname(1:5) 'UFVR'], 'filepath', save_path);
        pop_saveset(SONRep ,'filename', [EEG.setname(1:5) 'SONR'], 'filepath', save_path);
        pop_saveset(UNRep ,'filename', [EEG.setname(1:5) 'UNR'], 'filepath', save_path);
              
end