# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:02:03 2020

@author: Bjorn Funk
"""

import math

#should be a function of temperature
def density():
    return 1549.0 #kg/m^3

#Should be a function of temperature
def viscosity():
    return 0.009 #Pa*s(Kg/ms). from MSRE Viscosity of fuel

def Reynoldsnum(density, volumetricFlowRate, pipeDiameter, viscosity):

    '''
    Returns the Reynolds number for a flow in the pipe
    '''
    return 4*density*volumetricFlowRate/(pipeDiameter*math.pi*viscosity)



def HlMajor(pipeLength, fluidVelocity, diameter, Reynolds):
    '''
    Returns major head loss
    ''' 
    g = 9.807 #/s^2
    f = 0.1 #Initial uess of friction factor
    error = 1 #Initial error estimate
    kRough = 0.0001 #Surface Roughness of interior of pipes. Number based on steel, mortar lined (find better estimate)

    
    #Friction factor determination. Laminar flow below Re<2300 and Turbulent flow Re>2300
    if Reynolds<2300:        
        #Laminar friction factor
        f = 64/Reynolds

    else:
        #Turbulent flow assumed to be a good estimate
        #Iterate colebrook equation to determine friction factor for turbulent
        while abs(error) > 0.00000001:
            error = f-(-2*math.log10(kRough/(3.72*diameter)+2.51/(Reynolds*math.sqrt(f))))**(-2)
            f = f - error
    
    return -f * pipeLength * fluidVelocity**2 /(diameter * 2 * g)
    
def HlMinor(fluidVelocity,fittings = ['none']):
    
    '''
    Returns minor head loss
    
    Fitting inputs:
      tee, as elbow 
      tee, branching flow
      tee, run through
      180deg bend
      90deg elbow, long r
      90deg elbow, standard r
      gate valve, fully open
      gate valve, 3/4 open
      gate valve, 1/2 open
      gate valve, 1/4 open
      plug disk, fully open
      plug disk, 3/4 open
      plug disk, 1/2 open
      plug disk, 1/4 open
      butterfly valve, 5deg
      butterfly valve, 10deg
      butterfly valve, 20deg
      butterfly valve, 40deg
      butterfly valve, 60deg
    '''
    kValue = 0.0
    g = 9.807
    
    kVals =  {'none': 0.0,
              'tee, as elbow': 1.0, 
              'tee, branching flow': 1.0, 
              'tee, run through': 0.4, 
              '180deg bend': 1.5, 
              '90deg elbow, long r': 0.2, 
              '90deg elbow, standard r': 0.35,
              'gate valve, fully open': 0.17,
              'gate valve, 3/4 open': 0.9,
              'gate valve, 1/2 open': 4.5,
              'gate valve, 1/4 open': 24.0,
              'plug disk, fully open': 9,
              'plug disk, 3/4 open': 13,
              'plug disk, 1/2 open': 36,
              'plug disk, 1/4 open': 112,
              'butterfly valve, 5deg': 0.24,
              'butterfly valve, 10deg': 0.52,
              'butterfly valve, 20deg': 1.54,
              'butterfly valve, 40deg': 10.8,
              'butterfly valve, 60deg': 118}
    #FINISH FINDING k FOR ALL VALUES
    
    for i in range(len(fittings)):
        kValue += kVals[fittings[i]]
    
    return kValue*fluidVelocity**2/(2*g)
    


def fluidDynamics(densityofFluid, viscosityofFluid):
    '''
    Outputs pressure at points in system
    '''
    #Assumed volumetric flow rate
    volFlowRate =  0.00336 #m^3/s
    #Assumed diameter of all connecting pipes
    diameter = 0.1524 #m

    g = 9.807 #m/s^2
    fluidVelocity = volFlowRate/((diameter/2)**2*math.pi)
    Re = Reynoldsnum(density(),volFlowRate,diameter,viscosity())
    
    #initial pressure exiting the reactor core (Look up)
    pressure = []
    pressure.append(0.0)#pa
    
    #FINISH UP FINAL SIZE DESIGN FOR THIS
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
    
    #GET BETTER ESTIMATES OF THESE HEADS
    #head of components in fuel loop
    pumpHead = 14.33
    heatExchangerHead = -3.0
    purificationSystemHead = -1.0
    reactorHead = -3.0
    
    #CHANGE VISCOSITY AND DENSITY FUNCTIONS OF TEMPERATURE
    #Hl is head losses. First digit is major head loss from that point to next, second digit is minor head loss from that point to next,third is other head loss from that point to next 
    head = [[HlMajor(fuelLoopDesign[0][1],fluidVelocity,diameter,Reynoldsnum(density(),volFlowRate,diameter,viscosity())), HlMinor(fluidVelocity,fuelLoopFittings[0]), 0],#1
            [0, 0, pumpHead],#2
            [HlMajor(fuelLoopDesign[2][1],fluidVelocity,diameter,Reynoldsnum(density(),volFlowRate,diameter,viscosity())), HlMinor(fluidVelocity,fuelLoopFittings[2]), 0],#3
            [0, 0, heatExchangerHead],#4
            [HlMajor(fuelLoopDesign[4][1],fluidVelocity,diameter,Reynoldsnum(density(),volFlowRate,diameter,viscosity())), HlMinor(fluidVelocity, fuelLoopFittings[4]), 0],#5
            [0, 0, purificationSystemHead],#6
            [HlMajor(fuelLoopDesign[6][1],fluidVelocity,diameter,Reynoldsnum(density(),volFlowRate,diameter,viscosity())), HlMinor(fluidVelocity, fuelLoopFittings[6]), 0],#7
            [0, 0, reactorHead]]#8
    
    #pressure array
    for i in range(1,8):
        #CHANGE SO THAT DENSITY WILL BE CHANGED AS TEMPERATURE IS CHANGED
        pressure.append(pressure[i-1]+density()*g*(fuelLoopDesign[i][0]-fuelLoopDesign[i-1][0] + head[i][0] + head[i][1] + head[i][2]))
    
    
    return pressure
        
            
        
        
        
        
        
        