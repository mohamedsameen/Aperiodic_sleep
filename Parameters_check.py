import mne
import numpy as np
import matplotlib.pyplot as plt

# Import the FOOOF object
from fooof import FOOOF

# Import a utility to download and load example data
from fooof.utils.download import load_fooof_data

EEG = mne.read_epochs_eeglab('/home/b1044271/Columbia/Test_dataset.set')
EEG1 = EEG.pick('E257', exclude=[]) # select Cz for further analysis

#Now we select epochs and average over all epochs
N1s = EEG1['stage_1']
N2s = EEG1['stage_2']
N3s = EEG1['stage_3']
REs = EEG1['stage_5']
AWs = EEG1['stage_0']

# set parameters for frq transformation
fs = 250  #sampling freq
SETTINGS_B = { 'method' : 'welch', 'average' : 'mean', 'fmin' :1 , 'fmax' : 70}
Time_segments = [2, 5, 10, 15] #in seconds

# Frequency transformation welch's method from 1 to 70Hz
N1={}
N2={}
N3={}
AW={}
RM={}

i = 0
for x in Time_segments:
    i = i+1
    N1[x] = N1s.compute_psd(**SETTINGS_B, n_fft=fs*x) #N1
    N2[x] = N2s.compute_psd(**SETTINGS_B, n_fft=fs*x) #N2
    N3[x] = N3s.compute_psd(**SETTINGS_B, n_fft=fs*x)
    AW[x] = AWs.compute_psd(**SETTINGS_B, n_fft=fs*x)
    RM[x] = REs.compute_psd(**SETTINGS_B, n_fft=fs*x)

# Now plot to get a feeling
fig, ax = plt.subplots()
ax.plot(TF_Wa._freqs, np.mean(np.squeeze(TF_N1a),0), color = 'black')
ax.plot(TF_Wb._freqs, np.mean(np.squeeze(TF_N1b),0), color = 'blue')
ax.plot(TF_Wc._freqs, np.mean(np.squeeze(TF_N1c),0), color = 'red')
ax.plot(TF_Wd._freqs, np.mean(np.squeeze(TF_N1d),0), color = 'green')
plt.xscale("log")
plt.ylim(0, 0.03e-9)
plt.show()

# model fit on different freq characteristics
SETTINGS_F1={'max_n_peaks':8, 'aperiodic_mode':'fixed'}
SETTINGS_F2={'max_n_peaks':8, 'aperiodic_mode':'knee'}
freq_range = [N1[2]._freqs[0] , N1[2]._freqs[-1]]

fooof_a = {}
fooof_b = {}

i = 0
variables = [N1, N2, N3, AW, RM] # loop over stages
for  A in variables:
    for keys, values in A.items():  # loop over time windows
        fm1 = FOOOF(**SETTINGS_F1)
        fm1.fit(A[keys]._freqs, np.mean(np.squeeze(A[keys]._data),0), freq_range) # fit no knee
        fooof_a[i] = fm1.get_results()

        fm2 = FOOOF(**SETTINGS_F2)
        fm2.fit(A[keys]._freqs, np.mean(np.squeeze(A[keys]._data),0), freq_range) # fit with a knee
        fooof_b[i] = fm2.get_results()

        i=i+1
