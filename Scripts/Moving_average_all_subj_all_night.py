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


# get the staging list
path_stage = Path('/home/b1044271/EEGsleep/SleepStaging/mat/mne2/')
stage_files = os.listdir(path_stage)
stage_files = [file for file in stage_files]
stage_files = sorted(stage_files)

# get the subjects list
Data_path = '/home/b1044271/Columbia/Preprocessed/Better_ica/'
subj_files = os.listdir(Data_path)
subj_files = [file for file in subj_files]
subj_files = sorted(subj_files)

# Create path for results
path_results = Path('/home/b1044271/Columbia/Results/Time-resolved')


t = 5 #in seconds
t2 = 10
f_max =  45
electrode = 'E257'
fs = 250
# Settings for the analyses
SETTINGS_B  = { 'method' : 'welch', 'average' : 'mean', 'fmin' :1 , 'fmax':f_max, 'n_fft': fs*t, 'n_overlap': fs*t*0.5}

Slope_nk = np.zeros([17,100000])* np.nan
Slope_k = np.zeros([17,100000])* np.nan
Knee_k = np.zeros([17,100000])* np.nan
r2_nk = np.zeros([17,100000])* np.nan
r2_k = np.zeros([17,100000])* np.nan

# START
i= 0
for S in subj_files
  EEG = mne.io.read_raw_eeglab(os.path.join(Data_path, S)) # read raw .set file
  EEG1 = EEG.pick(electrode, exclude=[]) # select Cz for further analysis
  EEG_seg = mne.make_fixed_length_epochs(EEG1, duration = 20, reject_by_annotation = 'True', overlap = 15)
  EEG_psd = EEG_seg.compute_psd(**SETTINGS_B)

  #FOOOF settings
  SETTINGS_F1={'max_n_peaks':8, 'aperiodic_mode':'fixed'}
  SETTINGS_F2={'max_n_peaks':8, 'aperiodic_mode':'knee'}

  fm1 = FOOOFGroup(**SETTINGS_F1)
  fm2 = FOOOFGroup(**SETTINGS_F2)

  fm1.fit(EEG_psd._freqs, np.squeeze(EEG_psd._data[0:100]), [EEG_psd._freqs[0] , EEG_psd._freqs[-1]])
  fm2.fit(EEG_psd._freqs, np.squeeze(EEG_psd._data), [EEG_psd._freqs[0] , EEG_psd._freqs[-1]])

  Slope_nk[i, 0:len(fm1.get_params('aperiodic_params','exponent'))] = fm1.get_params('aperiodic_params','exponent')
  Slope_k[i, 0:len(fm2.get_params('aperiodic_params','exponent'))] = fm2.get_params('aperiodic_params','exponent')
  r2_nk[i, 0:len(fm1.get_params('r_squared'))] = fm1.get_params('r_squared')
  r2_k[i, 0:len(fm1.get_params('r_squared'))] = fm2.get_params('r_squared')
  Knee_k[i, 0:len(fm1.get_params('aperiodic_params','knee'))] = fm1.get_params('aperiodic_params','knee')
  i = i +1