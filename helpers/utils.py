import numpy as np
import os
import pandas as pd
from pathlib import Path
import glob

###################################################################################################
###################################################################################################

def resample_stages(path, req_samp_rate)

    path_stage = path
    stage_files = glob.glob(path_stage)
    #set required time resolution - stages are in 30 seconds so the conversion depends on the time resolution specified
    fs-actual = 30
    fs_req = req_samp_rate

    for file in stage_files:
        files  = pd.read_csv(file)
        stages = list(Stage.iloc[:,0])
        stages_new = [val for val in stages for _ in range(0, 30)]