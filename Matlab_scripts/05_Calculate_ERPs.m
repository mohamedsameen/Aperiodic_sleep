%% ERPs of the same time frame as the eexponent values

%fieldtrip
clear;
addpath(genpath('/home/b1044271/Toolboxes/obob_ownft'));
obob_init_ft;

%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;

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

ALL_S = [FV UFV SON UNs];
%% WAKE STIMS
% path_R='/home/b1044271/Columbia/Preprocessed/Stage_epoched/New_stage_trans/Cat/W/';
% dataRow_r   =struct2cell(dir(fullfile(path_R , '*_DummyW.set'))');
% files_D1 =dataRow_r(1,:);
% 
% dataRow_S  =struct2cell(dir(fullfile(path_R , '*_StimsW.set'))');
% files_S1 =dataRow_S(1,:);


%% SLEEP STIMS
path_R2='/home/b1044271/Columbia/Preprocessed/Stage_epoched/Stim_NoStim/NEW/ArtRej/';

dataRow_r   =struct2cell(dir(fullfile(path_R2 , '*_DummyR.set'))');
files_D2 =dataRow_r(1,:);

dataRow_S  =struct2cell(dir(fullfile(path_R2 , '*_StimsR.set'))');
files_S2 =dataRow_S(1,:);

dataRow_r   =struct2cell(dir(fullfile(path_R2 , '*_DummyN.set'))');
files_D3 =dataRow_r(1,:);

dataRow_S  =struct2cell(dir(fullfile(path_R2 , '*_StimsN.set'))');
files_S3 =dataRow_S(1,:);


for i = 1:length(files_S2)
    
    EEG_D2 = pop_loadset([path_R2 files_D2{i}]);
    EEG_S2 = pop_loadset([path_R2 files_S2{i}]); 
    EEG_D3 = pop_loadset([path_R2 files_D3{i}]);
    EEG_S3 = pop_loadset([path_R2 files_S3{i}]); 
    

  cfg=[];
  cfg.keeptrials = 'yes';
  
      % Sleep
      FVKCep2=eeglab2fieldtrip(EEG_D2,'preprocessing','none');
      DUM_R2{i}=ft_timelockanalysis(cfg,FVKCep2);

      UFVKCep2=eeglab2fieldtrip(EEG_S2,'preprocessing','none');
      STM_R2{i}=ft_timelockanalysis(cfg,UFVKCep2);
      
         
      FVKCep3=eeglab2fieldtrip(EEG_D3,'preprocessing','none');
      DUM_N2{i}=ft_timelockanalysis(cfg,FVKCep3);

      UFVKCep3=eeglab2fieldtrip(EEG_S3,'preprocessing','none');
      STM_N2{i}=ft_timelockanalysis(cfg,UFVKCep3);   
      
      
      
      
 
end
%% Baseline correction
%-----------------------%
cfg_b=[];
cfg_b.baseline=[-0.5 0];
cfg_b.baselinetype='relchange';
  
for subj = 1:17

     BE_StimR2{subj}=ft_timelockbaseline(cfg_b,STM_R2{subj});
     BE_DumR2{subj}=ft_timelockbaseline(cfg_b,DUM_R2{subj});
     
     BE_StimN2{subj}=ft_timelockbaseline(cfg_b,STM_N2{subj});
     BE_DumN2{subj}=ft_timelockbaseline(cfg_b,DUM_N2{subj});

end


%% Grandaverage

cfg_g=[];
cfg_g.latency=[-4 4];
cfg_g.channel = {'E257'};
cfg_g.keepindividual = 'yes'; 

NStim_all=ft_timelockgrandaverage(cfg_g, BE_StimN2{:});
NDum_all=ft_timelockgrandaverage(cfg_g, BE_DumN2{:});
RStim_all=ft_timelockgrandaverage(cfg_g, BE_StimR2{:});
RDum_all=ft_timelockgrandaverage(cfg_g, BE_DumR2{:});


NStim_all2 = NStim_all;
NStim_all2.individual(4,:,:)=[];

NDum_all2 = NDum_all;
NDum_all2.individual(4,:,:)=[];

RStim_all2 = RStim_all;
RStim_all2.individual(1,:,:)=[];

RDum_all2 = RDum_all;
RDum_all2.individual(1,:,:)=[];

%% Permutation

cfg=[];
cfg.statistic       ='ft_statfun_depsamplesT'; %between groups independant sampels statistics
cfg.method           ='montecarlo'; % Monte Carlo method for calculating the signif prob an estimate of the p-value under the permutation distribution.

cfg_g.channel = {'E257'};

cfg.correctm         = 'cluster';
cfg.clusteralpha     = 0.05;
cfg.clusterstatistic = 'maxsum';
cfg.avgoverchan      = 'yes';
%cfg.minnbchan        = 2;
cfg.tail             = 0;
cfg.clustertail      = 0;
cfg.alpha            = 0.025;
cfg.numrandomization = 5000;
cfg.uvar             = 1;
cfg.ivar             = 2;
% Design Matrix for T-Test (2 Conditions)
subj = 16;
design = zeros(2,2*subj);
for m = 1:subj
        design(1,m) = m;
end
for m = 1:subj
        design(1,subj+m) = m;
        
end
design(2,1:subj) = 1;
design(2,subj+1:2*subj) = 2;
cfg.design= design; 

% KC
rng(2)
[statsR]   = ft_timelockstatistics(cfg, RStim_all2, RDum_all2);
[statsN]   = ft_timelockstatistics(cfg, NStim_all2, NDum_all2);


%% Select Cz
cfg=[];
cfg.channel = {'E257'};

WStim_all = ft_selectdata(cfg, WStim_all);
WDum_all = ft_selectdata(cfg, WDum_all);
NStim_all = ft_selectdata(cfg, NStim_all);
NDum_all = ft_selectdata(cfg, NDum_all);
RStim_all = ft_selectdata(cfg, RStim_all);
RDum_all = ft_selectdata(cfg, RDum_all);

%% Saving

% Wstim_erp = squeeze(WStim_all.individual);
% save('Wstim_erp','Wstim_erp')
% 
Nstim_erp2 = squeeze(NStim_all2.individual);
save('Nstim_erp_final','Nstim_erp2')

Rstim_erp2 = squeeze(RStim_all2.individual);
save('Rstim_erp_final','Rstim_erp2')
% 
% 
% WDum_erp = squeeze(WDum_all.individual);
% save('WDum_erp','WDum_erp')
% 
NDum_erp2 = squeeze(NDum_all2.individual);
save('NDum_erp_final','NDum_erp2')

RDum_erp2 = squeeze(RDum_all2.individual);
save('RDum_erp_final','RDum_erp2')
% 
% Stim_erp = cat(3, Nstim_erp,Rstim_erp);
% Stim_erp2 = mean(Stim_erp,3);
% save('Stim_erp2','Stim_erp2')
% 
% 
% Dum_erp = cat(3, NDum_erp,RDum_erp);
% Dum_erp2 = mean(Dum_erp,3);
% save('Dum_erp2','Dum_erp2')
% 
times = RStim_all.time;
save('times_StimNoStim','times')


%% KC vs no KC
path_KC = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/KC_noKC/NEW/';

dataRow_k   =struct2cell(dir(fullfile(path_KC , '*StimKC_UFV.set'))');
files_K =dataRow_k(1,:);

dataRow_nk  =struct2cell(dir(fullfile(path_KC, '*StimNoKC_UFV.set'))');
files_nK =dataRow_nk(1,:);


for i = 1:length(files_K)
    

    EEG_K = pop_loadset([path_KC files_K{i}]); 
    EEG_nK = pop_loadset([path_KC files_nK{i}]); 
  
    EEG_K=pop_resample(EEG_K, 128)
    EEG_nK=pop_resample(EEG_nK, 128)
    
    mins=min([length(EEG_K.epoch) length(EEG_nK.epoch) ]);
    trials(i,1)=mins;
    
    EEG_K2    = pop_select(EEG_K,'trial',datasample(1:length(EEG_K.epoch),mins,'Replace',false));    
     EEG_nK2 = pop_select(EEG_nK,'trial',datasample(1:length(EEG_nK.epoch),mins,'Replace',false));    
    
   %% ERP
    cfg=[];
    cfg.keeptrials = 'yes';
   
    FVKCep1=eeglab2fieldtrip(EEG_K2,'preprocessing','none');
      STKC{i}=ft_timelockanalysis(cfg,FVKCep1);

      UFVKCep1=eeglab2fieldtrip(EEG_nK2,'preprocessing','none');
      STnKC{i}=ft_timelockanalysis(cfg,UFVKCep1);

end


cfg_b=[];
cfg_b.baseline=[-0.5 0];
cfg_b.baselinetype='relchange';
  
for subj = 1:17

     BE_StimKC{subj}=ft_timelockbaseline(cfg_b, STKC{subj});
     BE_StimNKC{subj}=ft_timelockbaseline(cfg_b, STnKC{subj});

end




%% Grandaverage

cfg_g=[];
cfg_g.latency=[-4 4];
cfg_g.keepindividual = 'yes'; 

KC_all=ft_timelockgrandaverage(cfg_g, BE_StimKC{:});
NKC_all=ft_timelockgrandaverage(cfg_g, BE_StimNKC{:});

%% Select Cz
cfg=[];
cfg.channel = {'E257'};

KC_all = ft_selectdata(cfg, KC_all);
NKC_all = ft_selectdata(cfg, NKC_all);

%% Permutation
cfg=[];
cfg.statistic       ='ft_statfun_depsamplesT'; %between groups independant sampels statistics
cfg.method           ='montecarlo'; % Monte Carlo method for calculating the signif prob an estimate of the p-value under the permutation distribution.

% cfg_g.channel = {'E257'};

cfg.correctm         = 'cluster';
cfg.clusteralpha     = 0.05;
cfg.clusterstatistic = 'maxsum';
cfg.avgoverchan      = 'yes';
%cfg.minnbchan        = 2;
cfg.tail             = 0;
cfg.clustertail      = 0;
cfg.alpha            = 0.025;
cfg.numrandomization = 5000;
cfg.uvar             = 1;
cfg.ivar             = 2;
% Design Matrix for T-Test (2 Conditions)
subj = 17;
design = zeros(2,2*subj);
for m = 1:subj
        design(1,m) = m;
end
for m = 1:subj
        design(1,subj+m) = m;
        
end
design(2,1:subj) = 1;
design(2,subj+1:2*subj) = 2;
cfg.design= design; 

% KC
[stats]   = ft_timelockstatistics(cfg, KC_all, NKC_all);


% SAVE
KC_erp = squeeze(KC_all.individual);
save('KC_erp','KC_erp')

NKC_erp = squeeze(NKC_all.individual);
save('NKC_erp','NKC_erp')

time_128 = KC_all.time;
save('time_128','time_128')
%% Spindles

path_SP = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/FS_noFS/';

dataRow_k   =struct2cell(dir(fullfile(path_SP , '*StimFS_UFV.set'))');
files_K =dataRow_k(1,:);

dataRow_nk  =struct2cell(dir(fullfile(path_SP, '*StimNoFS_UFV.set'))');
files_nK =dataRow_nk(1,:);


for i = 1:length(files_K)
    

    EEG_K = pop_loadset([path_SP files_K{i}]); 
    EEG_nK = pop_loadset([path_SP files_nK{i}]); 
  
    EEG_K=pop_resample(EEG_K, 128)
    EEG_nK=pop_resample(EEG_nK, 128)
    
    mins=min([length(EEG_K.epoch) length(EEG_nK.epoch) ]);
    trials(i,1)=mins;
    
    EEG_K2    = pop_select(EEG_K,'trial',datasample(1:length(EEG_K.epoch),mins,'Replace',false));    
     EEG_nK2 = pop_select(EEG_nK,'trial',datasample(1:length(EEG_nK.epoch),mins,'Replace',false));    
    
   %% ERP
    cfg=[];
    cfg.keeptrials = 'yes';
   
    FVKCep1=eeglab2fieldtrip(EEG_K2,'preprocessing','none');
      STKC{i}=ft_timelockanalysis(cfg,FVKCep1);

      UFVKCep1=eeglab2fieldtrip(EEG_nK2,'preprocessing','none');
      STnKC{i}=ft_timelockanalysis(cfg,UFVKCep1);

end

cfg_b=[];
cfg_b.baseline=[-0.5 0];
cfg_b.baselinetype='relchange';
  
for subj = 1:17

     BE_StimKC{subj}=ft_timelockbaseline(cfg_b, STKC{subj});
     BE_StimNKC{subj}=ft_timelockbaseline(cfg_b, STnKC{subj});

end
%% Grandaverage

cfg_g=[];
cfg_g.latency=[-4 4];
cfg_g.keepindividual = 'yes'; 

KC_all=ft_timelockgrandaverage(cfg_g, BE_StimKC{:});
NKC_all=ft_timelockgrandaverage(cfg_g, BE_StimNKC{:});

%% Select Cz
cfg=[];
cfg.channel = {'E257'};

KC_all = ft_selectdata(cfg, KC_all);
NKC_all = ft_selectdata(cfg, NKC_all);

%% Permutation
cfg=[];
cfg.statistic       ='ft_statfun_depsamplesT'; %between groups independant sampels statistics
cfg.method           ='montecarlo'; % Monte Carlo method for calculating the signif prob an estimate of the p-value under the permutation distribution.

% cfg_g.channel = {'E257'};

cfg.correctm         = 'cluster';
cfg.clusteralpha     = 0.05;
cfg.clusterstatistic = 'maxsum';
cfg.avgoverchan      = 'yes';
%cfg.minnbchan        = 2;
cfg.tail             = 0;
cfg.clustertail      = 0;
cfg.alpha            = 0.025;
cfg.numrandomization = 5000;
cfg.uvar             = 1;
cfg.ivar             = 2;
% Design Matrix for T-Test (2 Conditions)
subj = 17;
design = zeros(2,2*subj);
for m = 1:subj
        design(1,m) = m;
end
for m = 1:subj
        design(1,subj+m) = m;
        
end
design(2,1:subj) = 1;
design(2,subj+1:2*subj) = 2;
cfg.design= design; 

% KC
[stats]   = ft_timelockstatistics(cfg, KC_all, NKC_all);

%% Cohen

% first permutation over all possible iterations
cfg = [];
cfg.method      = 'montecarlo';
cfg.statistic   = 'ft_statfun_depsamplesT';
cfg.avgoverchan = 'yes';
cfg.alpha       = 0.05;
cfg.numrandomization = 'all';
cfg.correctm    = 'cluster';
cfg.correcttail = 'prob';
cfg.spmversion  = 'spm12';
cfg.uvar             = 1;
cfg.ivar             = 2;
subj = 16;
design = zeros(2,2*subj);
for m = 1:subj
        design(1,m) = m;
end
for m = 1:subj
        design(1,subj+m) = m;
end
design(2,1:subj) = 1;
design(2,subj+1:2*subj) = 2;
cfg.design= design; 


inference = ft_timelockstatistics(cfg, NStim_all2, NDum_all2);

% then the calculations
grandavgFIC_sel = NStim_all2;
%grandavgFIC_sel.individual   = squeeze(FV_KCs);


grandavgFC_sel  = NDum_all2;
%grandavgFC_sel.powspctrm = squeeze(UFV_KCs);
x1 = nan(16,1);
x2 = nan(16,1);

for i=1:16

  % construct a 3-dimensional Boolean array to select the data from this participant
  sel3d = false(size(grandavgFIC_sel.individual ));
  sel3d(i,:) = inference.negclusterslabelmat==1;

  % select the FIC data in the cluster for this participant, represent it as a vector
  tmp = grandavgFIC_sel.individual(sel3d(:));
  % compute the average over the cluster
  x1(i) = mean(tmp);

  % select the FC data in the cluster for this participant, represent it as a vector
  tmp = grandavgFC_sel.individual(sel3d(:));
  % compute the average over the cluster
  x2(i) = mean(tmp);
end

n1 = length(x1);
n2 = length(x2);

cd_TFKC= nanmean(x1-x2) ./ nanstd(x1-x2);

cd_TFKC

