#This scripts fits different aperiodic models (Knee M, Fixed M) to the EEG data. It produces a Expoennt and Knee Frequency metrics 
#######################################################
import os
from pathlib import Path
import numpy as np
import mne
import pandas as pd

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

#####################################################################
#GET PATHS
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

###############################################################################
#Setting parameters
# Settings for the analyses

f_min = 1
f_max = 45
t     = 15
fs    = 250

SETTINGS_W  = { 'method' : 'welch', 'average' : 'mean', 'fmin' :f_min , 'fmax':f_max, 'n_fft': fs*t, 'n_overlap': fs*t*0.5}
SETTINGS_F1 = {'max_n_peaks':8, 'aperiodic_mode':'knee'}
SETTINGS_F2 = {'max_n_peaks':8, 'aperiodic_mode':'fixed'}

#####################################################################
#Empty vectors for storing data

W_Kn  = np.zeros([17,2000])*np.nan
W_Exp = np.zeros([17,2000])*np.nan
W_Exp2 = np.zeros([17,2000])*np.nan
W_R2k = np.zeros([17,2000])*np.nan
W_R2nk = np.zeros([17,2000])*np.nan
W_E2k = np.zeros([17,2000])*np.nan
W_E2nk = np.zeros([17,2000])*np.nan


N1_Kn  = np.zeros([17,2000])*np.nan
N1_Exp = np.zeros([17,2000])*np.nan
N1_Exp2 = np.zeros([17,2000])*np.nan
N1_R2k = np.zeros([17,2000])*np.nan
N1_R2nk = np.zeros([17,2000])*np.nan
N1_E2k = np.zeros([17,2000])*np.nan
N1_E2nk = np.zeros([17,2000])*np.nan


N2_Kn  = np.zeros([17,2000])*np.nan
N2_Exp = np.zeros([17,2000])*np.nan
N2_Exp2 = np.zeros([17,2000])*np.nan
N2_R2k = np.zeros([17,2000])*np.nan
N2_R2nk = np.zeros([17,2000])*np.nan
N2_E2k = np.zeros([17,2000])*np.nan
N2_E2nk = np.zeros([17,2000])*np.nan


N3_Kn  = np.zeros([17,2000])*np.nan
N3_Exp = np.zeros([17,2000])*np.nan
N3_Exp2 = np.zeros([17,2000])*np.nan
N3_R2k = np.zeros([17,2000])*np.nan
N3_R2nk = np.zeros([17,2000])*np.nan
N3_E2k = np.zeros([17,2000])*np.nan
N3_E2nk = np.zeros([17,2000])*np.nan


R_Kn  = np.zeros([17,2000])*np.nan
R_Exp = np.zeros([17,2000])*np.nan
R_Exp2 = np.zeros([17,2000])*np.nan
R_R2k = np.zeros([17,2000])*np.nan
R_R2nk = np.zeros([17,2000])*np.nan
R_E2k = np.zeros([17,2000])*np.nan
R_E2nk = np.zeros([17,2000])*np.nan

#########################################################################
#START Looping over subjects
# Helper function for paths, check for the path and creates ones if not found
def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


# Start function
i = 0
for x in subj_files:
    EEG = mne.io.read_raw_eeglab(os.path.join(Data_path, x)) # read raw .set file
    print('loaded')

    events = mne.read_events(Path(path_stage, stage_files[i])) #read staging markers
    epochs = mne.Epochs(EEG, events=events, tmin=-30, tmax=0)

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

# calculate psd based on welch's method with differen freq range and diff time steps
    N1 = N1s.compute_psd(**SETTINGS_W) #N1
    N2 = N2s.compute_psd(**SETTINGS_W) #N2
    N3 = N3s.compute_psd(**SETTINGS_W)
    AW = AWs.compute_psd(**SETTINGS_W)
    RM = REs.compute_psd(**SETTINGS_W)

# FOOOF it
    fm1 = FOOOFGroup(**SETTINGS_F1)
    fm1.fit(N1._freqs, np.mean(N1._data,0), [N1._freqs[0] ,N1._freqs[-1]])

    fm2 = FOOOFGroup(**SETTINGS_F1)
    fm2.fit(N2._freqs, np.mean(N2._data,0), [N2._freqs[0] ,N2._freqs[-1]])

    fm3 = FOOOFGroup(**SETTINGS_F1)
    fm3.fit(N3._freqs, np.mean(N3._data,0), [N3._freqs[0] ,N3._freqs[-1]])

    fm4 = FOOOFGroup(**SETTINGS_F1)
    fm4.fit(RM._freqs, np.mean(RM._data,0), [RM._freqs[0] ,RM._freqs[-1]])

    fm5 = FOOOFGroup(**SETTINGS_F1)
    fm5.fit(AW._freqs, np.mean(AW._data,0), [AW._freqs[0] ,AW._freqs[-1]])

    fm6 = FOOOFGroup(**SETTINGS_F2)
    fm6.fit(N1._freqs, np.mean(N1._data,0), [N1._freqs[0] ,N1._freqs[-1]])

    fm7 = FOOOFGroup(**SETTINGS_F2)
    fm7.fit(N2._freqs, np.mean(N2._data,0), [N2._freqs[0] ,N2._freqs[-1]])

    fm8 = FOOOFGroup(**SETTINGS_F2)
    fm8.fit(N3._freqs, np.mean(N3._data,0), [N3._freqs[0] ,N3._freqs[-1]])

    fm9 = FOOOFGroup(**SETTINGS_F2)
    fm9.fit(RM._freqs, np.mean(RM._data,0), [RM._freqs[0] ,RM._freqs[-1]])

    fm10 = FOOOFGroup(**SETTINGS_F2)
    fm10.fit(AW._freqs, np.mean(AW._data,0), [AW._freqs[0] ,AW._freqs[-1]])

# parameters exctraction
    W_Kn[i,0:AW._data.shape[1]]  = fm5.get_params('aperiodic_params','knee')
    W_Exp[i,0:AW._data.shape[1]] = fm5.get_params('aperiodic_params','exponent')
    W_Exp2[i,0:AW._data.shape[1]] = fm10.get_params('aperiodic_params','exponent')

    W_R2k[i,0:AW._data.shape[1]] = fm5.get_params('r_squared')
    W_R2nk[i,0:AW._data.shape[1]] = fm10.get_params('r_squared')
    W_E2k[i,0:AW._data.shape[1]] = fm5.get_params('error')
    W_E2nk[i,0:AW._data.shape[1]] = fm10.get_params('error')



    R_Kn[i,0:RM._data.shape[1]]  = fm4.get_params('aperiodic_params','knee')
    R_Exp[i,0:RM._data.shape[1]] = fm4.get_params('aperiodic_params','exponent')
    R_Exp2[i,0:RM._data.shape[1]] = fm9.get_params('aperiodic_params','exponent')

    R_R2k[i,0:RM._data.shape[1]] = fm4.get_params('r_squared')
    R_R2nk[i,0:RM._data.shape[1]] = fm9.get_params('r_squared')
    R_E2k[i,0:RM._data.shape[1]] = fm4.get_params('error')
    R_E2nk[i,0:RM._data.shape[1]] = fm9.get_params('error')


    N1_Kn[i,0:N1._data.shape[1]]  = fm1.get_params('aperiodic_params','knee')
    N1_Exp[i,0:N1._data.shape[1]] = fm1.get_params('aperiodic_params','exponent')
    N1_Exp2[i,0:N1._data.shape[1]] = fm6.get_params('aperiodic_params','exponent')

    N1_R2k[i,0:N1._data.shape[1]] = fm1.get_params('r_squared')
    N1_R2nk[i,0:N1._data.shape[1]] = fm6.get_params('r_squared')
    N1_E2k[i,0:N1._data.shape[1]] = fm1.get_params('error')
    N1_E2nk[i,0:N1._data.shape[1]] = fm6.get_params('error')


    N2_Kn[i,0:N2._data.shape[1]]  = fm2.get_params('aperiodic_params','knee')
    N2_Exp[i,0:N2._data.shape[1]] = fm2.get_params('aperiodic_params','exponent')
    N2_Exp2[i,0:RM._data.shape[1]] = fm7.get_params('aperiodic_params','exponent')

    N2_R2k[i,0:AW._data.shape[1]] = fm2.get_params('r_squared')
    N2_R2nk[i,0:AW._data.shape[1]] = fm7.get_params('r_squared')
    N2_E2k[i,0:AW._data.shape[1]] = fm2.get_params('error')
    N2_E2nk[i,0:AW._data.shape[1]] = fm7.get_params('error')


    N3_Kn[i,0:N3._data.shape[1]]  = fm3.get_params('aperiodic_params','knee')
    N3_Exp[i,0:N3._data.shape[1]] = fm3.get_params('aperiodic_params','exponent')
    N3_Exp2[i,0:N3._data.shape[1]] = fm8.get_params('aperiodic_params','exponent')

    N3_R2k[i,0:AW._data.shape[1]] = fm3.get_params('r_squared')
    N3_R2nk[i,0:AW._data.shape[1]] = fm8.get_params('r_squared')
    N3_E2k[i,0:AW._data.shape[1]] = fm3.get_params('error')
    N3_E2nk[i,0:AW._data.shape[1]] = fm8.get_params('error')


    i = i+1

#################################################################################
#KNEE FREQ CALC
# Compute knee frequency
Kn_W = compute_knee_frequency(W_Kn, W_Exp)
Kn_N1 = compute_knee_frequency(N1_Kn, N2_Exp)
Kn_N2 = compute_knee_frequency(N2_Kn, N2_Exp)
Kn_N3 = compute_knee_frequency(N3_Kn, N3_Exp)
Kn_R = compute_knee_frequency(R_Kn, R_Exp)


# SAVING

result_path = Path('/home/b1044271/Columbia/Results/Slope_Knee_over_stages/')
check_path(result_path)

np.save(Path(result_path /'Kn_t15_F45_W.npy'),Kn_W)
np.save(Path(result_path /'Kn_t15_F45_N1.npy'),Kn_N1)
np.save(Path(result_path /'Kn_t15_F45_N2.npy'),Kn_N2)
np.save(Path(result_path /'Kn_t15_F45_N3.npy'),Kn_N3)
np.save(Path(result_path /'Kn_t15_F45_R.npy'),Kn_R)

np.save(Path(result_path /'Exp_wKnee_t15_F45_W.npy'),W_Exp)
np.save(Path(result_path /'Exp_wKnee_t15_F45_N1.npy'),N1_Exp)
np.save(Path(result_path /'Exp_wKnee_t15_F45_N2.npy'),N2_Exp)
np.save(Path(result_path /'Exp_wKnee_t15_F45_N3.npy'),N3_Exp)
np.save(Path(result_path /'Exp_wKnee_t15_F45_R.npy'),R_Exp)

np.save(Path(result_path /'Exp_nKnee_t15_F45_W.npy'),W_Exp2)
np.save(Path(result_path /'Exp_nKnee_t15_F45_N1.npy'),N1_Exp2)
np.save(Path(result_path /'Exp_nKnee_t15_F45_N2.npy'),N2_Exp2)
np.save(Path(result_path /'Exp_nKnee_t15_F45_N3.npy'),N3_Exp2)
np.save(Path(result_path /'Exp_nKnee_t15_F45_R.npy'),R_Exp2)

np.save(Path(result_path /'R2_Knee_t15_F45_W.npy'),W_R2k)
np.save(Path(result_path /'R2_Knee_t15_F45_N1.npy'),N1_R2k)
np.save(Path(result_path /'R2_Knee_t15_F45_N2.npy'),N2_R2k)
np.save(Path(result_path /'R2_Knee_t15_F45_N3.npy'),N3_R2k)
np.save(Path(result_path /'R2_Knee_t15_F45_R.npy'),R_R2k)

np.save(Path(result_path /'R2_nKnee_t15_F45_W.npy'),W_R2nk)
np.save(Path(result_path /'R2_nKnee_t15_F45_N1.npy'),N1_R2nk)
np.save(Path(result_path /'R2_nKnee_t15_F45_N2.npy'),N2_R2nk)
np.save(Path(result_path /'R2_nKnee_t15_F45_N3.npy'),N3_R2nk)
np.save(Path(result_path /'R2_nKnee_t15_F45_R.npy'),R_R2nk)

np.save(Path(result_path /'E_Knee_t15_F45_W.npy'),W_E2k)
np.save(Path(result_path /'E_Knee_t15_F45_N1.npy'),N1_E2k)
np.save(Path(result_path /'E_Knee_t15_F45_N2.npy'),N2_E2k)
np.save(Path(result_path /'E_Knee_t15_F45_N3.npy'),N3_E2k)
np.save(Path(result_path /'E_Knee_t15_F45_R.npy'),R_E2k)

np.save(Path(result_path /'E_nKnee_t15_F45_W.npy'),W_E2nk)
np.save(Path(result_path /'E_nKnee_t15_F45_N1.npy'),N1_E2nk)
np.save(Path(result_path /'E_nKnee_t15_F45_N2.npy'),N2_E2nk)
np.save(Path(result_path /'E_nKnee_t15_F45_N3.npy'),N3_E2nk)
np.save(Path(result_path /'E_nKnee_t15_F45_R.npy'),R_E2nk)


# PLOTTING

#array_list2 = [np.nanmean(Kn_W,1),np.nanmean(Kn_N1,1), np.nanmean(Kn_N2,1), np.nanmean(Kn_N3,1), np.nanmean(Kn_R,1)]
#array_list3 = [np.nanmean(W_Exp,1), np.nanmean(N1_Exp,1), np.nanmean(N2_Exp,1), np.nanmean(N3_Exp,1), np.nanmean(R_Exp,1)]
#array_list4 = [np.nanmean(W_Exp2,1), np.nanmean(N1_Exp2,1), np.nanmean(N2_Exp2,1), np.nanmean(N3_Exp2,1), np.nanmean(R_Exp2,1)]

#titles =  ['W','N1', 'N2','N3','R']

#fig = plt.figure(figsize=(15, 7))

#ax = fig.add_subplot(1, 3, 1)

#ax = seaborn.swarmplot(data=array_list2)
#ax.set( ylabel='Knee frequency (Hz)')
#ax.set_xticklabels(titles)
#seaborn.scatterplot(x=[0,1,2,3,4], y=np.nanmean(array_list2,1), marker='X', color='black', s=100, zorder=4, legend=False)

#ax = fig.add_subplot(1, 3, 2)
#ax = seaborn.swarmplot(data=array_list3)
#ax.set( ylabel='Exponent - Knee')
#ax.set_xticklabels(titles)
#seaborn.scatterplot(x=[0,1,2,3,4], y=np.nanmean(array_list3,1), marker='X', color='black', s=100, zorder=4, legend=False)

#ax = fig.add_subplot(1, 3, 3)
#ax = seaborn.swarmplot(data=array_list4)
#ax.set( ylabel='Exponent - No Knee')
#ax.set_xticklabels(titles)
#seaborn.scatterplot(x=[0,1,2,3,4], y=np.nanmean(array_list4,1), marker='X', color='black', s=100, zorder=4, legend=False)

