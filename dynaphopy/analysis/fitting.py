import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def lorentzian(x, a, b, c, d):
    return c/(np.pi*b*(1.0+((x-a)/b)**2))+d


def get_error_from_covariance(covariance):
    return abs(np.average(covariance))


def phonon_fitting_analysis(original, test_frequencies_range):

#    number_of_coefficients = parameters.number_of_coefficients_mem
#    test_frequencies_range = parameters.frequency_range

    print(range(original.shape[1]))
    for i in range(original.shape[1]):

        power_spectrum = original[:, i]

        height = np.max(power_spectrum)
        position = test_frequencies_range[np.argmax(power_spectrum)]

        try:
            fit_params, fit_covariances = curve_fit(lorentzian,
                                                    test_frequencies_range,
                                                    power_spectrum,
                                                    p0=[position, 0.1, height, 0.0])
        except:
            print('Warning: Fitting error, phonon',i)
            continue

        error = get_error_from_covariance(fit_covariances)
        width = 2.0*fit_params[1]

        print '\nPeak #', i+1
        print('------------------------------------')
        print 'Width(FWHM):', width, 'THz'
        print 'Position:', fit_params[0], 'THz'
        print 'Fitting Error:', error

        plt.figure(i+1)

        plt.xlabel('Frequency [THz]')
        plt.title('Curve fitting')

        plt.suptitle('Phonon '+str(i+1))
        plt.text(fit_params[0], height/2, 'Width: ' + "{:10.4f}".format(width),
                 fontsize=12)

        plt.plot(test_frequencies_range, power_spectrum,
                 label='Power spectrum')
        plt.plot(test_frequencies_range, lorentzian(test_frequencies_range, *fit_params),
                 label='Lorentzian fit',
                 linewidth=3)

        plt.legend()

    plt.show()
