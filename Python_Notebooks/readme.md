This respository contains the python notebooks that are used for the analzsis in the aperiodic sleep paper 

The notebooks use toolboxes that are specificed in the dependencies, but also some custom made funtions for statistical testings anf plotting that are found in the helper folder in the utils.py and plots.py

The folder is organized as follows:

# 1. Introduction

## 01_Literature search:
Performs a search in the literature using the lisc toolbox. It first looks for any mention of aperiodic activity in brain and sleep literature then looks for specific mentions of the Exponent to identify teh frequncy ranges used for its estimation.

## 02_Models_Simulations:
Simulates an electrophysiological signal and fits the differnt models to it, then compares the parameters of the different models.

# 2. iEEG analysis

## 03_iEEG_Sensitivity_matrix:
Using different frequency ranges and different time steps to fit the knee and the fixed exponent models to the iEEG and compare the resulting parameters.

## 04_iEEG_fit_specparam:
Fit aperiodic models (Knee and Fixed) to the different sleep stages of the iEEG data.

## 05_iEEG_PSDs
Computes PSDs of the different sleep stages of the iEEG data (Average PSD, Region PSD, Stage PSD)

## 06_iEEG_Compare_stages:
Compare the different aperiodic model parameters (Exponent, Knee freq, R2) of the sleep stages between the knee and the fixed models.

## 07_iEEG_decoding:
Uses an LDA classifier to differentiate between sleep stages using Knee Frequency, exponent of the knee model, and exponent of the fixed model, compares the results, then uses a Random Forest approach to identify the parameter that yields the best performance.

## 08_iEEG_model_comparison:
Performs model comparison between the Knee Model and the Fixed Model fit to the iEEG via the byesian infomration criterion (BIC)for gaussian distributions. 

# 3. EEG analysis

## 09_EEG_fit_specparam:
Fits aperiodic models (Knee and Fixed) to the different sleep stages of the EEG data.

## 10_EEG_PSDs
Computes PSDs of the different sleep stages of the EEG data (Average PSD, Region PSD, Stage PSD).

## 11_EEG_Compare_stages:
Compares the different aperiodic model parameters (Exponent, Knee freq, R2) of the sleep stages between the knee and the fixed models.

## 12_EEG_topoplots:
Plots the topographical maps of the spatial distribution of the Knee Freuency and the exponent metric in the EEG data.

## 13_EEG_decoding:
Uses an LDA classifier to differentiate between sleep stages using Knee Frequency, exponent of the knee model and exponent of the fixed model as well as the exponent of the simple model (fit between 30-45Hz - commonly used range in sleep research).

## 14_EEG_model_comparison:
Compares between the performance of the different models fit to the EEG using BIC.

# 4. Time-resolved analysis in full night continous EEG data

## 15_EEG_WholeNight_SingleSubj:
Plots the time-frequency representation, the hypnogram, as well as the exponent over the whole night in one subject from the EEG data (for estimation script see: Python_scripts/Exp_TF_SingleSubj)

## 16_EEG_epochXepoch
Calculates the aperiodic parameters for each stage across the whole night on an epoch-by-epoch (30 seconds) basis, then calculates the aperiodic parameters for each quartile of the night, for all stages.

## 17_EEG_transitions
Uses the different sleep parameters estimated continously over the whole night (see Python_scripts/Moving_avergae_all_subj_all_night) to detect transitions between sleep stages

## 18_EEG_ERPplots
Plots auditory ERPs using ERP calculations (see Matlab_scripts no: 2,3,4 & 5)








