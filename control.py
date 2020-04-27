"""
Created on Wed Apr  7 13:20:48 2020

@author: minim
"""

import numpy as np

""" IMPORT REACTOR MODULES """
# import Chemistry_Module
# import Fluids_Module
# import Heat_Transfer_Module
# import Kinetics_Module
# import Purification_Module

def Example_Run_Sim(time):
    # THE FOLLOWING CODE IS DESIGNED TO CREATE EXAMPLE GRAPHS.
    # CODE IS NOT RESPRESENTATIVE OF THE FINAL PRODUCT.
    
    data = [0,0,0,0]   
    
    data[0] = np.random.randint(low=1400, high=1600, size=time)
    data[1] = np.random.randint(low=350, high=450, size=time)
    data[2] = np.random.randint(low=15, high=18, size=time)
    data[3] = np.random.randint(low=80, high=100, size=time)
    
    return data

def Run_Sim(time):
    
    datapoints = time * 86400 # One datapoint every minute
    
    # Create data pools
    data = [0,0,0,0,0]
    data[0] = np.zeros(datapoints)
    data[1] = np.zeros(datapoints)
    data[2] = np.zeros(datapoints)
    data[3] = np.zeros(datapoints)
    #data[4] = np.zeros(datapoints)
    
    # Initial Conditions
    hx_temperature = 1000
    concentration = 0.5
    pressure
    i = 0
    
    # Simulation Iteration
    while i < datapoints:
        
        data[0][i] = concentration
        
        # Reactor Kinetics
        rk_temperature = Reactor_Kinetics_Module.Temperature(hx_temperature, concentration)
        
        # Chemistry
        density = Chemisty_Module.Density(rk_temperature)
        viscosity = Chemisty_Module.Viscosity(rk_temperature)
        solubility = Chemisty_Module.Solubility(rk_temperature)
        
        # Fluid Mechanics
        mass_flow_rate = Fluids_Module.Mass_Flow_Rate(density, viscosity)
        if (i < 1):
            pressure = Fluids_Module.Pressure(mass_flow_rate, density, viscosity)
            
        # Heat Transfer
        hx_temperature = Heat_Transfer_Module.Temperature(density, viscosity, mass_flow_rate)
        power = Heat_Transfer_Module.Power(hx_temperature)
        
        # Purification
        concentration = Purification_Module.Concentration(mass_flow_rate)
        
        data[1][i] = power
        data[2][i] = rk_temperature
        data[3][i] = solubility
        
        i = i + 1
    
    return data



if (__name__ == "__main__"):
    data = Run_Sim(20)