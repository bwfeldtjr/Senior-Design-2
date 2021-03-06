"""
Created on Wed Apr  7 13:20:48 2020

@author: minim
"""

import numpy as np

""" IMPORT REACTOR MODULES """
import Chemistry
import Fluids
import Heat_Exchanger_1 as HXC1
import Heat_Exchanger_2 as HXC2
import Kinetics
import Purification

def Run_Sim(time):
    
    datapoints = time #* 86400 # One datapoint every minute
    
    # Create data pools
    data = [0,0,0,0,0,0]
    data[0] = np.zeros(datapoints)
    data[1] = np.zeros(datapoints)
    data[2] = np.zeros(datapoints)
    data[3] = np.zeros(datapoints)
    data[4] = np.zeros(datapoints)
    data[5] = np.zeros(datapoints)
    
    # Initial Conditions
    HX2_Temp = 900
    concentration = 0.0
    concentration_factor = 0.001
    N = 100000
    i = 0

    
    # Simulation Iteration
    while i < datapoints:
        
        
        # Reactor Kinetics
        if i < 1:
            data[0][i] = concentration
        else:
            data[0][i] = concentration[0] #ERROR HERE
        rk_data = Kinetics.fun(HX2_Temp, concentration, N)
        rk_temperature = rk_data[0]
        C_i = rk_data[1][0]
        N = rk_data[2]

        
        # Chemistry
        density_fuel = Chemistry.primary_density(rk_temperature)
        viscosity_fuel = Chemistry.primary_viscosity(rk_temperature)
        density_cool = Chemistry.secondary_density(rk_temperature)
        viscosity_cool = Chemistry.secondary_viscosity(rk_temperature)
        solubility = Chemistry.solubilitypercentage(rk_temperature)
        
        # Fuel Fluid Mechanics
        fluids_data = Fluids.function(rk_temperature, HX2_Temp)
        pressureR = fluids_data[0]
        mass_flow_rateR = fluids_data[1]
        mass_flow_rateHX = fluids_data[2]
        
        # Heat Exhanger 1
        HX1_Temp = HXC1.CounterFlowOutputs(mass_flow_rateR,
                                           mass_flow_rateHX,
                                           rk_temperature,
                                           viscosity_fuel)
        
        # Heat Exchanger 2
        hx_data = HXC2.CounterFlowOutputs(mass_flow_rateR,
                                          mass_flow_rateHX,
                                          HX1_Temp,
                                          viscosity_fuel)
        HX2_Temp = hx_data[0]
        power = hx_data[1]
        

        # Coolant Fluid Mechanics
        coolant_data = Fluids.coolant(HX1_Temp, HX2_Temp) 
        pressureC = coolant_data[0]
        mass_flow_rateHE1 = coolant_data[1]
        mass_flow_rateHE2 = coolant_data[2]
        

        
        # Purification
        purification_data = Purification.Purif(concentration_factor,
                                           C_i,
                                           N,
                                           mass_flow_rateR,
                                           density_fuel)
        concentration = purification_data[0]
        #print(concentration)
        N = purification_data[1]
        
        # Data Collection (UNFINISHED)
        data[1][i] = power
        data[2][i] = rk_temperature
        data[3][i] = solubility
        data[4][i] = HX1_Temp
        data[5][i] = HX2_Temp
        
        
        i = i + 1
    
    return data


if (__name__ == "__main__"):
    data = Run_Sim(10)
    print("Final Concentration:", data[0][-1])
    print("Final Power:", data[1][-1])
    print("Final Reactor Kinetics Temperature:", data[2][-1])
    print("Final Solubility:", data[3][-1])
    print("Final Heat Exchanger 1 Temp:", data[4][-1])
    print("Final Heat Exchanger 2 Temp:", data[5][-1])