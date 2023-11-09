%preprocessing of hdEEG data using EEGLab
%developed by Dr. Dominik PJ Heib
%modified by Mohamed Ameen, M.Sc.
%

clear all

toolPath = 'D:\Mohamed\Codes\';
filePath = '/home/b1044271/FSON/FSON_raw';
savePath = '/home/b1044271/FSON/FSON_raw';


% add eeglab stuff to path
%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;


% start matlabpool with max local (physical) workers
%-----------------------------------
mypool = gcp;
if mypool.Connected~=1
    numCores = feature('numcores');
    parpool(numCores);
end


cd (filePath)
files = dir('*.set');

% define channels of no interest (face and neckCHannels)
chansOfnoInterest  = [238, 234, 230, 226, 225, 219, 239, 235, 231, 227, 218, 240, 236, 232, 228, 217, 237, 233, 229, 216,...
    241, 244, 248, 252, 253, 67, 242, 245, 249, 254, 73, 243, 246, 250, 255, 82, 91, 256, 251, 247,...
    208, 199, 187, 174, 165, 145, 133, 120, 111, 102,...
    209, 200, 188, 175, 166, 156, 146, 134, 121, 112, 103, 92,...
    93,  104, 113, 122, 135, 147, 157, 167, 176, 189, 201,...
    31];


for rec = 11:numel(files)
    
    eeglab;close gcf
    % read data (replace with arnod delorms new function)
    EEG = pop_loadset( [filePath '/' files(rec).name] );
    
%     physio=258:length(EEG.chanlocs);
    % delete chansOfnoInterest
    EEG = pop_select(EEG, 'nochannel', [chansOfnoInterest]);
    
    
    % trim first and last 2 secs
    %EEG = pop_select( EEG,'time',[2 EEG.xmax-2] );
    
    
    % ds data (uses Matlabs resample...anti aliasing is included 0.9*freq)
%     EEG = pop_resample( EEG, 128);

EEG = pop_eegfiltnew(EEG, 49, 51,[], 1); % NOTCH
            % bandpass filter data
    EEG = pop_eegfiltnew(EEG, 0.1, []);
%     EEG = pop_cleanline(EEG, 'bandwidth',2,'chanlist',1:EEG.nbchan ,'computepower',1,'linefreqs',[50 100],'newversion',0,'normSpectrum',0,'p',0.01,'pad',2,'plotfigures',0,'scanforlines',0,'sigtype','Channels','taperbandwidth',2,'tau',100,'verb',1,'winsize',4,'winstep',1);
%     EEG = pop_cleanline(EEG, 'bandwidth',2,'chanlist',1:EEG.nbchan ,'computepower',1,'linefreqs',50 ,'newversion',0,'normSpectrum',0,'p',0.01,'pad',2,'plotfigures',0,'scanforlines',0,'sigtype','Components','taperbandwidth',2,'tau',100,'verb',1,'winsize',4,'winstep',1);
    % add the REF channel back
    % add the REF channel back
    EEG.nbchan                            = EEG.nbchan+1;
    EEG.data(end+1,:)                     = zeros(1, EEG.pnts);
    EEG.chanlocs(1,EEG.nbchan).labels     = 'E257';
    EEG.chanlocs(1,EEG.nbchan).Y          = EEG.chaninfo.ndchanlocs(4).Y;
    EEG.chanlocs(1,EEG.nbchan).X          = EEG.chaninfo.ndchanlocs(4).X;
    EEG.chanlocs(1,EEG.nbchan).Z          = EEG.chaninfo.ndchanlocs(4).Z;
    EEG.chanlocs(1,EEG.nbchan).sph_theta  = EEG.chaninfo.ndchanlocs(4).sph_theta;
    EEG.chanlocs(1,EEG.nbchan).sph_phi    = EEG.chaninfo.ndchanlocs(4).sph_phi;
    EEG.chanlocs(1,EEG.nbchan).sph_radius = EEG.chaninfo.ndchanlocs(4).sph_radius;
    EEG.chanlocs(1,EEG.nbchan).theta      = EEG.chaninfo.ndchanlocs(4).theta;
    EEG.chanlocs(1,EEG.nbchan).radius     = EEG.chaninfo.ndchanlocs(4).radius;
 

    % Do robust average reference and remember bad channels
    % Referencing parameters
    params.referenceChannels    = 1:EEG.nbchan-1; % scalp channels to use for initial average reference
    params.evaluationChannels   = 1:EEG.nbchan-1; % scalp channels that will contribute to the robust reference
    params.rereferencedChannels = 1:EEG.nbchan; % scalp+external channels that will be referenced to the robust reference
    
    
    % Bad channel detection parameters
    params.badTimeThreshold            = 0.1;
    params.highFrequencyNoiseThreshold = 8;
    params.robustDeviationThreshold    = 13;
    params.ransacOff                   = true; % turned off as usually too aggressive
    [EEG, referenceOut]                = performReference(EEG, params);
    
        
    EEG=pop_runica(EEG,'icatype','runica', 'extended', 1); 
%     % epoch data
%     EEG    = pop_epoch( EEG, markerList, markerEpoching);
  %   icaEEG = EEG; % EEG set with all epochs. ICA Matrix is copid into this set later on
%      icaEEG.sanity.interpolatedChans = referenceOut.interpolatedChannels.all;
%     
    % run bad epoch detection and reject bad epoches
%     [EEG, rmepochs] = pop_autorej( EEG,'nogui','on');
%     epoch_props = epoch_properties(EEG,1:EEG.nbchan);
%     BadEpochs   = min_z(epoch_props);
%     EEG         = pop_rejepoch(EEG, BadEpochs,0);
%     
    
    %check if enough data points for suffiecien ic decomp.
%     icaEEG.sanity.AMICA1ok = ~floor(sqrt(size(EEG.data(:, :), 2) / 30)) < 35;
    
    
    % run Amica
%     [weights, sphere, mods] = runamica15(EEG.data(:,:), 'num_chans', EEG.nbchan,...
%         'outdir', [savePath  files(rec).name(1,1:end-4) '_icaOut'] ,...
%         'pcakeep', 35, 'num_models', 1,...
%         'do_reject', 1, 'numrej', 15, 'rejsig', 3, 'rejint', 1);
% %     
% %     % Add AMICA matrices to EEG data & compute ICA activations
%     EEG.icaweights = weights;
%     EEG.icasphere = sphere;
%     EEG.etc.amica = mods;
%     EEG = eeg_checkset(EEG, 'ica'); % Compute ICA activations
    
    % check for shitty decompositions..delete those epochs and rerun ica
%     EEG = pop_eegthresh( EEG, 0, 1:size(EEG.icaact,1), -1000, 1000, EEG.xmin, EEG.xmax, 0, 0);
%     EEG = pop_jointprob(EEG, 0, 1:size(EEG.icaact,1), 8.5, 999, 0, 1);
%     EEG = pop_rejkurt(EEG, 0, 1:size(EEG.icaact,1), 8, 999, 0, 1);
    
    % BadEpochs = dpjh_checkICA_results(EEG);
    % EEG       = pop_rejepoch(EEG, BadEpochs,0);
    
    %check if enough data points for suffiecien ic decomp.
%     icaEEG.sanity.AMICA2ok = ~floor(sqrt(size(EEG.data(:, :), 2) / 30)) < 35;
    
    
%      [weights, sphere, mods] = runamica15(EEG.data(:,:), 'num_chans', EEG.nbchan,...

%          'outdir', [savePath  files(rec).name(1,1:end-4) '_icaOut'],...
%          'pcakeep', 35, 'num_models', 1,...
%          'do_reject', 1, 'numrej', 15, 'rejsig', 3, 'rejint', 1);
    
    % save bad ICs
%     [EEG, cfg] = eeg_SASICA(EEG,cfg);
    
    
    %copy weights to original_epoched data
%     icaEEG.icaweights = weights;
%     icaEEG.icasphere = sphere;
%     icaEEG.etc.amica = mods;
%     icaEEG = eeg_checkset(icaEEG, 'ica'); % Compute ICA activations
%     icaEEG.setname = strcat(files(rec).name(1,1:end-4),'_ica');
%     icaEEG.filename = [filePath '\' files(rec).name];
%     icaEEG.filefilePath = filePath;
%     icaEEG.reject.gcompreject= EEG.reject.gcompreject;
%     icaEEG.reject.SASICA = EEG.reject.SASICA;
    
    EEG.filename = [filePath '/' files(rec).name];
    EEG.setname = strcat(files(rec).name(1,1:end-4),'_ica_notch2');
    pop_saveset( EEG, 'filename', EEG.setname, 'filepath', savePath);
    
end
%eegplot(EEG.data, 'srate', EEG.srate, 'data2', a.data)





