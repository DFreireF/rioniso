import matplotlib.pyplot as plt
from adjustText import adjust_text
import textalloc as ta
import numpy as np

class Plotters(object):
    def __init__(self, iso_data, xfit, yfit):
        self._plot_fit(xfit, yfit)
        self._plot_data(iso_data)
        plt.show()

    def _plot_fit(self, xfit, yfit):
        plt.plot(xfit, yfit, 'r-',  linewidth=5)
    
    def _plot_data(self, iso_data):
        plt.errorbar(np.asarray(iso_data[:, 1], dtype=float), np.asarray(iso_data[:, 3], dtype=float), yerr=np.asarray(iso_data[:, 4], dtype=float), color = 'black', fmt = 'o')



        
#separate the one under
#def isochronicity_curve_plot(T, sT, names_latex, gammat_0 = 1.395, fts = 36):
#    fig, axs = plt.subplots(1, 1, figsize=(25, 15))
#    
#    x_fit = np.arange((T/1000).min()*1e6,(T/1000).max()*1e6, 10000) / 1e6
#        
#    sigma = y_sigmaT_errs
#    seeds = [gammat_0, 0.0008, 0.01]
#    fit iso curve
#
#    Gammat,         dpop,       sigma_t_sys  = fit_params
#    GammatError, dpopError, sigma_t_sysError = np.sqrt(np.diag(fit_covariance))
#
#    
#    label_axs2 = f'$\sqrt{{\left(1 - \left(\\frac{{108.36}}{{T \cdot c}}\\right)^2 - \\frac{{1}}#{{{Gammat:.4f}^2}}\\right)^2 \cdot \\left(\\frac{{{np.abs(dpop)*1e-1:.4f}}}{{100}} \cdot #T\\right)^2 + {abs(sigma_t_sys):.4f}^2}}$'
#    
#    axs.errorbar(T_y, y_sigmaT_vals_Y, yerr=np.sqrt(y_sigmaT_errs_Y**2+sigma_sys**2), fmt='o', #label="Calibrant ion",
#                    markersize='13', ecolor='black',capsize=4, elinewidth=3, color='blue')
#    
#    axs.plot(x_fit, iso_curve(x_fit, *fit_params), 'r-', label=label_axs2,  linewidth=5)
#    axs.set_xlabel(r"Revolution time, $T$ (ns)", fontsize = fts)
#    axs.set_ylabel(r"$\sigma_{T}$ (ps)", fontsize = fts)
#
#    axs.grid(True, linestyle=':', color='grey',alpha = 0.7)
#
#    handle_labels(axs, T, sT, names_latex, labels, fast)
#
#    axs.legend(shadow=True,fancybox=True, fontsize = fts-5)
#    axs.tick_params(axis='both', which='major', labelsize=fts)
#    return axs
#
#def handle_labels(axs, T, sT, names_latex, labels, fast):
#    if labels:
#        ta.allocate_text(fig, axs, T/1000, sT, names_latex, x_scatter=T/1000, y_scatter=sT,
#                        textsize=35, nbr_candidates=5000, seed=42, min_distance=0.05, #max_distance=0.4)
#
#def main(T,  sT, names_latex, gammat_0=1.395, labels=False, fast=True, fts=36):
#    # Preprocess data
#    indexes_corrected = np.concatenate((np.where(ref == 'Y')[0], np.where(ref == 'N')[0])).#tolist()
#    T, sT, names_latex, y_sigmaT_vals, y_sigmaT_errs, unknown_ions = prepare_data(T, T_y, T_n, #sT, Nuclei_Y, Nuclei_N, ref, names_latex, indexes_corrected)
#    sigma_sys = calculate_errors(y_sigmaT_errs, 1.5)  # Example chi2_fit_sigma value
#    # Setup plot
#    fig, axs = setup_plot(fts)
#    # Plot calibrant ions
#    plot_data(axs, T_y, y_sigmaT_vals[:len(T_y)], y_sigmaT_errs[:len(T_y)], sigma_sys, #"Calibrant ion", 'blue')
#    # Plot unknown ions if present
#    if unknown_ions > 0:
#        plot_data(axs, T_n, y_sigmaT_vals[len(T_y):], y_sigmaT_errs[len(T_y):], sigma_sys, #"Unknown ion", 'orange')
#    # Handle labels
#    handle_labels(axs, T, sT, names_latex, labels, fast)
#    