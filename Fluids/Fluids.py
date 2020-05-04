# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:42:40 2020

@author: Bjorn
"""

import math

from reynolds import Reynoldsnum
from major_head_loss import HlMajor
from minor_head_loss import HlMinor
import Chemistry as Chemistry


def function(fluidTempReactor, fluidTempHeatEx):
    '''
    Outputs pressure at several points in the system and mass flow after the reactor and after the heat exchanger
    '''
    #Constants
    g = 9.807 #m/s^2
    
    #Design of MSR
    #Assumed diameter of all connecting pipes (From MSRE)
    diameter = 0.1524 #m
    #Assumed volumetric flow rate (From MSRE)
    volFlowRate =  0.07571 #m^3/s
    fluidVelocity = volFlowRate/((diameter/2)**2*math.pi)

    fuelLoopDesign = [[0.0, 3.2],#1 First digit is height coordinate, second is length of pipe to next
                      [2.2, 0.0],#2
                      [2.2, 0.762],#3
                      [2.2, 0],#4
                      [1.7, 0.1],#5
                      [1.6, 0],#6
                      [0.1, 2.362],#7
                      [0.0, 0]]#8
    
    #array of fittings from that point to next
    fuelLoopFittings =[['90deg elbow, standard r'],#1
                       ['none'],#2
                       ['90deg elbow, standard r'],#3
                       ['none'],#4
                       ['none'],#5
                       ['none'],#6
                       ['90deg elbow, standard r','90deg elbow, standard r'],#7
                       ['none']]#8
        
    #Fluid properties as a function of temperature after the reactor(R) and heat exchanger (HE)
    densityR = Chemistry.primary_density(fluidTempReactor)*1000#kg/m^3
    densityHE = Chemistry.primary_density(fluidTempHeatEx)*1000#kg/m^3
    viscosityR = Chemistry.primary_viscosity(fluidTempReactor)/1000#Pa*s
    viscosityHE = Chemistry.primary_viscosity(fluidTempHeatEx)/1000#Pa*s
    ReynoldsR = Reynoldsnum(densityR, volFlowRate, diameter, viscosityR)
    ReynoldsHE = Reynoldsnum(densityHE,volFlowRate,diameter,viscosityHE)
 
    #Head loss
    #head of components in fuel loop
    pumpHead = 0#m  Initial number
    heatExchangerHead = -7.74#m
    #Purification System
    purificationDiameter = 0.9144#m
    purificationLength = 1.524#m
    purificationVel = volFlowRate/(math.pi*(purificationDiameter/2)**2)#m/s
    purEntranceHead = (1.1*(fluidVelocity-purificationVel)**1.92)/(2*g)#m
    purExitHead = (1/(math.pi*(purificationDiameter/2)**2/(math.pi*(diameter/2)**2)))
    ReynoldsPur = Reynoldsnum(densityHE,volFlowRate,purificationDiameter,viscosityHE)
    purificationSystemHead = -(purEntranceHead + purExitHead + HlMajor(purificationLength,purificationVel,purificationDiameter,ReynoldsPur))#m
    reactorHead = -0.3048*10**(-5)*(volFlowRate*15850.323)**2.01#m
    #First digit is major head loss from that point to next, second digit is minor head loss from that point to next,third is other head loss from that point to next 
    head = [[HlMajor(fuelLoopDesign[0][1],fluidVelocity,diameter,ReynoldsR), HlMinor(fluidVelocity,fuelLoopFittings[0]), 0],#1
            [0, 0, pumpHead],#2
            [HlMajor(fuelLoopDesign[2][1],fluidVelocity,diameter,ReynoldsR), HlMinor(fluidVelocity,fuelLoopFittings[2]), 0],#3
            [0, 0, heatExchangerHead],#4
            [HlMajor(fuelLoopDesign[4][1],fluidVelocity,diameter,ReynoldsHE), HlMinor(fluidVelocity, fuelLoopFittings[4]), 0],#5
            [0, 0, purificationSystemHead],#6
            [HlMajor(fuelLoopDesign[6][1],fluidVelocity,diameter,ReynoldsHE), HlMinor(fluidVelocity, fuelLoopFittings[6]), 0],#7
            [0, 0, reactorHead]]#8

    #Determine pump head requirements
    for i in range(len(head)):
        for j in range(3):
            pumpHead += head[i][j]            
    head[1][2] = -pumpHead

    #Pressure array
    pressure = []
    #initial pressure exiting the reactor core
    pressure.append(0.0)#pa
    #pressure array first cycles through items before the heat exchanger then after heat exchanger
    for i in range(1,8):
        if i<3:
            pressure.append(pressure[i-1]+densityR*g*(fuelLoopDesign[i][0]-fuelLoopDesign[i-1][0] + head[i][0] + head[i][1] + head[i][2]))
        else:
            pressure.append(pressure[i-1]+densityR*g*(fuelLoopDesign[i][0]-fuelLoopDesign[i-1][0] + head[i][0] + head[i][1] + head[i][2]))

    #Compute mass flow rate for after heat exchanger and after reactor 
    massFlowRateR = volFlowRate*densityR #After Reactor
    massFlowRateHE = volFlowRate*densityHE #After Heat Exchanger
    
    
    
    return [pressure, massFlowRateR, massFlowRateHE]

def coolant(fluidTempHot, fluidTempCold):
    '''
    Returns pressure and mass flow rates of the coolant loop using the hot and cold fluid temperatures
    '''
     #Constants
    g = 9.807 #m/s^2
    
    #Design of MSR
    #Assumed diameter of all connecting pipes (From MSRE)
    diameter = 0.1524 #m
    #Assumed volumetric flow rate (From MSRE)
    volFlowRate =  0.05363 #m^3/s
    fluidVelocity = volFlowRate/((diameter/2)**2*math.pi)

    fuelLoopDesign = [[0.0, 3.2],#1 First digit is height coordinate, second is length of pipe to next
                      [2.2, 0.0],#2
                      [2.2, 0.762],#3
                      [2.2, 0],#4
                      [1.7, 0.1],#5
                      [1.6, 0]]#6

    
    #array of fittings from that point to next
    fuelLoopFittings =[['90deg elbow, standard r'],#1
                       ['none'],#2
                       ['90deg elbow, standard r'],#3
                       ['none'],#4
                       ['none'],#5
                       ['none']]#6
        
    #Fluid properties as a function of temperature after the fuel/coolant (HE1) heat exchanger and the 
    densityHE1 = Chemistry.secondary_density(fluidTempHot)*1000#kg/m^3
    densityHE2 = Chemistry.secondary_density(fluidTempCold)*1000#kg/m^3
    viscosityHE1 = Chemistry.secondary_viscosity(fluidTempHot)/1000#Pa*s
    viscosityHE2 = Chemistry.secondary_viscosity(fluidTempCold)/1000#Pa*s
    ReynoldsHE1 = Reynoldsnum(densityHE1, volFlowRate, diameter, viscosityHE1)
    ReynoldsHE2 = Reynoldsnum(densityHE2,volFlowRate,diameter,viscosityHE2)
 
    #Head loss
    #head of components in coolant loop
    pumpHead = 0#m
    #Fuel/coolant heat exchanger
    heatExchanger1Head = -3.0#m
    #Heat exchanger for thermal power
    heatExchanger2Head = -3.0#m
    #First digit is major head loss from that point to next, second digit is minor head loss from that point to next,third is other head loss from that point to next 
    head = [[HlMajor(fuelLoopDesign[0][1],fluidVelocity,diameter,ReynoldsHE1), HlMinor(fluidVelocity,fuelLoopFittings[0]), 0],#1
            [0, 0, pumpHead],#2
            [HlMajor(fuelLoopDesign[2][1],fluidVelocity,diameter,ReynoldsHE1), HlMinor(fluidVelocity,fuelLoopFittings[2]), 0],#3
            [0, 0, heatExchanger2Head],#4
            [HlMajor(fuelLoopDesign[4][1],fluidVelocity,diameter,ReynoldsHE2), HlMinor(fluidVelocity, fuelLoopFittings[4]), 0],#5
            [0, 0, heatExchanger1Head]]#6
    
    #Determine pump head requirements
    for i in range(len(head)):
        for j in range(3):
            pumpHead += head[i][j]            
    head[1][2] = -pumpHead

    #Pressure array
    pressure = []
    #initial pressure exiting the reactor core
    pressure.append(0.0)#pa
    #pressure array first cycles through items before the heat exchanger then after heat exchanger
    for i in range(1,6):
        if i<3:
            pressure.append(pressure[i-1]+densityHE1*g*(fuelLoopDesign[i][0]-fuelLoopDesign[i-1][0] + head[i][0] + head[i][1] + head[i][2]))
        else:
            pressure.append(pressure[i-1]+densityHE2*g*(fuelLoopDesign[i][0]-fuelLoopDesign[i-1][0] + head[i][0] + head[i][1] + head[i][2]))
    
    #Comput mass flow rate for 
    massFlowRateHE1 = volFlowRate*densityHE1 #After Heat Exchanger 1
    massFlowRateHE2 = volFlowRate*densityHE2 #After Heat Exchanger 2
    
    return [pressure, massFlowRateHE1, massFlowRateHE2]
