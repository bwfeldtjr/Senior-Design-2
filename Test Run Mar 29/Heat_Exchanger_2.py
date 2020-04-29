# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:09:39 2020

@author: cjh1_000
"""
"""
ALL UNITS IN SI
"""

import math 
import numpy as np

"""
I used reynolds number to find the Nu for hot and cold fuild then used the effectivness to find the final Temp of both the fuel and the coolant.
These reynolds numbers will change equations if the same shell and tube heat exchanger is not used.
if different heat exchanger is used just switch the reynolds number equations and then code should work as intended.

"""      

    
def CounterFlowOutputs(MassFlowRateHot, MassFlowRateCold, HX1_Temp, mu_fuel):
    """Cp of coolant"""
    cp_cool = 1046.7
    
    """Pr of coolant"""
    pr_cool = 11.8
    
    """Temp of coolant in C"""
    temp_cool = 390
    
    """mu of coolant"""
    mu_cool = .0159*math.exp(3179/(temp_cool+273))
    
    """k of coolant"""
    k_cool = .45
    
    """density of coolant"""
    p = 2800
    
    """Volumetric flow of coolant"""
    vf = 850 * .0000631
    
    """Cp of fuel"""
    cp_fuel = 1967.79
    
    """Pr of fuel """
    pr_fuel = 12.65
    
    """ K of fuel"""
    k_fuel = 1.4
    
    """inner diameter of the inner pipe in inches"""
    D1 = 10 
    
    """outer diameter of the inner pipe in inches"""
    D2 = 12 
    
    """inner diameter of the outer pipe in inches"""
    D3 = 20 
    
    """Length of heat exchanger in meters"""
    L = 40

    
    ReynoldsHot = (4.0*MassFlowRateHot)/(math.pi*D1*mu_fuel)
    ReynoldsCold = (4.0*MassFlowRateCold)/(math.pi*(D3+D2)*mu_cool)
    NuCold = 0
    NuHot = 0
    if(ReynoldsHot > 4000 and ReynoldsCold > 4000):
        NuHot = 0.023*(ReynoldsHot**(4/5))*(pr_fuel**(0.3))
        NuCold = 0.023*(ReynoldsCold**(4/5))*(pr_cool**(0.4))
    elif(ReynoldsHot < 4000 and ReynoldsCold > 4000):
        NuHot = 3.66 + ((0.668*(D1/L)*ReynoldsHot*pr_fuel)/(1+(0.04*((D1/L)*ReynoldsHot*pr_fuel)**(2/3))))
        NuCold = 0.023*(ReynoldsCold**(4/5))*(pr_cool**(0.4))
    elif(ReynoldsHot < 4000 and ReynoldsCold < 4000):
        NuHot = 3.66 + ((0.668*(D1/L)*ReynoldsHot*pr_fuel)/(1+(0.04*((D1/L)*ReynoldsHot*pr_fuel)**(2/3))))
        NuCold = 3.66 + ((0.668*(D1/L)*ReynoldsCold*pr_cool)/(1+(0.04*((D1/L)*ReynoldsCold*pr_cool)**(2/3))))
    elif(ReynoldsHot > 4000 and ReynoldsCold < 4000):
        NuHot = 0.023*(ReynoldsHot**(4/5))*(pr_fuel**(0.3))
        NuCold = 3.66 + ((0.668*(D1/L)*ReynoldsCold*pr_cool)/(1+(0.04*((D1/L)*ReynoldsCold*pr_cool)**(2/3))))
    
    else:
        print("Error")
        

    """
    All code below will not change with a change in the heat exchanger
    """
    
    hCold = (NuCold*k_cool)/(D3-D2)
    hHot = (NuHot*k_fuel)/D1
    Ai = math.pi*D1*L
    Ao = math.pi*D3*L
    log = np.log(D2/D1)
    Rtot= ((1/(hHot*Ai)) + (1/(hCold*Ao))) + (log/(2*math.pi*237*L))
    UA = 1/Rtot
    Ch = MassFlowRateHot*cp_fuel
    Cc = MassFlowRateCold*cp_cool
    Cmin = 0 
    Cmax = 0
    if Ch < Cc:
        Cmin = Ch
        Cmax = Cc
        MassFlowRateMin = MassFlowRateHot
        cpmin = cp_fuel
    else:
        Cmin = Cc
        Cmax = Ch
        MassFlowRateMin = MassFlowRateCold
        cpmin = cp_cool
    
    """Calculation of effectiveness and Tout"""
    Cr = Cmin/Cmax
    NTU = UA/Cmin
    e = math.exp(-NTU*(1-Cr))
    effectiveness = (1-e)/(1-(Cr*e))
    Tc2Out= temp_cool + (effectiveness*Cmin*(HX1_Temp-temp_cool)/(MassFlowRateMin*cpmin))
    q = Cc*(Tc2Out-temp_cool)
    Tf2Out = HX1_Temp - (q/Ch)
    #Tf2OutC = Tf2Out - 273.15
    #Tc2OutC = Tc2Out - 273.15
    power = None # Power calculation goes here
        
    return Tf2Out, power
