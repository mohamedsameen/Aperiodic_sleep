# Import measure related functions
from spiketools.measures.spikes import (compute_firing_rate, compute_isis,
                                        compute_cv, compute_fano_factor)
from spiketools.measures.conversions import (convert_times_to_train, convert_train_to_times,
                                             convert_isis_to_times)
from spiketools.measures.trials import (compute_trial_frs, compute_pre_post_rates,
                                        compute_segment_frs, compute_pre_post_averages,
                                        compute_pre_post_diffs)

from spiketools.plts.data import plot_lines
# Import simulation functions
from spiketools.sim import sim_spiketimes
# Import plot functions
from spiketools.plts.spikes import plot_isis
from spiketools.plts.trials import plot_rasters
from fooof.plts import plot_spectra
import mne
import numpy as np
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from spiketools.plts.utils import make_axes
import warnings
warnings.filterwarnings("ignore")

# folder of the results
path_files = Path('/home/b1044271/Columbia/Results/PSDs/')

# Get names of all subject folder
sbj_folders = list(path_files.iterdir())
sbj_folders = sorted(sbj_folders)


# PLotting the psds for all conditions per subjects
axes = make_axes(20, 5, figsize=(15, 20))
psd_files = os.listdir(path_files / subj / 'N1')
assert len(axes) == len(psd_files), 'The number of files is wrong!'
for psd, ax in zip(psd_files, axes):
    print(psd)
    N1_psd = np.load(path_files / subj / 'N1' / psd)
    N2_psd = np.load(path_files / subj / 'N2' / psd)

    plot_spectra(np.arange(0, N1_psd.shape[1],1),
                 [np.mean(N1_psd,0),np.mean(N2_psd,0),np.mean(N3_psd,0),np.mean(AW_psd,0),np.mean(RM_psd,0)],
                 log_powers=True, ax=ax)

## TOM's method
F_PARAMS = ['F30', 'F45', 'F55', 'F70', 'F100']
T_PARAMS = ['T2', 'T5', 'T10', 'T15']

axes = iter(make_axes(20, 5, figsize=(15, 20)))
for subj in sbj_folders[6:7]:

    for CUR_T_PARAM in T_PARAMS:
        for CUR_F_PARAM in F_PARAMS:
            N1_psd = np.load(path_files / subj / 'N1' / (CUR_T_PARAM + '_' + CUR_F_PARAM + '.npy'))
            N2_psd = np.load(path_files / subj /'N2' / (CUR_T_PARAM + '_' + CUR_F_PARAM + '.npy'))
            N3_psd = np.load(path_files / subj /'N3' / (CUR_T_PARAM + '_' + CUR_F_PARAM + '.npy'))
            AW_psd = np.load(path_files / subj /'AW' / (CUR_T_PARAM + '_' + CUR_F_PARAM + '.npy'))
            RM_psd = np.load(path_files / subj /'RM' / (CUR_T_PARAM + '_' + CUR_F_PARAM + '.npy'))
            plot_spectra(np.arange(0, N1_psd.shape[1],1),
                         [np.mean(N1_psd,0),np.mean(N2_psd,0),np.mean(N3_psd,0),
                          np.mean(AW_psd,0),np.mean(RM_psd,0)],
                         log_freqs=True, log_powers=True, ax=next(axes))
