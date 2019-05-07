from __future__ import division, print_function, absolute_import

from tmm.tmm_core import (coh_tmm, unpolarized_RT, ellips,
                       position_resolved, find_in_structure_with_inf)

from numpy import pi, linspace, inf, array
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

try:
    import colorpy.illuminants
    import colorpy.colormodels
    from . import color
    colors_were_imported = True
except ImportError:
    # without colorpy, you can't run sample5(), but everything else is fine.
    colors_were_imported = False


# "5 * degree" is 5 degrees expressed in radians
# "1.2 / degree" is 1.2 radians expressed in degrees
degree = pi/180



def bilayer(center_lambda):
    """
    Here's a thin non-absorbing layer, on top of a thick absorbing layer, with
    air on both sides. Plotting reflected intensity versus wavenumber, at two
    different incident angles.
    """
    n_silica = 1.45704
    n_tantalum = 2.1306
    
    dHigh = center_lambda / (4 * n_tantalum)
    dLow = center_lambda / (4 * n_silica)
    
    # list of layer thicknesses in nm
    d_list = [inf, dHigh, dLow, dHigh, dLow, dHigh, dLow, dHigh, dHigh, dLow, dHigh, dLow, dHigh, dLow, dHigh,inf]
    # list of refractive indices
    n_list = [1, n_tantalum,n_silica,n_tantalum,n_silica,n_tantalum,n_silica,n_tantalum,n_tantalum,n_silica,n_tantalum,n_silica,n_tantalum,n_silica,n_tantalum,1.5]
    # list of wavenumbers to plot in nm^-1
    lambda_list = linspace(400, 800, num=100) #in nm 
    # initialize lists of y-values to plot
    T_list = []
    for lambda_vac in lambda_list:
		# For normal incidence, s and p polarizations are identical.
		# I arbitrarily decided to use 's'.
        T_list.append(coh_tmm('s', n_list, d_list, 0, lambda_vac)['T'])
    plt.figure()
    plt.plot(lambda_list, T_list)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Fraction of power transmitted')
    plt.title('Transmission vs. wavelengths')
    
    with open('transmittance.txt', 'w') as t_file:
        for x in T_list:
            x = str(x)
            t_file.write(x + '\n')
            
    with open('wavelength.txt', 'w') as w_file:
        for y in lambda_list:
            y = str(y)
            w_file.write(y + '\n')
            
    #print(lambda_list[T_list.index(max(T_list))], max(T_list), lambda_list[T_list.index(min(T_list))], min(T_list))
