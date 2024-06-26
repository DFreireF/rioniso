from iqtools import *
import numpy as np
from scipy.optimize import curve_fit
from rioniso.functions import *

class IsoCurve(object):

    def __init__(self):
        self.simulated_data = np.array([])
        self.experimental_data = np.array([])
        self.iso_data = np.array([])
        self.fit_indices = np.array([])

    @classmethod
    def create_object(cls, simulated_data, experimental_data):
        obj = cls()
        obj.simulated_data = simulated_data
        obj.experimental_data = experimental_data
        obj.get_iso_data()
        obj.fit_indices = np.arange(0, len(obj.iso_data), 1) #by default all the index will be displayed
        return obj

    def create_fit_properties(self):
        self.set_iso_curve_fit_parameters()
        self.set_fit_data()

    def get_iso_data(self, xspan = 6e3):
        self.iso_data = self.calculate_iso_inputs(self.simulated_data, self.experimental_data, xspan=xspan)
    
    def calculate_iso_inputs(self, simulated_data, data, xspan = 3e3):
        iso_data = []
        for label, harmonic, frequency in zip(simulated_data[:,0], simulated_data[:,1],     simulated_data[:,-1]):
            xx, _, zz = get_cut_spectrogram(data['xx'], data['yy'], data['zz'], 
                        xcen = float(frequency), xspan = xspan)
            x = xx[0,:]
            az = np.average(zz, axis = 0)
            p0 = [0, 1000, 1000,-0, 400]
            try:
                lower_bounds = [-np.inf, -np.inf, -np.inf, -np.inf, 40]
                upper_bounds = [np.inf, np.inf, np.inf, np.inf, 1000]

                popt, pcov = curve_fit(linear_gaussian_func, x, az, p0=p0,
                    bounds=(lower_bounds, upper_bounds))
                m, c, amplitude, mean, sigma = popt
                me, ce, amplitudee, meane, sigmae = np.sqrt(np.diag(pcov))
                fit_params = [label, mean + float(frequency)/float(harmonic), meane/float   (harmonic), np.abs(sigma)/float(harmonic), sigmae/float(harmonic), amplitude,  amplitudee]
                iso_data.append(fit_params)

            except RuntimeError:
                pass

        return np.array(iso_data)

    def set_iso_curve_fit_parameters(self):
        try:
            self.mean = np.asarray(self.iso_data[:, 1][self.fit_indices], dtype=float)
            self.sigma = np.asarray(self.iso_data[:, 3][self.fit_indices], dtype=float)
            #sigma_e = np.asarray(self.iso_data[:, 4][visible_indices], dtype=float)
            self.fit_parameters, self.fit_errors = fit_iso_curve_f(self.mean, self.sigma)

        except Exception as e:
            print(f"Error calculating fit parameters: {e}")
            self.fit_parameters, self.fit_errors = None, None
    
    def set_fit_data(self, step = 100):
        self.fit_range = np.arange(self.mean.min(), self.mean.max(), step)
        self.fit_values = iso_curve_f(self.fit_range, *self.fit_parameters)


def fit_iso_curve_f(f, sigma, errors = None, seeds = [1.395, 2e-4, 0.5]):
    try:
        if errors is not None:
            fit_params, fit_covariance = curve_fit(iso_curve_f, f, sigma, p0=seeds,
                                            sigma=errors, absolute_sigma=True)
        else: 
            fit_params, fit_covariance = curve_fit(iso_curve_f, f, sigma, p0=seeds)
        return fit_params, np.sqrt(np.diag(fit_covariance))

    except RuntimeError:
        print('Fit iso curve error')
        pass

def mass_resolving_power(mean, sigma, gammat):
    return (2*np.sqrt(2*np.log(2))*sigma)**(-1) * mean * gammat**(-2)

def FWHM_resolvable_isomer(resolving_power, mass):
    return mass / R