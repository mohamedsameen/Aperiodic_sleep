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


# select electrodes (if empty, use all electrodes)
electrode = []

# Set parameters for calculating
t     = 5 #in seconds
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

# START
i= 0
for S in subj_files:
    EEG = mne.io.read_raw_eeglab(os.path.join(Data_path, S)) # read raw .set file

# select Cz for further analysis
    if electrode:
        EEG = EEG.pick(electrode, exclude=[])

    EEG_seg = mne.make_fixed_length_epochs(EEG, duration = 20, reject_by_annotation = 'True', overlap = 18)
    EEG_psd = EEG_seg.compute_psd(**SETTINGS_B)

    # Create a folder for each subject
    check_path(path_results / S[0:4])

    # Vectors for storing results per subject
    Slope_nk = np.zeros([183,100000])* np.nan
    Slope_k = np.zeros([183,100000])* np.nan
    Knee_k = np.zeros([183,100000])* np.nan
    r2_nk = np.zeros([183,100000])* np.nan
    r2_k = np.zeros([183,100000])* np.nan
    Off_nk = np.zeros([183,100000])* np.nan
    Off_k = np.zeros([183,100000])* np.nan

    # FOOFGroup to add paramters from all channels
    fm1 = FOOOFGroup(**SETTINGS_F1)
    fm2 = FOOOFGroup(**SETTINGS_F2)

    fm1.fit(EEG_psd._freqs, np.squeeze(EEG_psd._data), [EEG_psd._freqs[0] , EEG_psd._freqs[-1]])
    fm1.save(S[0:4] + '_AllNight_NK',  file_path = path_results / electrode, save_results=True)

    fm2.fit(EEG_psd._freqs, np.squeeze(EEG_psd._data), [EEG_psd._freqs[0] , EEG_psd._freqs[-1]])
    fm2.save(S[0:4] + '_AllNight_K',  file_path = path_results / electrode, save_results=True)

    Slope_nk[0:183, 0:len(fm1.get_params('aperiodic_params','exponent'))] = fm1.get_params('aperiodic_params','exponent')
    Slope_k[0:183, 0:len(fm2.get_params('aperiodic_params','exponent'))] = fm2.get_params('aperiodic_params','exponent')

    r2_nk[0:183, 0:len(fm1.get_params('r_squared'))] = fm1.get_params('r_squared')
    r2_k[0:183, 0:len(fm2.get_params('r_squared'))] = fm2.get_params('r_squared')

    Knee_k[0:183, 0:len(fm2.get_params('aperiodic_params','knee'))] = fm2.get_params('aperiodic_params','knee')

    Off_nk[0:183, 0:len(fm1.get_params('aperiodic_params','offset'))] = fm1.get_params('aperiodic_params','offset')
    Off_k[0:183, 0:len(fm2.get_params('aperiodic_params','offset'))] = fm2.get_params('aperiodic_params','offset')

    np.save(Path(path_results /S[0:4] /  'Slope_nk_mean_20_2'),Slope_nk)
    np.save(Path(path_results /S[0:4] /  'Slope_k_mean_20_2'),Slope_k)
    np.save(Path(path_results /S[0:4] /  'r2_k_mean_20_2'),r2_k)
    np.save(Path(path_results /S[0:4] /  'r2_nk_mean_20_2'),r2_nk)
    np.save(Path(path_results /S[0:4] /  'Knee_k_mean_20_2'),Knee_k)
    np.save(Path(path_results /S[0:4] /  'Offset_nk_mean_20_2'),Off_nk)
    np.save(Path(path_results /S[0:4] /  'Offset_k_mean_20_2'),Off_k)
