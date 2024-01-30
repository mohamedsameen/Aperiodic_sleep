% epoching the preprocessed EEG data for temporally resolved analysis of aperiodic activity
% code takes continuous .set files and returns epoched .set files..............

clear all;

% add eeglab stuff to path
%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;



save_path = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/FS_noFS/';
%% paths for markers
path_kc='/home/b1044271/EEGsleep/EEGlab/Done/detections/KC/new/KC_2019/';
path_stage      = '/home/b1044271/EEGsleep/SleepStaging/mat/';
path_data        = '/home/b1044271/Columbia/Preprocessed/Better_ica/';
path_sp            = '/home/b1044271/EEGsleep/EEGlab/Done/detections/SP-whole/spindleFeatures/spindleResults/Markers/34/';
remMarkers2   = '/home/b1044271/FSON_REM/REM_markers/recent_stages_BV/Markers_June23/';

key_SP={'FS_2_start','SS_2_start'};


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

for subj = 1:19
        if subj==2 || subj==9
            continue
    elseif subj < 10
         VP=sprintf('VP0%d_notch2_ica_done.set',subj);
            SS=strcat(path_stage,sprintf('VP0%d_SS.txt',subj));
            FS=strcat(path_sp,sprintf('VP0%d_SP_C3.txt',subj));
      
     else
         VP=sprintf('VP%d_notch2_ica_done.set',subj);
          SS=strcat(path_stage,sprintf('VP%d_SS.txt',subj));
            FS=strcat(path_sp,sprintf('VP%d_SP_C3.txt',subj));

        end
    
    % read data (replace with arnod delorms new function)
   EEG=pop_loadset([path_data VP]); % load set data
   EEG=pop_resample(EEG, 128);
   eventstruct=importevent(SS,EEG.event,EEG.srate,'fields',{'type','latency'},'timeunit',NaN);EEG.event=eventstruct;
   eventstruct=importevent(FS,EEG.event,EEG.srate,'fields',{'type','latency'},'timeunit',NaN);EEG.event=eventstruct;
   eeg_checkset(EEG,'eventconsistency'); %align the imported events
    %EEG = pop_resample(EEG, 250);
   %% Epoch events
   EEGS2   = pop_epoch(EEG,{'stage_2'},[-30 0]); %ALL stages 2 


%% Epoch stims  (KC no KC)
  
    %FV
    ALLep=pop_epoch(EEGS2,UFV,[-5 5]);
    ALLep2=pop_select(ALLep,'time',[0 2]);
    
      ALL_FS=[]; 
      No_FS=[]; 
      
   for i= 1:length(ALLep2.epoch)
            epoch=[ALLep2.epoch(i).eventtype];
            
            if isempty(epoch)
                continue
            end
            
            FS=[];
            FS=find(~cellfun(@isempty,regexp(epoch,strjoin(key_SP,'|'))));

            if ~isempty(FS)
                ALL_FS(i)= 1; 
            end
   end
   FSs  = find(ismember(1:length(ALLep.epoch),find(ALL_FS)));
   No_FS=find(~ismember(1:length(ALLep.epoch),find(ALL_FS)));
   
   
   %% 
    
   % NO FS
    nFSep=pop_select(ALLep,'trial',No_FS);    
    nFSep=pop_select(nFSep,'trial',datasample(1:length(nFSep.epoch),length(FSs)*2,'Replace',false)); 
   
    
    [nFSep  , rmepochs] = pop_autorej(nFSep  ,'nogui','on');epoch_props = epoch_properties(nFSep  ,1: nFSep.nbchan);
    BadEpochs   = min_z(epoch_props);  
    nFSep   = pop_rejepoch(nFSep, BadEpochs,0);
    
       
    FSep=pop_select(ALLep,'trial',FSs);
    [FSep  , rmepochs] = pop_autorej(FSep  ,'nogui','on');epoch_props = epoch_properties(FSep  ,1: FSep.nbchan);
    BadEpochs   = min_z(epoch_props);  
    FSep   = pop_rejepoch(FSep, BadEpochs,0);
    
     
    
    mins=min([length(FSep.epoch) length(nFSep.epoch)]);

    
    nFSep2=pop_select(nFSep,'trial',datasample(1:length(nFSep.epoch),mins,'Replace',false));
    FSep2=pop_select(FSep,'trial',datasample(1:length(FSep.epoch),mins,'Replace',false));

    
    %save
    pop_saveset(FSep2,'filename', [EEG.setname(1:end-30) 'StimFS_UFV'], 'filepath', save_path);
    pop_saveset(nFSep2,'filename', [EEG.setname(1:end-30) 'StimNoFS_UFV'], 'filepath', save_path);
    
end



