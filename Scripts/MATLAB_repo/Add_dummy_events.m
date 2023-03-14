%Add dummy markers to EEG files in mne
%prepare the marker here and move them to mne

clear all;

toolPath = 'D:\Mohamed\Codes\';
filePath = '/home/b1044271/FSON/FSON_raw';
save_path = '/home/b1044271/Columbia/Dummy/';


% add eeglab stuff to path
%EEGLab
addpath(genpath('/home/b1044271/Toolboxes/eeglab14_1_1b'));
eeglab; close gcf;


cd (filePath)
files = dir('*.set');



for rec = 1:numel(files)
    
    % read data (replace with arnod delorms new function)
    EEG = pop_loadset( [filePath '/' files(rec).name] );
    
    name1 = EEG.filename(1:end-7);
    
    EEGm = EEG.xmax;
    fs         = EEG.srate;
    
    A =  250: 250: EEGm*250;
    B = zeros(length(A),1);
    C= repmat (-1, length(A),1);
        
     t=table(A',B,C);

    writetable(t,[save_path EEG.filename(1:end-7) 'dum_mark.txt'],'FileType','text','WriteVariableNames' ,false);
    A=[];B=[];C=[];t=[];
    
    
         
end
    
    

