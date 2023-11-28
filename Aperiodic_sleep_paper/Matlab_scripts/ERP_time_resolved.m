%% ERPs of the same time frame as the eexponent values

%fieldtrip
clear;
addpath(genpath('/home/b1044271/Toolboxes/obob_ownft'));
obob_init_ft;

%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;

path_R='/home/b1044271/Columbia/Preprocessed/Stage_epoched/New_stage_trans/stims/Last/';
dataRow_r   =struct2cell(dir(fullfile(path_R , '*_DummyN.set'))');
files_D1 =dataRow_r(1,:);

dataRow_r   =struct2cell(dir(fullfile(path_R , '*_DummyR.set'))');
files_D2 =dataRow_r(1,:);

dataRow_S  =struct2cell(dir(fullfile(path_R , '*_StimsN*.set'))');
files_S1 =dataRow_S(1,:);

dataRow_S  =struct2cell(dir(fullfile(path_R , '*_StimsR*.set'))');
files_S2 =dataRow_S(1,:);

for i = 1:length(files_S1)
    
    EEG_D1 = pop_loadset([path_R files_D1{i}]);
    EEG_S1 = pop_loadset([path_R files_S1{i}]);
    EEG_D2 = pop_loadset([path_R files_D2{i}]);
    EEG_S2 = pop_loadset([path_R files_S2{i}]); 

  cfg=[];
  cfg.keeptrials = 'yes';
   
      FVKCep1=eeglab2fieldtrip(EEG_D1,'preprocessing','none');
      DUM_N{i}=ft_timelockanalysis(cfg,FVKCep1);

       
      UFVKCep1=eeglab2fieldtrip(EEG_S1,'preprocessing','none');
      STM_N{i}=ft_timelockanalysis(cfg,UFVKCep1);
      
            FVKCep2=eeglab2fieldtrip(EEG_D2,'preprocessing','none');
      DUM_R{i}=ft_timelockanalysis(cfg,FVKCep2);

       
      UFVKCep2=eeglab2fieldtrip(EEG_S2,'preprocessing','none');
      STM_R{i}=ft_timelockanalysis(cfg,UFVKCep2);
end