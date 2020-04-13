# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math

def primary_density(T): # T must be in celcius
    density = 2.38 - (40E-5) * T # [g/cm^3]
    return density

def primary_viscosity(T):
    viscosity = 8.4 # [cP] At 600 celcius
    return viscosity

def secondary_density(T): # T must be in celcius
    density = 2.16 - (40E-5) * T # [g/cm^3]
    return density

def secondary_viscosity(T): # T must be in celsius
    T= T+273
    viscosity = 0.118 * math.exp(3624 / T) # [cP]
    return viscosity

    
    