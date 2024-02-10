# Overview

The investigation of aperiodic activity in electrophysiological signals is trending. Previous work showed that the aperiodic exponent cna differentiate between stages.
In this project, we used recent methods for parametrizing neural power spectra  (Donoghue et al., 2020) in iEEG and EEG sleep recordings to investigate the temporal dynamics of aperiodic activity during sleep.

This project is a collaboration between the Sleep Lab (_Mohamed S. Ameen_) at the University of Salzburg, Austria and Jacob's Lab (_Thomas Donoghue_) at Columbia University in NYC, USA


## Reference

The preprint for this project:

Ameen, M. S., Jacobs, J., Schabus, M., Hoedlmoser, K., & Donoghue, T. (2024). The Temporal Dynamics of Aperiodic Neural Activity Track 
Changes in Sleep Architecture (p. 2024.01.25.577204). bioRxiv. https://doi.org/10.1101/2024.01.25.577204


# Project Guide

In this project we used both Python (v3.7) and MATLAB (v2019a). Matlab scripts are basically preprocessing scripts. 
From the preprocessing of full night EEG files to the epoching of the data into trials of different conditions and calculating ERPs. 
We also used Fieldtrip toolbox in MATLAB for cluster based permutation statistics.

In Python we have scripts and Notebooks. Python scripts are mainly to run FOOOF over full night EEG datasets. 
Python Notebooks contain the codes for running FOOOF as well as the statistical analyses on the resulting FOOOF parameters.


## Requirements

This repo requires Python >= 3.7 to run.

Dependency Python packages:
- [numpy](https://github.com/numpy/numpy)
- [pandas](https://github.com/pandas-dev/pandas)
- [scipy](https://github.com/scipy/scipy)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [seaborn](https://github.com/mwaskom/seaborn)

- [mne](https://github.com/mne-tools/mne-python)
- [fooof](https://fooof-tools.github.io/fooof/index.html) >= 1.0.0 
- [lisc](https://github.com/lisc-tools/lisc/tree/main/tutorials)  >= 0.2.0 

