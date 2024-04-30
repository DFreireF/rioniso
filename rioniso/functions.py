import numpy as np

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