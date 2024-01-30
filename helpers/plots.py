"""Helper plot functions for the sleep project"""

from matplotlib import cm
import numpy as np
import mne
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import colors

from fooof.core.utils import nearest_ind
from fooof.core.errors import NoModelError
from fooof.core.funcs import gaussian_function
from fooof.core.modutils import safe_import, check_dependency
from fooof.sim.gen import gen_aperiodic
from fooof.plts.utils import check_ax
from fooof.plts.spectra import plot_spectrum
from fooof.plts.settings import PLT_FIGSIZES, PLT_COLORS
from fooof.plts.style import check_n_style, style_spectrum_plot
from fooof.analysis.periodic import get_band_peak_fm
from fooof.utils.params import compute_knee_frequency, compute_fwhm

plt = safe_import('.pyplot', 'matplotlib')
mpatches = safe_import('.patches', 'matplotlib')

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
    
 #########################################################################################

def plot_annotated_modelx(fm, y1,y2, plt_log=False, annotate_peaks=True, annotate_aperiodic=True,
                         ax=None, plot_style=style_spectrum_plot):
    """Plot a an annotated power spectrum and model, from a FOOOF object.

    Parameters
    ----------
    fm : FOOOF
        FOOOF object, with model fit, data and settings available.
    plt_log : boolean, optional, default: False
        Whether to plot the frequency values in log10 spacing.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    plot_style : callable, optional, default: style_spectrum_plot
        A function to call to apply styling & aesthetics to the plots.

    Raises
    ------
    NoModelError
        If there are no model results available to plot.
    """

    # Check that model is available
    if not fm.has_model:
        raise NoModelError("No model is available to plot, can not proceed.")

    # Settings
    fontsize = 15
    lw1 = 4.0
    lw2 = 3.0
    ms1 = 12

    # Create the baseline figure
    ax = check_ax(ax, PLT_FIGSIZES['spectral'])
    fm.plot(plt_log=plt_log, ax=ax, plot_style=None,
            data_kwargs={'lw' : lw1, 'alpha' : 0.6},
            aperiodic_kwargs={'lw' : lw1, 'zorder' : 10},
            model_kwargs={'lw' : lw1, 'alpha' : 0.5}
            )


    # Get freqs for plotting, and convert to log if needed
    freqs = fm.freqs if not plt_log else np.log10(fm.freqs)
    plt.xlim(freqs[0]-0.1,freqs[-1]+0.1)
    plt.ylim(y1,y2)
    ax1=plt.gca()
    
    
    plt.xticks(fontsize=34)
    plt.yticks(fontsize=34)
    plt.grid(False)
    
    ## Buffers: for spacing things out on the plot (scaled by plot values)
    x_buff1 = max(freqs) * 0.1
    x_buff2 = max(freqs) * 0.25
    y_buff1 = 0.15 * np.ptp(ax.get_ylim())
    shrink = 0.1

    # There is a bug in annotations for some perpendicular lines, so add small offset
    #   See: https://github.com/matplotlib/matplotlib/issues/12820. Fixed in 3.2.1.
    bug_buff = 0.000001

    if annotate_peaks:

        # Extract largest peak, to annotate, grabbing gaussian params
        gauss = get_band_peak_fm(fm, fm.freq_range, attribute='gaussian_params')

        peak_ctr, peak_hgt, peak_wid = gauss
        bw_freqs = [peak_ctr - 0.5 * compute_fwhm(peak_wid),
                    peak_ctr + 0.5 * compute_fwhm(peak_wid)]

        if plt_log:
            peak_ctr = np.log10(peak_ctr)
            bw_freqs = np.log10(bw_freqs)

        peak_top = fm.power_spectrum[nearest_ind(freqs, peak_ctr)]

    if annotate_aperiodic:

        # Annotate Aperiodic Offset
        #   Add a line to indicate offset, without adjusting plot limits below it
        ax.set_autoscaley_on(False)
        ax.plot([freqs[0], freqs[0]], [ax.get_ylim()[0], fm.fooofed_spectrum_[0]],
                color=PLT_COLORS['aperiodic'], linewidth=lw2, alpha=0.5)
        ax.annotate('Offset',
                    xy=(freqs[0]+bug_buff, fm.power_spectrum[0]-y_buff1),
                    xytext=(freqs[0]-x_buff1, fm.power_spectrum[0]-y_buff1),
                    verticalalignment='center',
                    horizontalalignment='center',
                    arrowprops=dict(facecolor=PLT_COLORS['aperiodic'], shrink=shrink),
                    color=PLT_COLORS['aperiodic'], fontsize=fontsize)

        # Annotate Aperiodic Knee
        if fm.aperiodic_mode == 'knee':

            # Find the knee frequency point to annotate
            knee_freq = compute_knee_frequency(fm.get_params('aperiodic', 'knee'),
                                               fm.get_params('aperiodic', 'exponent'))
            knee_freq = np.log10(knee_freq) if plt_log else knee_freq
            knee_pow = fm.power_spectrum[nearest_ind(freqs, knee_freq)]

            # Add a dot to the plot indicating the knee frequency
            ax.plot(knee_freq, knee_pow, 'o', color=PLT_COLORS['aperiodic'], ms=ms1*1.5, alpha=0.7)

            ax.annotate('Knee',
                        xy=(knee_freq, knee_pow),
                        xytext=(knee_freq-x_buff2, knee_pow-y_buff1),
                        verticalalignment='center',
                        arrowprops=dict(facecolor=PLT_COLORS['aperiodic'], shrink=shrink),
                        color=PLT_COLORS['aperiodic'], fontsize=fontsize)

        # Annotate Aperiodic Exponent
        mid_ind = int(len(freqs)/2)
        ax.annotate('Exponent',
                    xy=(freqs[mid_ind], fm.power_spectrum[mid_ind]),
                    xytext=(freqs[mid_ind]-x_buff2, fm.power_spectrum[mid_ind]-y_buff1),
                    verticalalignment='center',
                    arrowprops=dict(facecolor=PLT_COLORS['aperiodic'], shrink=shrink),
                    color=PLT_COLORS['aperiodic'], fontsize=fontsize)

    # Apply style to plot & tune grid styling
    check_n_style(plot_style, ax, plt_log, True)

    # Add labels to plot in the legend
    da_patch = mpatches.Patch(color=PLT_COLORS['data'], label='Original Data')
    ap_patch = mpatches.Patch(color=PLT_COLORS['aperiodic'], label='Aperiodic Parameters')
    pe_patch = mpatches.Patch(color=PLT_COLORS['periodic'], label='Peak Parameters')
    mo_patch = mpatches.Patch(color=PLT_COLORS['model'], label='Full Model')

    handles = [da_patch, ap_patch if annotate_aperiodic else None,
               pe_patch if annotate_peaks else None, mo_patch]
    handles = [el for el in handles if el is not None]

    ax.legend(handles=handles, handlelength=1, fontsize='x-large')

