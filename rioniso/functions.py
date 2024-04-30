import numpy as np
from scipy.constants import *

c = physical_constants['speed of light in vacuum'][0]

def gaussian(x, amplitude, mean, sigma):
    return amplitude * np.exp(-((x - mean) / sigma)**2 / 2)

def linear_gaussian_func(x, m, c, amplitude, mean, sigma):
    linear_term = m * x + c
    gaussian_term = gaussian(x, amplitude, mean, sigma)
    return linear_term + gaussian_term

def iso_curve(revt, gammat, dp_p, sys, path = 108.36):
    return np.sqrt((((1-(path/(revt*(c/1e9)))**2-1/(gammat**2))*dp_p*revt)**2+sys**2))

def iso_curve_f(revf, gammat, dp_p, sys, path = 108.36):
    return np.sqrt((((1-(path/c*revf)**2-1/(gammat**2))*dp_p*revf)**2+sys**2))

def calculate_reduced_chi_squared(y_data, y_fit, yerror, num_params):
    residuals = y_data - y_fit
    chi_squared = np.sum(residuals**2/yerror**2)
    dof = len(y_data) - num_params
    chi_squared_red = chi_squared / dof
    return chi_squared_red

def transform_to_revolution_time(harmonics, frequency, frequency_error, frequency_spread, frequency_spread_error):
    # Inputs: np.arrays
    revolution_time = 1e12 / (frequency / harmonics)
    revolution_time_error = frequency_error / (frequency**2) * harmonics * 1e12 # converting to picoseconds
    revolution_time_spread = frequency_spread / frequency * revolution_time
    revolution_time_spread_error =  harmonics / frequency / frequency / frequency * (frequency_spread_error * frequency + 2 * frequency_spread * frequency_error) * 1e12 # converting to picoseconds
    
    return revolution_time, revolution_time_error, revolution_time_spread, revolution_time_spread_error

#def fit_iso_curve(T, sT, seeds, sigma):#T and sT in ps
#    try:
#        fit_params, fit_covariance = curve_fit(iso_curve, T/1000, sT, p0=seeds,
#                                           sigma=sigma, absolute_sigma=True)
#        return fit_params, np.sqrt(np.diag(fit_covariance))
#
#    except RuntimeError:
#        pass