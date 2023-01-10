"""Helper plot functions for the sleep project"""

from matplotlib import cm

from mne.viz import plot_topomap

###################################################################################################
###################################################################################################

def plot_topo(data, raw, vmin, vmax, label=None, ax=None):
    """Plots the topography of a spectral parameter."""

    plot_topomap(data, raw.info, vmin=vmin, vmax=vmax,
                 cmap=cm.viridis, contours=0, axes=ax);
    ax.set_title(label)
