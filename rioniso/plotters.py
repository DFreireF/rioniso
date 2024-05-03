import matplotlib.pyplot as plt
import textalloc as ta
import numpy as np

class Plotters(object):
    def __init__(self, width=10, height=8, dpi=300, fs = 14):
        self.mean_freq      = np.array([])
        self.sigma_freq     = np.array([])
        self.sigma_freq_err = np.array([])
        self.names          = np.array([])
        self.xfit           = np.array([])
        self.yfit           = np.array([])
        self.fit_parameters = np.array([])
        self.marker_visibility = []
        self.fontsize = fs
        self._set_fig(width, height, dpi)

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
        obj.marker_visibility = [True] * len(obj.mean_freq)
        return obj

    def update_plot(self):
        self.axs.clear()  # Clear previous contents
        self.set_axs_style()
        self._plot_fit(*self.fit_parameters)
        self._plot_data()
        self.fig.canvas.draw_idle() # Redraw the current figure
        

    def _set_fig(self, width, height, dpi):
        self.fig, self.axs = plt.subplots(1, 1, figsize=(width, height), dpi = dpi, layout='tight')
        self.set_axs_style()

    def set_axs_style(self):
        self.axs.set_xlabel(r"Revolution frequency (MHz)", fontsize =  self.fontsize)
        self.axs.set_ylabel(r"$\sigma_{f}$ (Hz)", fontsize =  self.fontsize)
        self.axs.grid(True, linestyle=':', color='grey',alpha = 0.7)
        self.axs.tick_params(axis='both', which='major', labelsize= self.fontsize)

    def _plot_fit(self, gammat, dpop, sigma_sys):
        label = f'$\sqrt{{\left(1 - \left(\\frac{{f \cdot 108.36}}{{c}}\\right)^2 - \\frac{{1}}{{{gammat:.4f}^2}}\\right)^2 \cdot \\left(\\frac{{{np.abs(dpop)*1e2:.4f}}}{{100}} \cdot f\\right)^2 + {abs(sigma_sys):.4f}^2}}$'
        self.axs.plot(self.xfit, self.yfit, '-', color='blue',  linewidth=5, label = label)
        self.axs.legend(shadow=True, fancybox=True, fontsize = self.fontsize-3)
    
    def _plot_data(self):
        for i in range(len(self.mean_freq)):
            self.axs.errorbar(
                self.mean_freq[i], self.sigma_freq[i], yerr=self.sigma_freq_err[i],
                fmt='o', picker = True, pickradius = 3, color='black' if self.marker_visibility[i] else 'red'
            )

    def handle_labels(self):
        ta.allocate_text(self.fig, self.axs, self.mean_freq, self.sigma_freq, self.names, x_scatter=self.mean_freq, y_scatter=self.sigma_freq,
                        textsize=7)#, nbr_candidates=5000, seed=42, min_distance=0.05, max_distance=0.4)
        self.fig.canvas.draw_idle()

    def toggle_visibility(self, index):
        """ Toggle the visibility of the data point at the given index. """
        self.marker_visibility[index] = not self.marker_visibility[index]
        self.update_plot()
    
    def update_indexes(self):
        return self.marker_visibility

    def handle_events(self, event):
        xdata = event.artist.get_xdata()
        ydata = event.artist.get_ydata()
        for i, (x, y) in enumerate(zip(self.mean_freq, self.sigma_freq)):
            if x == xdata[0] and y == ydata[0]:  # Checking coordinates match
                self.toggle_visibility(i)
                break