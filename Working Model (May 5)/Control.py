"""
Created on Wed Apr  7 13:20:48 2020

@author: minim
"""

import numpy as np
import time as Time

""" IMPORT REACTOR MODULES """
import Chemistry
import Fluids
import Heat_Exchanger_1 as HXC1
import Heat_Exchanger_2 as HXC2
import Kinetics
import Purification

def Run_Sim(time):
    timer_start = Time.time()
    
    datapoints = time * 1440 # One datapoint every minute
    
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
    concentration = 1000000000
    concentration_factor = 0.001
    N = 100000
    i = 0

    
    # Simulation Iteration
    while i < datapoints:
        
        
        # Reactor Kinetics
        if i < 1:
            data[0][i] = concentration
        else:
            data[0][i] = concentration[0]
        rk_data = Kinetics.fun(HX2_Temp, concentration, N)
        rk_temperature = rk_data[0] # Celsius
        C_i = rk_data[1][0] # Concentration Array
        N = rk_data[2] # Neutron Population Array
        power = rk_data[3]/6000 # MW

        
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
        HX2_temp = HXC2.CounterFlowOutputs(mass_flow_rateR,
                                          mass_flow_rateHX,
                                          HX1_Temp,
                                          viscosity_fuel)

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
        N = purification_data[1]
        
        # Data Collection (UNFINISHED)
        data[1][i] = power
        data[2][i] = rk_temperature
        data[3][i] = solubility
        data[4][i] = HX1_Temp
        data[5][i] = HX2_Temp
        
        i = i + 1
    
    timer_end = Time.time()
    elapsed_time = timer_end - timer_start
    elapsed_time = round(elapsed_time, 2)
    print("Simulation ran in", elapsed_time, "seconds.")
    
    return data


if (__name__ == "__main__"):
    data = Run_Sim(1)
    print("Final Concentration:", round(data[0][-1], 2))
    print("Final Power:", round(data[1][-1], 2), "MW")
    print("Final Reactor Kinetics Temperature:", round(data[2][-1], 2), "C")
    print("Final Solubility:", round(data[3][-1]*100, 2), "%")
    print("Final Heat Exchanger 1 Temp:", round(data[4][-1], 2), "C")
    print("Final Heat Exchanger 2 Temp:", round(data[5][-1], 2), "C")