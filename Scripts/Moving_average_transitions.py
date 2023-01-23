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


# get the subjects list
Data_path = '/home/b1044271/Columbia/Preprocessed/Stage_epoched'
subj_files = os.listdir(Data_path)
subj_files = [file for file in subj_files]
subj_files = sorted(subj_files)

t = 5 #in seconds
f_max =  45
electrode = 'E257'
fs = 250
# Settings for the analyses
SETTINGS_B  = { 'method' : 'welch', 'average' : 'mean', 'fmin' :1 , 'fmax':f_max, 'n_fft': fs*t, 'n_overlap': fs*t*0.5}
SETTINGS_F1={'max_n_peaks':8, 'aperiodic_mode':'fixed'}

fm1 = FOOOFGroup(**SETTINGS_F1)
for x in subj_files:
    EEG = mne.read_epochs_eeglab(os.path.join(Data_path, x))
    EEG1 = EEG.pick(electrode, exclude=[]) # select Cz for further analysis

    EEG_psd = EEG.compute_psd(**SETTINGS_B)

    fm1.fit(EEG_psd._freqs, np.squeeze(np.mean(EEG_psd._data, axis = 1)), [EEG_psd._freqs[0] , EEG_psd._freqs[-1]])
    fm1.save(x +'_K_trans',  file_path = '/home/b1044271/Columbia/Results/Time-resolved/E257/Transitions', save_results=True)
