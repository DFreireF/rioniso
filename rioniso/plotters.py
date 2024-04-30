import matplotlib.pyplot as plt
from adjustText import adjust_text
import textalloc as ta
import numpy as np

class Plotters(object):
    def __init__(self, iso_data, xfit, yfit):
        self.mean_freq = np.asarray(iso_data[:, 1], dtype=float)*1e-6
        self.sigma_freq = np.asarray(iso_data[:, 3], dtype=float)
        self.sigma_freq_err = np.asarray(iso_data[:, 4], dtype=float)
        names = iso_data[:,0]
        self._plot(xfit*1e-6, yfit, names)
        
    def _plot(self, xfit, yfit, names):
        self._set_fig()
        self._plot_fit(xfit, yfit)
        self._plot_data()
        self.handle_labels(names)
        plt.show()

    def _set_fig(self):
        fontsize = 18
        self.fig, self.axs = plt.subplots(1, 1, figsize=(15, 8))
        self.axs.set_xlabel(r"Revolution frequency (MHz)", fontsize = fontsize)
        self.axs.set_ylabel(r"$\sigma_{f}$ (Hz)", fontsize = fontsize)
        self.axs.grid(True, linestyle=':', color='grey',alpha = 0.7)
        #self.axs.legend(shadow=True,fancybox=True, fontsize = fontsize-5)
        self.axs.tick_params(axis='both', which='major', labelsize=fontsize)

    def _plot_fit(self, xfit, yfit):
        self.axs.plot(xfit, yfit, 'r-',  linewidth=5)
    
    def _plot_data(self):
        self.axs.errorbar(self.mean_freq, self.sigma_freq, yerr=self.sigma_freq_err, color = 'black', fmt = 'o')

    def handle_labels(self, names_latex):
        ta.allocate_text(self.fig, self.axs, self.mean_freq, self.sigma_freq, names_latex, x_scatter=self.mean_freq, y_scatter=self.sigma_freq,
                        textsize=15, nbr_candidates=5000, seed=42, min_distance=0.05, max_distance=0.4)


        


#    label_axs2 = f'$\sqrt{{\left(1 - \left(\\frac{{108.36}}{{T \cdot c}}\\right)^2 - \\frac{{1}}#{{{Gammat:.4f}^2}}\\right)^2 \cdot \\left(\\frac{{{np.abs(dpop)*1e-1:.4f}}}{{100}} \cdot #T\\right)^2 + {abs(sigma_t_sys):.4f}^2}}$'
#    
#    axs.errorbar(T_y, y_sigmaT_vals_Y, yerr=np.sqrt(y_sigmaT_errs_Y**2+sigma_sys**2), fmt='o', #label="Calibrant ion",
#                    markersize='13', ecolor='black',capsize=4, elinewidth=3, color='blue')
#    
#    axs.plot(x_fit, iso_curve(x_fit, *fit_params), 'r-', label=label_axs2,  linewidth=5)

#    return axs