% read EEGLab format events and convert them to mne format
cd /home/b1044271/EEGsleep/SleepStaging/mat
save_path = '/home/b1044271/EEGsleep/SleepStaging/mat/mne/';
for subj = 1:19
if subj==2 || subj==9
continue
end
if subj < 10
load(sprintf('VP0%d_stage',subj));
A=eval(sprintf('VP0%d_stage',subj));
name1=sprintf('VP0%d_SS_250_mne.txt',subj);
else
load(sprintf('VP%d_stage',subj));
A=eval(sprintf('VP%d_stage',subj));
name1=sprintf('VP%d_SS_250_mne.txt',subj);
end
B=A(:,2);B=B*250; Bn = [1;B(1:end)]  ;
C=A(:,1); Cn = [9;C(1:end)]  ;
D=zeros(length(Bn),1);
t=table(Bn,D,Cn);
writetable(t,[save_path name1],'FileType','text','WriteVariableNames' ,false);
B=[];Bn=[];C=[];Cn=[];D=[];t=[];
end