# -*- coding: utf-8 -*-
"""
author: Bjorn Funk
"""
import math

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
    i = 0
    
    for i in range(len(fittings)):
        kValue += kVals[fittings[i]]
    
    return kValue*fluidVelocity**2/(2*g)