import mne
import numpy as np
import matplotlib.pyplot as plt

# Import the FOOOF object
from fooof import FOOOF

# Import a utility to download and load example data
from fooof.utils.download import load_fooof_data

EEG = mne.read_epochs_eeglab('/home/b1044271/Columbia/Test_dataset.set')
EEG1 = EEG.pick('E257', exclude=[]) # select Cz for further analysis

#Now we select epochs and average over all epochs
N1s = EEG1['stage_1']
N2s = EEG1['stage_2']
N3s = EEG1['stage_3']
REs = EEG1['stage_5']
AWs = EEG1['stage_0']

# set parameters for frq transformation
fs = 250  #sampling freq
SETTINGS_B = { 'method' : 'welch', 'average' : 'mean', 'fmin' :1 , 'fmax' : 70}
Time_segments = [2, 5, 10, 15] #in seconds

# Frequency transformation welch's method from 1 to 70Hz
N1={}
N2={}
N3={}
AW={}
RM={}

i = 0
for x in Time_segments:
    i = i+1
    N1[x] = N1s.compute_psd(**SETTINGS_B, n_fft=fs*x) #N1
    N2[x] = N2s.compute_psd(**SETTINGS_B, n_fft=fs*x) #N2
    N3[x] = N3s.compute_psd(**SETTINGS_B, n_fft=fs*x)
    AW[x] = AWs.compute_psd(**SETTINGS_B, n_fft=fs*x)
    RM[x] = REs.compute_psd(**SETTINGS_B, n_fft=fs*x)

# Now plot to get a feeling
fig, ax = plt.subplots()
ax.plot(TF_Wa._freqs, np.mean(np.squeeze(TF_N1a),0), color = 'black')
ax.plot(TF_Wb._freqs, np.mean(np.squeeze(TF_N1b),0), color = 'blue')
ax.plot(TF_Wc._freqs, np.mean(np.squeeze(TF_N1c),0), color = 'red')
ax.plot(TF_Wd._freqs, np.mean(np.squeeze(TF_N1d),0), color = 'green')
plt.xscale("log")
plt.ylim(0, 0.03e-9)
plt.show()

# model fit on different freq characteristics
SETTINGS_F1={'max_n_peaks':8, 'aperiodic_mode':'fixed'}
SETTINGS_F2={'max_n_peaks':8, 'aperiodic_mode':'knee'}
freq_range = [N1[2]._freqs[0] , N1[2]._freqs[-1]]

fooof_a = {}
fooof_b = {}

i = 0
variables = [N1, N2, N3, AW, RM] # loop over stages
for  A in variables:
    for keys, values in A.items():  # loop over time windows
        fm1 = FOOOF(**SETTINGS_F1)
        fm1.fit(A[keys]._freqs, np.mean(np.squeeze(A[keys]._data),0), freq_range) # fit no knee
        fooof_a[i] = fm1.get_results()

        fm2 = FOOOF(**SETTINGS_F2)
        fm2.fit(A[keys]._freqs, np.mean(np.squeeze(A[keys]._data),0), freq_range) # fit with a knee
        fooof_b[i] = fm2.get_results()
        i=i+1

# CREATE AND EXCEL SHEET WITH ALL model parameters
import xlsxwriter

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('Parametres_index.xlsx')
worksheet = workbook.add_worksheet()

data_cols = ['ID', 'Stage','Time Steps(s)', 'Knee', 'Rsquared', 'Error', 'Offset', 'Exponent', 'Number of Peaks']
header_format = workbook.add_format({
    'bold': False,
    'font_name': 'Arial',
    'font_size': 10,
    'text_wrap': True,
    'center_across': True,
    'valign': 'bottom',
    'fg_color': '#cdffff',
    'border': 1})

for col_num, value in enumerate(data_cols):
    worksheet.write(0, col_num, value, header_format)

i=1
ii = 0
timesteps = ["2","5","10","15"]*5
stages = np.repeat(np.array(["N1", "N2", "N3","R","W"]), 4, axis=0)
for key , value in fooof_a.items():

    worksheet.write(i, 0, 1)
    worksheet.write(i, 3, "N")
    worksheet.write(i, 1, stages[ii])
    worksheet.write(i, 2, timesteps[ii])
    worksheet.write(i, 4, fooof_a[key].r_squared)     # Writes an int
    worksheet.write(i, 5, fooof_a[key].error)
    worksheet.write(i, 6, fooof_a[key].aperiodic_params[0])
    worksheet.write(i, 7, fooof_a[key].aperiodic_params[1])
    worksheet.write(i, 8, len(fooof_a[key].peak_params))
    i=i+1
    ii = ii+1

# KNEE MODEL PARAM
iii = i +1 # continue in the row following the end of the no knee condition
ii = 0 # reset for loops
for key , value in fooof_b.items():

    worksheet.write(iii, 0, 1)
    worksheet.write(iii, 4, "Y")
    worksheet.write(iii, 1, stages[ii])
    worksheet.write(iii, 2, timesteps2[ii])
    worksheet.write(iii, 3, freq_lims[ii])
    worksheet.write(iii, 5, fooof_b[key].r_squared)     # Writes an int
    worksheet.write(iii, 6, fooof_b[key].error)     # Writes an int
    worksheet.write(iii, 7, fooof_b[key].aperiodic_params[0])
    worksheet.write(iii, 8, fooof_b[key].aperiodic_params[2])     # Writes an int
    worksheet.write(iii, 9, len(fooof_b[key].peak_params))     # Writes an int
    iii = iii +1
    ii = ii+1
workbook.close()
