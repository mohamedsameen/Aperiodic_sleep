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
SETTINGS_B = { 'method' : 'welch', 'median' : 'mean', 'fmin' :0.1 }
path_results = Path('/home/b1044271/Columbia/Results/PSDs/New_freq_Res')
path_frqs = Path('/home/b1044271/Columbia/Results/PSDs/Freqs')

Time_segments = [2, 5, 10, 15,20] #in seconds
f_max = [30, 45 , 55, 70, 100]
electrode = 'E257'
# Helper function for paths
def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

check_path(path_results / electrode)

i = 0
for x in subj_files:

  check_path(path_results / electrode / x[0:4]) # create subject folder
  EEG = mne.io.read_raw_eeglab(os.path.join(Data_path, x)) # read raw .set file
  print('loaded')
  EEG1 = EEG.pick(electrode, exclude=[]) # select Cz for further analysis
  events = mne.read_events(Path(path_stage, stage_files[i])) #read staging markers
  epochs = mne.Epochs(EEG, events=events, tmin=-30, tmax=0)
  i = i+1
# Frequency transformation welch's method from 1 to 70Hz different time stamps
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

  for t in Time_segments:
      for f in f_max:
          N1 = N1s.compute_psd(**SETTINGS_B, fmax=f, n_fft=fs*t) #N1
          N2 = N2s.compute_psd(**SETTINGS_B, fmax=f, n_fft=fs*t) #N2
          N3 = N3s.compute_psd(**SETTINGS_B, fmax=f, n_fft=fs*t)
          AW = AWs.compute_psd(**SETTINGS_B, fmax=f, n_fft=fs*t)
          RM = REs.compute_psd(**SETTINGS_B, fmax=f, n_fft=fs*t)

          check_path(path_results /electrode/ x[0:4] / 'N1')
          check_path(path_results /electrode/ x[0:4] / 'N2')
          check_path(path_results /electrode/ x[0:4] / 'N3')
          check_path(path_results /electrode/ x[0:4] / 'AW')
          check_path(path_results /electrode/ x[0:4] / 'RM')

          names = ['T' ,str(t), '_F' , str(f), '.npy']
          Freq_res = ['T' ,str(t),'F' , str(f), '_freqres.npy']


          np.save(Path(path_results /electrode/ x[0:4] / 'N1'/ ''.join(names)),np.squeeze(N1._data))
          np.save(Path(path_results /electrode/ x[0:4] / 'N2'/ ''.join(names)),np.squeeze(N2._data))
          np.save(Path(path_results /electrode/ x[0:4] / 'N3'/ ''.join(names)),np.squeeze(N3._data))
          np.save(Path(path_results /electrode/ x[0:4] / 'AW'/ ''.join(names)),np.squeeze(AW._data))
          np.save(Path(path_results /electrode/ x[0:4] / 'RM'/ ''.join(names)),np.squeeze(RM._data))

          np.save(Path(path_frqs / ''.join(Freq_res)),RM._freqs)
