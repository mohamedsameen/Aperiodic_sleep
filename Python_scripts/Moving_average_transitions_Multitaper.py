# Using multitaper approach to provide a high temporal resolution for estimating the PSDs across the whole night for fine-grained estimation of the aperiodic model parameters over the whole night.
# The resukts are used for analysing evoked responses (c.f. Figure 7)
##########################################################
import mne
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
# Import the FOOOF object
from fooof import FOOOF
from fooof import FOOOFGroup
# Import a utility to download and load example data
from fooof.utils.download import load_fooof_data
from pathlib import Path
import glob
from math import floor
from mne.time_frequency import tfr_multitaper


# get the subjects list
Data_path = '/home/b1044271/Columbia/Preprocessed/Stage_epoched/Stim_NoStim/NEW/ArtRej/WAKE/*.set'
subj_files = sorted(glob.glob(Data_path))

electrode = 'E257'
fs = 250

# Settings for Welch's
t=5
f_max=45
SETTINGS_B  = { 'method' : 'welch', 'average' : None, 'fmin' :1 , 'fmax':f_max, 'n_fft': fs*t, 'n_overlap': fs*t*0.5}

# Settings for FOOOF
SETTINGS_F1={'max_n_peaks':8, 'aperiodic_mode':'knee'}
SETTINGS_F2={'max_n_peaks':8, 'aperiodic_mode':'fixed'}

fm1 = FOOOFGroup(**SETTINGS_F1)
for x in subj_files:
    EEG = mne.read_epochs_eeglab(os.path.join(Data_path, x))
    EEG = EEG.pick(electrode, exclude=[]) # select Cz for further analysis

    EEG_psd1 = tfr_multitaper(EEG, freqs=np.arange(1,45.5,0.5), n_cycles=np.arange(1,45.5,0.5), use_fft=True, return_itc=False,
    average=False, decim=2)

    #EEG_psd2 = EEG.compute_psd(**SETTINGS_B) 
	
    #fm1 = FOOOFGroup(**SETTINGS_F2)
    fm2 = FOOOFGroup(**SETTINGS_F1)

    fm2.fit(EEG_psd1.freqs, np.transpose(np.mean(np.squeeze(EEG_psd1._data),0)), [EEG_psd1.freqs[0] , EEG_psd1.freqs[-1]])
    fm2.save(x[79:-4] +'_FOOOFed_MT',file_path = '/home/b1044271/Columbia/Results/Time-resolved/Transitions/Cz/Stim_NoStim/NEW/AR/Wake/', save_results=True)

    #fm2.fit(EEG_psd2.freqs, np.transpose(np.mean(np.squeeze(EEG_psd2._data),0)), [EEG_psd2.freqs[0] , EEG_psd2.freqs[-1]])
    #fm2.save(x[55:-4] +'_FOOOFed_W_Fixed',  file_path = '/home/b1044271/Columbia/Results/Time-resolved/Transitions/Cz/KC/NEW', save_results=True)


np.save('/home/b1044271/Columbia/Results/Time-resolved/Transitions/Cz/Stim_NoStim/NEW/AR/Wake/Freqs_transitions_MT', EEG_psd1.freqs)
#np.save('/home/b1044271/Columbia/Results/Time-resolved/Transitions/Cz/Freqs_transitions_W', EEG_psd2.freqs)
