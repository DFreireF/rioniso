import matplotlib.pyplot as plt
import textalloc as ta
import numpy as np

class Plotters(object):
    def __init__(self):
        self.mean_freq      = np.array([])
        self.sigma_freq     = np.array([])
        self.sigma_freq_err = np.array([])
        self.names          = np.array([])
        self.xfit           = np.array([])
        self.yfit           = np.array([])
        self.fit_parameters = np.array([])
        self.fitted_indexes = np.array([])

    @classmethod
    def create_object(cls, iso_data, xfit, yfit, fit_parameters, fitted_indexes):
        obj = cls()
        obj.mean_freq = np.asarray(iso_data[:, 1], dtype=float) * 1e-6
        obj.sigma_freq = np.asarray(iso_data[:, 3], dtype=float)
        obj.sigma_freq_err = np.asarray(iso_data[:, 4], dtype=float)
        obj.names = iso_data[:, 0]
        obj.xfit = xfit * 1e-6
        obj.yfit = yfit
        obj.fit_parameters = fit_parameters
        obj.fitted_indexes = fitted_indexes
        return obj

    def update_plot(self):
        self._set_fig()
        self._plot_fit(*self.fit_parameters)
        self._plot_data()
        self.handle_labels()
        self.fig.canvas.draw_idle() # Redraw the current figure

    def _set_fig(self, width=15, height=8, dpi=300, fs = 18):
        fontsize = fs
        self.fig, self.axs = plt.subplots(1, 1, figsize=(width, height), dpi = dpi)
        self.axs.set_xlabel(r"Revolution frequency (MHz)", fontsize = fontsize)
        self.axs.set_ylabel(r"$\sigma_{f}$ (Hz)", fontsize = fontsize)
        self.axs.grid(True, linestyle=':', color='grey',alpha = 0.7)
        self.axs.tick_params(axis='both', which='major', labelsize=fontsize)

    def _plot_fit(self, gammat, dpop, sigma_sys):
        label = f'$\sqrt{{\left(1 - \left(\\frac{{f \cdot 108.36}}{{c}}\\right)^2 - \\frac{{1}}{{{gammat:.4f}^2}}\\right)^2 \cdot \\left(\\frac{{{np.abs(dpop)*1e2:.4f}}}{{100}} \cdot f\\right)^2 + {abs(sigma_sys):.4f}^2}}$'
        self.axs.plot(self.xfit, self.yfit, '-', color='blue',  linewidth=5, label = label)
        self.axs.legend(shadow=True,fancybox=True, fontsize = 13)
    
    def _plot_data(self):
        self.points = self.axs.errorbar(self.mean_freq, self.sigma_freq, yerr=self.sigma_freq_err, color = 'black', fmt = 'o', picker = True, pickradius = 5)

    def handle_labels(self):
        ta.allocate_text(self.fig, self.axs, self.mean_freq, self.sigma_freq, self.names, x_scatter=self.mean_freq, y_scatter=self.sigma_freq,
                        textsize=15, nbr_candidates=5000, seed=42, min_distance=0.05, max_distance=0.4)

    def toggle_visibility(self, index):
        """ Toggle the visibility of the data point at the given index. """
        current_alpha = self.points[index].get_alpha()
        new_alpha = 0.25 if current_alpha == 1 else 1  # Toggle between 0.25 and 1
        self.points[index].set_alpha(new_alpha)
        self.fig.canvas.draw_idle()  # Redraw the plot
    
    def update_indexes(self):
        fitted_indexes = []
        for i, point in enumerate(self.points):
            if point.get_alpha() == 1:
                fitted_indexes.append(i)
        self.fitted_indexes = np.array(fitted_indexes)
