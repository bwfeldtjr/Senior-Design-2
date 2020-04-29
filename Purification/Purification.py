# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 15:00:20 2020

@author: Tim Easley
"""
import numpy as np
import math
import fluid dynamics as fluids


# Need to Import Mass Flow Rate, Concentration, Temperature
# Use Mass Flow Rate to calculate how long the fuel will be in the adsorption column
# Use Concentration as the basis for adsorption effectiveness
# Temperature is Temperature. Need to calculate some heat transfer to give temperature out.
# Also need to calculate reactivity added back into the system from purification

# Mass Flow Rate = kg/s
# Density = kg/m^3
# Volume = m^3
def Purif(PurificationFactor):
    '''
    Calculates required purification constant then applies. Input is desired factor of purification
    '''
    r = 0.9144 #column radius in m
    h = 1.524 #column height in m
    V = np.pi*(r**2)*(h) #volume of column in m^3

    Mfrt = fluids.function[:,2]
    density = #Import from fluid dynamics
    t = (V*density)/Mfrt #time in adsorption column

    C_i =  #import from Reactor Kinetics
    k = -ln(PurificationFactor)/t
    CF = np.exp(-k*t) #factor by which concentration is modified
    C_f = C_i*CF
    
    
    return C_f    
    

#Add more for each different fission product