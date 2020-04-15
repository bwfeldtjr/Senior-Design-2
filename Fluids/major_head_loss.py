# -*- coding: utf-8 -*-
"""
author: Bjorn Funk
"""
import math

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