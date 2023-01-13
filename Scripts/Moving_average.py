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
# importing the random module
import random


# SET THE IMPORTANT parameters
single_subject = 0
whole_night = 1

t = 20 #in seconds
Overlap = 15
electrode = 'E257'

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

# Settings for the analyses
fs = 250
SETTINGS_B = { 'method' : 'welch', 'average' : 'mean', 'fmin' :1 , 'fmin' : 45 , 'n_fft': fs*t , 'n_overlap': fs*t*0.5}
path_results = Path('/home/b1044271/Columbia/Results/Time-resolved')
#FOOOF settings
SETTINGS_F1={'max_n_peaks':8, 'aperiodic_mode':'fixed'}
SETTINGS_F2={'max_n_peaks':8, 'aperiodic_mode':'knee'}
fm1 = FOOOFGroup(**SETTINGS_F1)
fm2 = FOOOFGroup(**SETTINGS_F2)

# Helper function for paths
def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

check_path(path_results / electrode)

if single_subject:
    EEG     = mne.io.read_raw_eeglab(os.path.join(Data_path, subj_files[random.randint(0,16)])) # read raw .set file
    EEG_seg = mne.make_fixed_length_epochs(EEG, duration = Time_segment, reject_by_annotation = 'True', overlap = Overlap)
    X       = EEG_seg.compute_psd(**SETTINGS_B)

    fm1.fit(X._freqs, np.squeeze(X._data), [X._freqs[0] , X._freqs[-1]])
    fm2.fit(X._freqs, np.squeeze(X._data), [X._freqs[0] , X._freqs[-1]])

    fm1.get_params('aperiodic_params','exponent')
    fm2.get_params('aperiodic_params','exponent')

else:
    i = 0

    Slope_nk = np.zeros([17,100000])* np.nan
    Slope_k = np.zeros([17,100000])* np.nan
    Knee_k = np.zeros([17,100000])* np.nan
    r2_nk = np.zeros([17,100000])* np.nan
    r2_k = np.zeros([17,100000])* np.nan

    for x in subj_files:

        if whole_night:
            EEG     = mne.io.read_raw_eeglab(os.path.join(Data_path, subj_files[random.randint(0,16)])) # read raw .set file
            EEG_seg = mne.make_fixed_length_epochs(EEG, duration = t, reject_by_annotation = 'True', overlap = Overlap)
            X       = EEG_seg.compute_psd(**SETTINGS_B)

            fm1.fit(X._freqs, np.squeeze(X._data), [X._freqs[0] , X._freqs[-1]])
            fm2.fit(X._freqs, np.squeeze(X._data), [X._freqs[0] , X._freqs[-1]])

            Slope_nk[i, 0:len(fm1.get_params('aperiodic_params','exponent'))] = fm1.get_params('aperiodic_params','exponent')
            Slope_k[i, 0:len(fm2.get_params('aperiodic_params','exponent'))] = fm2.get_params('aperiodic_params','exponent')

            r2_nk[i, 0:len(fm1.get_params('r_squared'))] = fm1.get_params('r_squared')
            r2_k[i, 0:len(fm1.get_params('r_squared'))] = fm2.get_params('r_squared')

            knee_k[i, 0:len(fm1.get_params('aperiodic_params','knee'))] = fm1.get_params('aperiodic_params','knee')


        else:

            events = mne.read_events(Path(path_stage, stage_files[i])) #read staging markers
            epochs = mne.Epochs(EEG, events=events, tmin=-30, tmax=0)
            i = i+1
            #Frequency transformation welch's method from 1 to 70Hz different time stamps
                #Now we select epochs and average over all epochs
            N1s = epochs['1']
            N2s = epochs['2']
            N3s = epochs['3']
            REs = epochs['5']
            AWs = epochs['0']

            # Settings for PSD calculation using welch's
            N1={}
            N2={}
            N3={}
            AW={}
            RM={}

            N1 = N1s.compute_psd(**SETTINGS_B) #N1
            N2 = N2s.compute_psd(**SETTINGS_B) #N2
            N3 = N3s.compute_psd(**SETTINGS_B)
            AW = AWs.compute_psd(**SETTINGS_B)
            RM = REs.compute_psd(**SETTINGS_B)
