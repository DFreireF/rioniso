from iqtools import *
import numpy as np
from scipy.optimize import curve_fit

def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / stddev)**2 / 2)

def linear_gaussian_func(x, m, c, amplitude, mean, sigma):
    linear_term = m * x + c
    gaussian_term = gaussian(amplitude, mean, sigma)
    return linear_term + gaussian_term

def iso_curve(revt, gammat, dp_p, sys, path = 108.36):
    return np.sqrt((((1-(path/(revt*(c/1e9)))**2-1/(gammat**2))*dp_p*revt)**2+sys**2))

def fit_iso_curve(T, sT, seeds, sigma):#T and sT in ps
    try:
        fit_params, fit_covariance = curve_fit(iso_curve, T/1000, sT, p0=seeds,
                                           sigma=sigma, absolute_sigma=True)
        return fit_params, fit_covariance

    except RuntimeError:
        pass

def calculate_reduced_chi_squared(y_data, y_fit, yerror, num_params):
    residuals = y_data - y_fit
    chi_squared = np.sum(residuals**2/yerror**2)
    dof = len(y_data) - num_params
    chi_squared_red = chi_squared / dof
    return chi_squared_red

def calculate_iso_inputs(simulated_data, data):
    for frequency in simulated_data:
        xx, yy, zz = get_cut_spectrogram(data['xx'],data['yy'],data['zz'], 
                    xcen = frequency, xspan = 7e3)
        az = np.average(zz, axis = 0)
        p0 = [0,1000, 1000,-0, 400]
        try:
            popt, pcov = curve_fit(linear_gaussian_func, xx[0,:], az, p0=p0)
            m, c, amplitude, mean, sigma = popt
            plt.plot(xx[0,:], az)
            plt.plot(xx[0,:],linear_gaussian_func(xx[0,:], m, c, amplitude, mean, sigma))
            plt.show()
            print('center',int(np.round(popt[3]+xcen)),  int(np.round(np.sqrt(np.diag(pcov))[3])))
            print('sigma',int(np.round(popt[4])),  int(np.round(np.sqrt(np.diag(pcov))[4])))
            print('amp',int(np.round(popt[2])),  int(np.round(np.sqrt(np.diag(pcov))[2])))
        except RuntimeError:
            pass

def transform_to_revolution_time(harmonics, frequency, frequency_error, frequency_spread, frequency_spread_error):
    # Inputs: np.arrays
    revolution_time = 1e12 / (frequency / harmonics)
    revolution_time_error = frequency_error / (frequency**2) * harmonics * 1e12 # converting to picoseconds
    revolution_time_spread = frequency_spread / frequency * revolution_time
    revolution_time_spread_error =  harmonics / frequency / frequency / frequency * (frequency_spread_error * frequency + 2 * frequency_spread * frequency_error) * 1e12 # converting to picoseconds
    
    return revolution_time, revolution_time_error, revolution_time_spread, revolution_time_spread_error