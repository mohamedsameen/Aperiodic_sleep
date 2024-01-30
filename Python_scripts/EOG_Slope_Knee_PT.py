#Here we will Look at EOG data and see the PSDs and slopes
import os
from pathlib import Path
import numpy as np
import mne
import pandas as pd
import glob

# Use neurodsp for convenience
from neurodsp.plts import plot_time_series, plot_power_spectra
from neurodsp.spectral import compute_spectrum

# Import fooof for checking model fits
from fooof import FOOOF
from fooof import FOOOFGroup

# KNEE freqs
from fooof.utils.params import compute_knee_frequency
from fooof.utils.download import load_fooof_data

# Plotting functions
from spiketools.plts.utils import make_axes
import matplotlib.pyplot as plt
import seaborn

# Import custom project code
import sys
sys.path.append("/home/b1044271/Columbia/Aperiodic_sleep/helpers")
from utils import check_distribution, perform_correlation, check_path

#####################################################################
# get the files for the no K-complex
Data_path = '/home/b1044271/FSON_REM/EOG_data/*Phasic.set'
Phasic_files = np.sort(glob.glob(Data_path))

Data_path = '/home/b1044271/FSON_REM/EOG_data/*Tonic.set'
Tonic_files = np.sort(glob.glob(Data_path))

result_path = Path('/home/b1044271/Columbia/Results/Phasic_Tonic/')
check_path(result_path)
results_path = '/home/b1044271/Columbia/Results/Phasic_Tonic/'

count = [1,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19] # participant number (for saving) 
####################################################################
#Setting parameters
# Settings for the analyses

f_min = 1
f_max = 45
t     = 1
fs    = 250

SETTINGS_W  = { 'method' : 'welch', 'average' : 'mean', 'fmin' :f_min , 'fmax':f_max, 'n_fft': fs*t, 'n_overlap': fs*t*0.5}
SETTINGS_F1 = {'max_n_peaks':8, 'aperiodic_mode':'knee'}
SETTINGS_F2 = {'max_n_peaks':8, 'aperiodic_mode':'fixed'}

#####################################################################
#Empty vectors for storing data
T_Kn  = np.zeros([17,2000])*np.nan
T_Exp = np.zeros([17,2000])*np.nan
T_Exp2 = np.zeros([17,2000])*np.nan
T_R2k = np.zeros([17,2000])*np.nan
T_R2nk = np.zeros([17,2000])*np.nan

P_Kn  = np.zeros([17,2000])*np.nan
P_Exp = np.zeros([17,2000])*np.nan
P_Exp2 = np.zeros([17,2000])*np.nan
P_R2k = np.zeros([17,2000])*np.nan
P_R2nk = np.zeros([17,2000])*np.nan

#########################################################################
#START Looping over subjects
# Helper function for paths, check for the path and creates ones if not found

# Start function
i = 0
for x in np.arange(17):

    EEG_P = mne.io.read_epochs_eeglab(Phasic_files[x]) # read raw .set file
    EEG_T = mne.io.read_epochs_eeglab(Tonic_files[x]) # read raw .set file

# calculate psd based on welch's method with differen freq range and diff time steps
    P = EEG_P.compute_psd(**SETTINGS_W) #N1
    T = EEG_T.compute_psd(**SETTINGS_W) #N2
    
    # put the PSD data in an array
    Px = P._data
    Tx = T._data
		
    # Equalise the number of epcochs
    X = min(len(Px), len(Tx))

    P1 = Px[np.random.choice(Px.shape[0], X, replace=False), :]
    T1 = Tx[np.random.choice(Tx.shape[0], X, replace=False), :]

    P2 = np.squeeze(np.mean(P1,axis=1))
    T2 = np.squeeze(np.mean(T1,axis=1))

    namesP = ['VP' ,str(count[x]), '_P_PSD.npy']
    namesT = ['VP' ,str(count[x]), '_T_PSD.npy']

    np.save(results_path + ''.join(namesP),P2)
    np.save(results_path + ''.join(namesT),T2)

# FOOOF it
    fm1 = FOOOFGroup(**SETTINGS_F1)
    fm1.fit(P._freqs, P2, [P._freqs[0] ,P._freqs[-1]])

    fm2 = FOOOFGroup(**SETTINGS_F1)
    fm2.fit(T._freqs, T2, [T._freqs[0] ,T._freqs[-1]])

    fm3 = FOOOFGroup(**SETTINGS_F2)
    fm3.fit(P._freqs, P2, [P._freqs[0] ,P._freqs[-1]])

    fm4 = FOOOFGroup(**SETTINGS_F2)
    fm4.fit(T._freqs, T2, [T._freqs[0] ,T._freqs[-1]])

# parameters exctraction
    T_Kn[i,0:len(T1)]   = fm2.get_params('aperiodic_params','knee')
    T_Exp[i,0:len(T1)]  = fm2.get_params('aperiodic_params','exponent')
    T_Exp2[i,0:len(T1)] = fm4.get_params('aperiodic_params','exponent')
    T_R2k[i,0:len(T1)]  = fm2.get_params('r_squared')
    T_R2nk[i,0:len(T1)] = fm4.get_params('r_squared')

    P_Kn[i,0:len(P1)]   = fm1.get_params('aperiodic_params','knee')
    P_Exp[i,0:len(P1)]  = fm1.get_params('aperiodic_params','exponent')
    P_Exp2[i,0:len(P1)] = fm3.get_params('aperiodic_params','exponent')
    P_R2k[i,0:len(P1)]  = fm1.get_params('r_squared')
    P_R2nk[i,0:len(P1)] = fm3.get_params('r_squared')

    i = i+1
#################################################################################
#KNEE FREQ CALC
# Compute knee frequency
Kn_P = compute_knee_frequency(P_Kn, P_Exp)
Kn_T = compute_knee_frequency(T_Kn, T_Exp)

# SAVING
np.save('/home/b1044271/Columbia/Results/Phasic_Tonic/Freqs_vector.npy',T._freqs)

np.save(Path(result_path /'Kn_t15_F45_P.npy'),Kn_P)
np.save(Path(result_path /'Kn_t15_F45_T.npy'),Kn_T)

np.save(Path(result_path /'Exp_wKnee_t15_F45_T.npy'),T_Exp)
np.save(Path(result_path /'Exp_wKnee_t15_F45_P.npy'),P_Exp)

np.save(Path(result_path /'Exp_nKnee_t15_F45_T.npy'),T_Exp2)
np.save(Path(result_path /'Exp_nKnee_t15_F45_P.npy'),P_Exp2)

np.save(Path(result_path /'R2_Knee_t15_F45_T.npy'),T_R2k)
np.save(Path(result_path /'R2_Knee_t15_F45_P.npy'),P_R2k)

np.save(Path(result_path /'R2_nKnee_t15_F45_T.npy'),T_R2nk)
np.save(Path(result_path /'R2_nKnee_t15_F45_P.npy'),P_R2nk)
