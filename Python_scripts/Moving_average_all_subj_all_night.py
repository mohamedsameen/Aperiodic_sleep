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
path_results = Path('/home/b1044271/Columbia/Results/Time-resolved/ALL_electrodes/')


# select electrodes (if empty, uses all electrodes)
electrode = 'E257'

# Set parameters for calculating
t     = 15 #in seconds
f_min =  1 # maximum frequency
f_max =  45 # maximum frequency
fs    = 250 #sampling freq

# Settings for the frequency calculations (Welch's method)
SETTINGS_B  = { 'method' : 'welch', 'average' : 'mean', 'fmin' :f_min , 'fmax':f_max, 'n_fft': fs*t, 'n_overlap': fs*t*0.5}

# FOOF settings
SETTINGS_F1={'max_n_peaks':8, 'aperiodic_mode':'fixed'}
SETTINGS_F2={'max_n_peaks':8, 'aperiodic_mode':'knee'}

# Helper function for paths
def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

# Vectors for storing results per subject
Slope_nk = np.zeros([17,100000])* np.nan
Slope_k = np.zeros([17,100000])* np.nan
Knee_k = np.zeros([17,100000])* np.nan
r2_nk = np.zeros([17,100000])* np.nan
r2_k = np.zeros([17,100000])* np.nan
Off_nk = np.zeros([17,100000])* np.nan
Off_k = np.zeros([17,100000])* np.nan
E_nk = np.zeros([17,100000])* np.nan
E_k = np.zeros([17,100000])* np.nan


# START
i= 0
for S in subj_files:
    EEG = mne.io.read_raw_eeglab(os.path.join(Data_path, S)) # read raw .set file

    # select Cz for further analysis
    if electrode:
        EEG = EEG.pick(electrode, exclude=[])

    EEG_seg = mne.make_fixed_length_epochs(EEG, duration = 15, reject_by_annotation = 'True', overlap = 14)
    EEG_psd = EEG_seg.compute_psd(**SETTINGS_B)

    # FOOFGroup to add paramters from all channels
    fm1 = FOOOFGroup(**SETTINGS_F1)
    fm2 = FOOOFGroup(**SETTINGS_F2)
	
    fm1.fit(EEG_psd._freqs, np.squeeze(EEG_psd._data), [EEG_psd._freqs[0] , EEG_psd._freqs[-1]])
    fm1.save(S[0:4] + '_AllNight_NK',  file_path = path_results / S[0:4], save_results=True)

    fm2.fit(EEG_psd._freqs, np.squeeze(EEG_psd._data), [EEG_psd._freqs[0] , EEG_psd._freqs[-1]])
    fm2.save(S[0:4] + '_AllNight_K',  file_path = path_results / S[0:4], save_results=True)


    Slope_nk[i, 0:len(fm1.get_params('aperiodic_params','exponent'))] = fm1.get_params('aperiodic_params','exponent')
    Slope_k[i, 0:len(fm2.get_params('aperiodic_params','exponent'))] = fm2.get_params('aperiodic_params','exponent')

    r2_nk[i, 0:len(fm1.get_params('r_squared'))] = fm1.get_params('r_squared')
    r2_k[i, 0:len(fm2.get_params('r_squared'))] = fm2.get_params('r_squared')

    E_nk[i, 0:len(fm1.get_params('r_squared'))] = fm1.get_params('error')
    E_k[i, 0:len(fm2.get_params('r_squared'))] = fm2.get_params('error')


    Knee_k[i, 0:len(fm2.get_params('aperiodic_params','knee'))] = fm2.get_params('aperiodic_params','knee')

    Off_nk[i, 0:len(fm1.get_params('aperiodic_params','offset'))] = fm1.get_params('aperiodic_params','offset')
    Off_k[i, 0:len(fm2.get_params('aperiodic_params','offset'))] = fm2.get_params('aperiodic_params','offset')

    i = i+1

# saving the results in numpy files
np.save(str(path_results) +  '/'  + 'Slope_nk_mean_15_1x',Slope_nk)
np.save(str(path_results) +  '/'  + 'Slope_k_mean_15_1x',Slope_k)
np.save(str(path_results) +  '/'  + 'r2_k_mean_15_1x',r2_k)
np.save(str(path_results) +  '/'  + 'r2_nk_mean_15_1x',r2_nk)
np.save(str(path_results) +  '/'  + 'Knee_k_mean_15_1x',Knee_k)
np.save(str(path_results) +  '/'  + 'Offset_nk_mean_15_1x',Off_nk)
np.save(str(path_results) +  '/'  + 'Offset_k_mean_15_1x',Off_k)
np.save(str(path_results) +  '/'  + 'Error_nk_mean_15_1x',E_nk)
np.save(str(path_results) +  '/'  + 'Error_k_mean_15_1x',E_k)

