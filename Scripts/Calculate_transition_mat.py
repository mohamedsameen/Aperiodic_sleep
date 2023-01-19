from fooof.utils.download import load_fooof_data
from math import floor
import mne
import numpy as np
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from spiketools.plts.utils import make_axes
import seaborn as sns
import imagesc as imagesc
import glob

# get all stages files
path_stage = '/home/b1044271/EEGsleep/SleepStaging/*.txt'
stage_files = glob.glob(path_stage)

Trns_mat = np.ones([17,25])

i = 0
for file in stage_files:

    files  = pd.read_csv(file)
    stages = list(files.iloc[:,0])

    # Go through the staging files and get the index of all the stags then find the next stage

    N1_o = [i for i in range(len(stages)) if stages[i] == 1]
    N1_l = np.array(stages)[np.array([i + 1 for i in N1_o[0:-2]])]

    N2_o = [i for i in range(len(stages)) if stages[i] == 2]
    N2_l = np.array(stages)[np.array([i + 1 for i in N2_o[0:-2]])]

    N3_o = [i for i in range(len(stages)) if stages[i] == 3]
    N3_l = np.array(stages)[np.array([i + 1 for i in N3_o[0:-2]])]

    R_o = [i for i in range(len(stages)) if stages[i] == 5]
    R_l = np.array(stages)[np.array([i + 1 for i in R_o[0:-2]])]

    W_o = [i for i in range(len(stages)) if stages[i] == 0]
    W_l = np.array(stages)[np.array([i + 1 for i in W_o[0:-2]])]

    # Go through the epochs and get the transitions
    R_trans  = np.ones([5,350]) * np.nan
    N1_trans = np.ones([5,350]) * np.nan
    N2_trans = np.ones([5,350]) * np.nan
    N3_trans = np.ones([5,350]) * np.nan
    W_trans  = np.ones([5,350]) * np.nan

    X = [1,2,3,5,0]

ii=0
for S in X:
    N1_trans[ii,0:len([i for i in range(len(N1_l)) if N1_l[i] == S])] = [i for i in range(len(N1_l)) if N1_l[i] == S]
    N2_trans[ii,0:len([i for i in range(len(N2_l)) if N2_l[i] == S])] = [i for i in range(len(N2_l)) if N2_l[i] == S]
    N3_trans[ii,0:len([i for i in range(len(N3_l)) if N3_l[i] == S])] = [i for i in range(len(N3_l)) if N3_l[i] == S]
    R_trans[ii,0:len([i for i in range(len(R_l)) if R_l[i] == S])] = [i for i in range(len(R_l)) if R_l[i] == S]
    W_trans[ii,0:len([i for i in range(len(W_l)) if W_l[i] == S])] = [i for i in range(len(W_l)) if W_l[i] == S]

    ii=ii+1

N1_t = [np.sum(~np.isnan(N1_trans[4])), np.sum(~np.isnan(N1_trans[3])),np.sum(~np.isnan(N1_trans[0])),
            np.sum(~np.isnan(N1_trans[1])),np.sum(~np.isnan(N1_trans[2]))]

N2_t = [np.sum(~np.isnan(N2_trans[4])), np.sum(~np.isnan(N2_trans[3])),np.sum(~np.isnan(N2_trans[0])),
            np.sum(~np.isnan(N2_trans[1])),np.sum(~np.isnan(N2_trans[2]))]

N3_t = [np.sum(~np.isnan(N3_trans[4])), np.sum(~np.isnan(N3_trans[3])),np.sum(~np.isnan(N3_trans[0])),
            np.sum(~np.isnan(N3_trans[1])),np.sum(~np.isnan(N3_trans[2]))]

R_t = [np.sum(~np.isnan(R_trans[4])), np.sum(~np.isnan(R_trans[3])),np.sum(~np.isnan(R_trans[0])),
            np.sum(~np.isnan(R_trans[1])),np.sum(~np.isnan(R_trans[2]))]

W_t = [np.sum(~np.isnan(W_trans[4])), np.sum(~np.isnan(W_trans[3])),np.sum(~np.isnan(W_trans[0])),
            np.sum(~np.isnan(W_trans[1])),np.sum(~np.isnan(W_trans[2]))]


Trns_mat[i,:] = np.concatenate((W_t,R_t,N1_t,N2_t,N3_t),axis=0)
i=i+1
