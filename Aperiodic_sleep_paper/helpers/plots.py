"""Helper plot functions for the sleep project"""

from matplotlib import cm
import numpy as np
import mne
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import colors
###################################################################################################
###################################################################################################

def plot_topo(data, raw, vmin, vmax, label=None, ax=None):
    """Plots the topography of a spectral parameter."""

    mne.viz.plot_topomap(data, raw.info, vmin=vmin, vmax=vmax,
                         cmap=cm.viridis, contours=0, axes=ax);
    ax.set_title(label)

def plot_topo_colorbar(vmin, vmax, label, save_fig=True):
    """Creates a colorbar for the topography plots.
    vmin: int
    vmax: int
    label: str
    saave_fig: bool
    """
    fig = plt.figure(figsize=(2, 3))
    ax1 = fig.add_axes([0.9, 0.25, 0.15, 0.9])

    cmap = cm.viridis
    norm = colors.Normalize(vmin=vmin, vmax=vmax)

    cb1 = colorbar.ColorbarBase(plt.gca(), cmap=cmap,
                                norm=norm, orientation='vertical')

    save_figure(save_fig, label + '_cb')

#####################################################################################
def plot_event_related_lines(data1, data2, xaxis, label1 , label2, Title, color1, color2):
    
    data1m = np.nanmean(data1,axis=0)
    data1s = stats.sem(data1,0, nan_policy = 'omit')
    
    data2m = np.mean(data2,axis=0)
    data2s = stats.sem(data2,0, nan_policy = 'omit')

    plt.plot(xaxis, data1m,color=color1,linestyle='-',linewidth=3, label = label1)
    plt.fill_between(xaxis, data1m-data1s, data1m+data1s,facecolor=color1, alpha=0.25)

    plt.plot(xaxis, data2m,color=color2,linestyle='-',linewidth=3, label = label2)
    plt.fill_between(xaxis, data2m-data2s, data2m+data2s,facecolor=color2, alpha=0.25)

    plt.legend(prop={'size': 16}, frameon=False)
    plt.title(Title, fontsize = 24)

    #plt.axvline(x= 0, color='k',linestyle='--',linewidth=1)
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    #plt.ylabel('exponent', fontsize=28)
    #plt.xlabel('time relative to transition (s)', fontsize=20)
    
    