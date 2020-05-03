# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 15:00:20 2020

@author: Tim Easley
"""
import numpy as np
import math
from numpy import log as ln


# Need to Import Mass Flow Rate, Concentration, Temperature
# Use Mass Flow Rate to calculate how long the fuel will be in the adsorption column
# Use Concentration as the basis for adsorption effectiveness
# Temperature is Temperature. Need to calculate some heat transfer to give temperature out.
# Also need to calculate reactivity added back into the system from purification

# Mass Flow Rate = kg/s
# Density = kg/m^3
# Volume = m^3
def Purif(PurificationFactor, C_i, N, Mfrt, density):
    '''
    Calculates required purification constant then applies. Input is desired factor of purification
    '''
    r = 0.9144 #column radius in m
    h = 1.524 #column height in m
    V = np.pi*(r**2)*(h) #volume of column in m^3

    t = (V*density)/Mfrt #time in adsorption column

    k = -ln(PurificationFactor)/t
    CF = float(np.exp(-k*t)) #factor by which concentration is modified
    #C_f = C_i * CF
    i = 0
    C_f = [0,0,0,0,0,0]
    
    while i < 6:
        C_f[i] = C_i[i] * CF
        i = i + 1
    
    return [C_f, N]

#Add more for each different fission product
if (__name__ == "__main__"):
    """Define Inputs"""
    PurificationFactor = None
    C_i = None
    Mfrt = None
    desnity = None
    data = Purif(PurificationFactor, C_i, N, Mfrt, density)