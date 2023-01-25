"""Helper plot functions for the sleep project"""

from matplotlib import cm

import mne

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
