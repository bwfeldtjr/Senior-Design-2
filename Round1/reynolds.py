# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:44:51 2020

@author: Brenden
"""

import math

#Function for fuel Reynolds number
def Reynoldsnum(density, volumetricFlowRate, pipeDiameter, viscosity):

    '''
    Returns the Reynolds number for a flow in the pipe
    '''
    return 4*density*volumetricFlowRate/(pipeDiameter*math.pi*viscosity)