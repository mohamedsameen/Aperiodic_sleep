import mne
import numpy as np
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from spiketools.plts.utils import make_axes
import glob

def stage_samp_adj(path, extension, required_sampling_rate):
    # GET stages
    path_stage = path + '*.' + extension
    stage_files = glob.glob(path_stage)

    #set required time resolution
    #stages are in 30 seconds so the conversion depends on the time resolution specified
    fs_actual = 30
    fs_eq = fs_actual / required_sampling_rate

    for file in stage_files:
    files  = pd.read_csv(file)
    stages = list(files.iloc[:,0])
    Stages_new = [val for val in stages for _ in range(0, floor(fs_eq))]
    i = i+1
