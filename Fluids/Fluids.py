# -*- coding: utf-8 -*-
"""
author: Bjorn Funk
"""

import math

from reynolds import Reynoldsnum
from major_head_loss import HlMajor
from minor_head_loss import HlMinor
import Chemistry


def function(fluidTempReactor, fluidTempHeatEx):
    '''
    Outputs pressure at several points in the system and mass flow after the reactor and after the heat exchanger
    '''
    #Constants
    g = 9.807 #m/s^2
    
    #FINISH UP FINAL SIZE and FITTING DESIGN FOR THIS
    #Design of MSR
    #Assumed diameter of all connecting pipes (From MSRE)
    diameter = 0.1524 #m
    #Assumed volumetric flow rate (From MSRE)
    volFlowRate =  0.00336 #m^3/s
    fluidVelocity = volFlowRate/((diameter/2)**2*math.pi)

    fuelLoopDesign = [[0, 1],#1 First digit is height coordinate, second is length of pipe to next
                      [1, 0],#2
                      [1, 100],#3
                      [1, 0],#4
                      [1, 4],#5
                      [-3, 0],#6
                      [-3, 1],#7
                      [-2, 1]]#8
    
    #FINISH UP WHAT FITTINGS WILL BE IN THIS DESIGN, ADD T FITTINGS FOR FREEZEPLUG
    #array of fittings from that point to next
    fuelLoopFittings =[['90deg elbow, standard r'],#1
                       ['none'],#2
                       ['90deg elbow, standard r'],#3
                       ['none'],#4
                       ['90deg elbow, long r'],#5
                       ['none'],#6
                       ['none'],#7
                       ['none']]#8
        
    #Fluid properties as a function of temperature
    densityR = Chemistry.primary_density(fluidTempReactor)*1000#kg/m^3
    densityHE = Chemistry.primary_density(fluidTempHeatEx)*1000#kg/m^3
    viscosityR = Chemistry.primary_viscosity(fluidTempReactor)/1000#Pa*s
    viscosityHE = Chemistry.primary_viscosity(fluidTempHeatEx)/1000#Pa*s
    ReynoldsR = Reynoldsnum(densityR, volFlowRate, diameter, viscosityR)
    ReynoldsHE = Reynoldsnum(densityHE,volFlowRate,diameter,viscosityHE)
 
    #GET BETTER ESTIMATES OF THESE HEADS
    #Head loss
    #head of components in fuel loop
    pumpHead = 14.33#m
    heatExchangerHead = -3.0#m
    purificationSystemHead = -1.0#m
    reactorHead = -3.0#m
    #First digit is major head loss from that point to next, second digit is minor head loss from that point to next,third is other head loss from that point to next 
    head = [[HlMajor(fuelLoopDesign[0][1],fluidVelocity,diameter,ReynoldsR), HlMinor(fluidVelocity,fuelLoopFittings[0]), 0],#1
            [0, 0, pumpHead],#2
            [HlMajor(fuelLoopDesign[2][1],fluidVelocity,diameter,ReynoldsR), HlMinor(fluidVelocity,fuelLoopFittings[2]), 0],#3
            [0, 0, heatExchangerHead],#4
            [HlMajor(fuelLoopDesign[4][1],fluidVelocity,diameter,ReynoldsHE), HlMinor(fluidVelocity, fuelLoopFittings[4]), 0],#5
            [0, 0, purificationSystemHead],#6
            [HlMajor(fuelLoopDesign[6][1],fluidVelocity,diameter,ReynoldsHE), HlMinor(fluidVelocity, fuelLoopFittings[6]), 0],#7
            [0, 0, reactorHead]]#8
    
    #Pressure array
    pressure = []
    #FIND BETTER INITIAL PRESSURE
    #initial pressure exiting the reactor core
    pressure.append(0.0)#pa
    #pressure array first cycles through items before the heat exchanger then after heat exchanger
    for i in range(1,8):
        if i<3:
            pressure.append(pressure[i-1]+densityR*g*(fuelLoopDesign[i][0]-fuelLoopDesign[i-1][0] + head[i][0] + head[i][1] + head[i][2]))
        else:
            pressure.append(pressure[i-1]+densityHE*g*(fuelLoopDesign[i][0]-fuelLoopDesign[i-1][0] + head[i][0] + head[i][1] + head[i][2]))
    
    #Comput mass flow rate for 
    massFlowRateR = volFlowRate*densityR
    massFlowRateHE = volFlowRate*densityHE
    
    return pressure, massFlowRateR, massFlowRateHE
        
            
        
        
        
        
        
        