import numpy as np
import os
import pandas as pd
from pathlib import Path
import glob
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, kendalltau, normaltest
from math import floor
from scipy.stats import friedmanchisquare
from scikit_posthocs import posthoc_dunn
from pingouin import compute_effsize
from cliffs_delta import cliffs_delta 
from scipy.stats import norm
###################################################################################################
###################################################################################################

#
def plot_event_related_lines(data1, data2, xaxis, label1 , label2, Title):
    
    data1m = np.nanmean(data1,axis=0)
    data1s = stats.sem(data1,0, nan_policy = 'omit')
    
    data2m = np.mean(data2,axis=0)
    data2s = stats.sem(data2,0, nan_policy = 'omit')

    
    
    plt.plot(xaxis, data1m,color='b',linestyle='-',linewidth=3, label = label1)
    plt.fill_between(xaxis, data1m-data1s, data1m+data1s,facecolor='b', alpha=0.25)

    plt.plot(xaxis, data2m,color='r',linestyle='-',linewidth=3, label = label2)
    plt.fill_between(xaxis, data2m-data2s, data2m+data2s,facecolor='r', alpha=0.25)

    plt.legend(prop={'size': 16}, frameon=False)
    plt.title(Title, fontsize = 24)

    #plt.axvline(x= 0, color='k',linestyle='--',linewidth=1)
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    #plt.ylabel('exponent', fontsize=28)
    #plt.xlabel('time relative to transition (s)', fontsize=20)
    
#########
# Checks the distriburtion of data (normal - not normally distruibuted)
def check_distribution(data):
    _, p_value = normaltest(data)
    is_normal = p_value > 0.05
    return is_normal

# performs correlations depending on the normality test (true or false for normality)
#returns correlation and p-value

def perform_correlation(x, y):
    
    _, p_value = normaltest(x)
    is_normal_x = p_value > 0.05

    _, p_value = normaltest(y)
    is_normal_y = p_value > 0.05

    if is_normal_x and is_normal_y:
        # Both arrays are normally distributed
        print("Using Pearson correlation")
        correlation, p_value = pearsonr(x, y)
    else:
        # At least one array is not normally distributed
        print("Using Spearman correlation")
        correlation, p_value = spearmanr(x, y)

    print(f"Correlation: {correlation}")
    print(f"P-value: {p_value}")    


###############
# Resample 30s staging files acccording to the required sampling rate
def resample_stages(path_file, new_samp_rate):
    stage_file = pd.read_csv(path_file)
    #set required time resolution - stages are in 30 seconds so the conversion depends on the time resolution specified
    cov_eq = 30/new_samp_rate
    stages = list(stage_file.iloc[:,0])
    stages_n = [val for val in stages for _ in range(0, floor(cov_eq))]
    return(stages_n)


#############
# Performs appropriate pairwise test after checking for normality of distribution
def pairwise_comparison(data1, data2, alpha=0.05):
    """
    Check the distribution of two datasets and perform appropriate pairwise statistical test.

    Parameters:
    - data1: numpy array or list, first dataset
    - data2: numpy array or list, second dataset
    - alpha: float, significance level (default is 0.05)

    Returns:
    - result: dict containing the following keys:
      - 'distribution_test': str, indicates the distribution type ('normal', 'non-normal')
      - 'test_result': str, indicates the result of the statistical test ('reject' or 'fail to reject')
      - 'p_value': float, p-value of the statistical test
      - 'test_statistic': float, test statistic value
      - 'effect_size': float, effect size (Cohen's d for t-test, U for Mann-Whitney U test)
    """
    # Perform distribution test
    _, p_value1 = stats.normaltest(data1)
    _, p_value2 = stats.normaltest(data2)

    if p_value1 < alpha or p_value2 < alpha:
        distribution_type = 'non-normal'
    else:
        distribution_type = 'normal'

    # Perform appropriate pairwise test
    if distribution_type == 'normal':
        statistic, p_value = stats.ttest_ind(data1, data2)
        effect_size = (np.mean(data1) - np.mean(data2)) / np.sqrt((np.std(data1)**2 + np.std(data2)**2) / 2)
        if p_value < alpha:
            test_result = 'reject'
        else:
            test_result = 'fail to reject'
    else:
        statistic, p_value = stats.mannwhitneyu(data1, data2)
        n1 = len(data1)
        n2 = len(data2)
        U = statistic
        effect_size = (U - (n1 * n2 / 2)) / np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        if p_value < alpha:
            test_result = 'reject'
        else:
            test_result = 'fail to reject'

    result = {
        'distribution_test': distribution_type,
        'test_result': test_result,
        'p_value': p_value,
        'test_statistic': statistic,
        'effect_size': effect_size
    }

    return result

###################
# Helper function for paths, check for the path and creates ones if not found
def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


###################
# Functions to perform friedman test and post-hoc Dunn with Bonferroni correction
def compute_z_values(p_values):
    """
    Calculate z-values from Dunn's test p-values.

    Parameters:
    - p_values: Array of p-values from pairwise comparisons.

    Returns:
    - Array of z-values.
    """
    # Ensure p-values are within the valid range [0, 1]
    p_values = np.clip(p_values, np.finfo(float).eps, 1 - np.finfo(float).eps)

    # Calculate two-sided z-values
    z_values = norm.ppf(1 - p_values / 2)

    return z_values


# bonferroni multiple comparison
def bonferroni_correction(p_values, num_comparisons):
    """
    Apply Bonferroni correction to p-values.

    Parameters:
    - p_values: Array of p-values.
    - num_comparisons: Number of pairwise comparisons.

    Returns:
    - Array of corrected p-values.
    """
    return np.minimum(p_values * num_comparisons, 1)

# MAIN FUNCTION (FRIEDMAN TEST FOLLOWED BY DUNN's)
def friedman_dunns(data):
    """
    Perform Friedman test followed by Dunn's post-hoc test.

    Parameters:
    - data: DataFrame where each column represents a treatment/sample.

    Returns:
    - Results DataFrame containing Friedman test statistics and Dunn's post-hoc results.
    """
    # Friedman test
    friedman_result = friedmanchisquare(*[data[col] for col in data.columns])
    W = friedman_result.statistic / (len(data)*(len(data.columns)-1))
    # Dunn's post-hoc test
    posthoc_result = posthoc_dunn(data.melt(var_name='groups', value_name='values'), val_col='values', group_col='groups')
     
    # Compute Z-values
    z_values = compute_z_values(posthoc_result.values)
    
    # Initialize a DataFrame for effect sizes
    effect_sizes = pd.DataFrame(index=data.columns, columns=data.columns)

    # Compute effect sizes using Cliff's Delta
    for i, col1 in enumerate(data.columns):
        for j, col2 in enumerate(data.columns):
            if i < j:
                effect_sizes.loc[col1, col2] = cliffs_delta(data[col1], data[col2])[0]
                effect_sizes.loc[col2, col1] = -effect_sizes.loc[col1, col2]
                
    # Apply Bonferroni correction to p-values
    num_comparisons = len(data.columns) * (len(data.columns) - 1) / 2
    cpv  = bonferroni_correction(posthoc_result.values, num_comparisons)
    corrected_p_values =  pd.DataFrame(cpv)


    return friedman_result, W, posthoc_result, z_values, effect_sizes, corrected_p_values

######################################

# Calculate (BIC) bayesian information criterion for gaussian data
def calculate_bic(n, mse, num_params):

    bic = n * np.log(mse) + num_params * np.log(n)

    return bic

##################################
def calculate_t_statistic(array1, array2):
    # Calculate the t-statistic for two independent samples
    num_obs1 = len(array1)
    num_obs2 = len(array2)
    
    mean_diff = np.mean(array1) - np.mean(array2)
    pooled_var = ((num_obs1 - 1) * np.var(array1, ddof=1) + (num_obs2 - 1) * np.var(array2, ddof=1)) / (num_obs1 + num_obs2 - 2)
    
    se = np.sqrt(pooled_var * (1/num_obs1 + 1/num_obs2))
    
    t_statistic = mean_diff / se
    
    return t_statistic

##########################################
def calculate_cohens_d(array1, array2):
    # Calculate Cohen's d for two independent samples
    mean_diff = np.mean(array1) - np.mean(array2)
    pooled_std = np.sqrt((np.std(array1, ddof=1)**2 + np.std(array2, ddof=1)**2) / 2)
    
    cohen_d = mean_diff / pooled_std
    
    return cohen_d

###########################################
def perform_permutation_test(array1, array2, num_permutations=1000):
    observed_t_statistic = calculate_t_statistic(array1, array2)
    observed_cohen_d = calculate_cohens_d(array1, array2)

    # Concatenate the arrays for permutation
    combined_array = np.concatenate([array1, array2])

    # Create an array to store permuted statistics
    permuted_t_statistics = np.zeros(num_permutations)
    permuted_cohen_ds = np.zeros(num_permutations)

    # Perform permutations
    for i in range(num_permutations):
        # Permute the labels (values)
        permuted_labels = np.random.permutation(combined_array)

        # Split the permuted array back into two arrays
        permuted_array1 = permuted_labels[:len(array1)]
        permuted_array2 = permuted_labels[len(array1):]

        # Calculate the permuted statistics
        permuted_t_statistic = calculate_t_statistic(permuted_array1, permuted_array2)
        permuted_cohen_d = calculate_cohens_d(permuted_array1, permuted_array2)

        permuted_t_statistics[i] = permuted_t_statistic
        permuted_cohen_ds[i] = permuted_cohen_d

    # Calculate the p-values
    p_value_t_statistic = np.mean(permuted_t_statistics >= observed_t_statistic)
    p_value_cohen_d = np.mean(permuted_cohen_ds >= observed_cohen_d)

    # Create a DataFrame to store results

    t = observed_t_statistic
    p = p_value_t_statistic
    d =  observed_cohen_d

    return t,p,d

##########################################################
def perform_baseline(dataV, timeV, l_lim, h_lim):
    """
    Perform baseline correction (absolute change)

    Parameters:
    - dataV: data
    - timeV: Time vector
    - l_lim: lower time limit for baseline
    - h_lim: upper time limit for baseline

    Returns:
    - Baseline corrected vector
    """
    idx = (timeV>l_lim)*(timeV<h_lim) #get times
    bl  = np.where(idx) # get indices of times in data
    dataN = np.ones(np.shape(dataV)) * np.nan
    
    for b in np.arange(np.shape(dataV)[0]):
        meanBL = np.nanmean(dataV[b,bl])

        for i in np.arange(np.shape(dataV)[1]):
        
            dataN[b,i] = (dataV[b,i]-meanBL)
            
    return(dataN)
