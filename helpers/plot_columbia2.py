def plot_hd_topo(data, raw, zmin, zmax, ax):
    """Plots the topography of a spectral parameter."""

    
    mne.viz.plot_topomap(data, raw.info, vmin=zmin, vmax=zmax,
                         cmap=cm.viridis, contours=0, axes=ax);
    ax.set_title(label)
