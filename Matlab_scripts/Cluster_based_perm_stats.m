% cluster based permutation analysis of the Time-resolved plots in the 
% aperiodic_sleep project

%% start fieldtrip
addpath(genpath('/home/b1044271/Toolboxes/obob_ownft'));
obob_init_ft;

%% load the actual data we need (Transitions)

X1 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/N2_of_N3comp.txt'));
X2 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/N3_of_N3comp.txt'));

X3 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/N2_of_N1comp_KF.txt'));
X4 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/N1_of_N1comp_KF.txt'));

X5 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/NREM_2-3_comp.txt'));
X6 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/REM_comp.txt'));

X7 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/N1_of_N1toN2comp_KF.txt'));
X8 =  table2array(readtable('/home/b1044271/Columbia/Results/Permutation/KF/N2_of_N1toN2comp_KF.txt'));


%% Evoked responses

X9 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/Stims_NREM_16.txt'));
X10 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/Dummy_NREM_16.txt'));

X11 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/Stims_REM_16.txt'));
X12 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/Dummy_REM_16.txt'));

X13 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/FV_NREM.txt'));
X14 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/UFV_NREM.txt'));

X15 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/FV_REM.txt'));
X16 =  table2array(readtable('/home/b1044271/Columbia/Results/Evoked/UFV_REM.txt'));


%% PSDs
x0 =  table2array(readtable('/home/b1044271/Columbia/Results/peakPSD_KC.txt'));
x00 =  table2array(readtable('/home/b1044271/Columbia/Results/peakPSD_noKC.txt'));

%% cluster based

% load a fieldtrip erp structure
load('/home/b1044271/EEGsleep/EEGlab/newEEGLAB/EEGlab/Results/ERP/All_elecs/erp_FV.mat')

%Grand average
cfg = [];
 cfg.latency = [-0.5 2];
cfg.keepindividual = 'yes'; 
cfg.channel = {'E36'};
all_FV= ft_timelockgrandaverage(cfg,erp_FV{:});

% Parameters
cfg = [];
cfg.method = 'montecarlo';       % use the Monte Carlo Method to calculate the significance probability
cfg.statistic = 'ft_statfun_depsamplesT'; % use the independent samples T-statistic as a measure to                             % evaluate the effect at the sample level
cfg.correctm = 'cluster';
cfg.clusteralpha = 0.05;         % alpha level of the sample-specific test statistic that                              % will be used for thresholding
cfg.clusterstatistic = 'maxsum'; % test statistic that will be evaluated under the                             % permutation distribution.
% cfg.latency=[125 1125];                         % in the clustering algorithm (default=0).
%cfg.minnbchan = 2;
%cfg.neighbours    = neighbours;
cfg.tail = 0;                    % -1, 1 or 0 (default = 0); one-sided or two-sided test
cfg.clustertail = 0;
cfg.alpha = 0.025;               % alpha level of the permutation test
cfg.numrandomization = 5000;      % number of draws from the permutation distribution
% cfg.avgoverchan      = 'yes';
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
cfg.design  = design;   

%% PSDs
FV_KCs=permute(x0,[1,3,2]);
UFV_KCs=permute(x00,[1,3,2]);

all_UFV = all_FV;


all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;

all_FV.time  = 1:0.5:45;
all_UFV.time =  1:0.5:45;

[stat_p] = ft_timelockstatistics(cfg, all_UFV, all_FV);

%% N3 V N2
FV_KCs=permute(X1,[1,3,2]);
UFV_KCs=permute(X2,[1,3,2]);

all_UFV = all_FV;


all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 
all_FV.time  = -60:2:58;
all_UFV.time =  -60:2:58;
[stat_n] = ft_timelockstatistics(cfg, all_UFV, all_FV);

%% N1 V N2
FV_KCs=permute(X4,[1,3,2]);
UFV_KCs=permute(X3,[1,3,2]);

all_UFV = all_FV;


all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 
all_FV.time  = -60:2:58;
all_UFV.time =  -60:2:58;
[stat_n2] = ft_timelockstatistics(cfg, all_UFV, all_FV);

%% NREM V REM
FV_KCs=permute(X6,[1,3,2]);
UFV_KCs=permute(X5,[1,3,2]);

all_UFV = all_FV;

all_FV.time  = -60:2:58;
all_UFV.time =  -60:2:58;

all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 

[stat_n3] = ft_timelockstatistics(cfg, all_UFV, all_FV);

%% N1 to N1 or N2
FV_KCs=permute(X7,[1,3,2]);
UFV_KCs=permute(X8,[1,3,2]);

all_UFV = all_FV;

all_FV.time  = -60:2:58;
all_UFV.time =  -60:2:58;

all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;

[stat_n4] = ft_timelockstatistics(cfg, all_UFV, all_FV);

%% Auditory responses (NREM)
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
cfg.design  = design; 


FV_KCs=permute(X10,[1,3,2]);
UFV_KCs=permute(X9,[1,3,2]);

all_UFV = all_FV;

all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 
all_FV.time  = 1:1:1250;
all_UFV.time = 1:1:1250;
[stat_n5] = ft_timelockstatistics(cfg, all_UFV, all_FV);

%% Auditory responses (REM)
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
cfg.design  = design; 


FV_KCs=permute(X12,[1,3,2]);
UFV_KCs=permute(X11,[1,3,2]);

all_UFV = all_FV;

all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 
all_FV.time  = 1:1:1250;
all_UFV.time = 1:1:1250;
[stat_n6] = ft_timelockstatistics(cfg, all_UFV, all_FV);
%% FV UFV 
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
cfg.design  = design; 


FV_KCs=permute(X13,[1,3,2]);
UFV_KCs=permute(X14,[1,3,2]);

all_UFV = all_FV;

all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 
all_FV.time  = 1:1:1250;
all_UFV.time = 1:1:1250;
[stat_n6] = ft_timelockstatistics(cfg, all_UFV, all_FV);




%% SON UN
FV_KCs=permute(X15,[1,3,2]);
UFV_KCs=permute(X16,[1,3,2]);

all_UFV = all_FV;

all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 
all_FV.time  = 1:1:1250;
all_UFV.time = 1:1:1250;
[stat_n7] = ft_timelockstatistics(cfg, all_UFV, all_FV);

%% KC no KC

FV_KCs=permute(X15,[1,3,2]);
UFV_KCs=permute(X16,[1,3,2]);

all_UFV = all_FV;


all_FV.individual = FV_KCs;
all_UFV.individual = UFV_KCs;
% 
all_FV.time  = 1:1:640;
all_UFV.time = 1:1:640;

[stat_n8] = ft_timelockstatistics(cfg, all_FV, all_UFV);


%%  Cohen d

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


inference = ft_timelockstatistics(cfg, all_UFV, all_FV);

% then the calculations
grandavgFIC_sel = all_FV;
%grandavgFIC_sel.individual   = squeeze(FV_KCs);


grandavgFC_sel  = all_UFV;
%grandavgFC_sel.powspctrm = squeeze(UFV_KCs);
x1 = nan(17,1);
x2 = nan(17,1);

for i=1:17

  % construct a 3-dimensional Boolean array to select the data from this participant
  sel3d = false(size(grandavgFIC_sel.individual ));
  sel3d(i,:) = inference.negclusterslabelmat==2;

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

