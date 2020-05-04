# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:18:18 2020

@author: cjh1_000
"""
"""
temp
cp  
visc=mu 
pr 
k 
"""

"""
EVERYTHING IN SI UNITS
"""

import math
import numpy as np


"""
I used reynolds number to find the Nu for hot and cold fuild then used the effectivness to find the final Temp of both the fuel and the coolant.
These reynolds numbers will change equations if the same shell and tube heat exchanger is not used.
if different heat exchanger is used just switch the reynolds number equations and then code should work as intended.

"""      
    
def CounterFlowOutputs(MassFlowRateHot, MassFlowRateCold, Fuel_Temp, mu_fuel):
    
    """Temp of coolant in C"""
    temp_cool = 455

    """Cp of coolant"""
    cp_cool = 976.78 + 1.0634 * temp_cool
    
    """Pr of coolant"""
    pr_cool = 5.938
    
    """mu of coolant"""
    mu_cool = (4*10**-5)*math.exp(4170/temp_cool)
    
    """k of coolant"""
    k_cool = 0.36 + (5.6 * 10**-4) * temp_cool
    
    # """Volumetric flow of coolant"""
    # vf = 850 * .0000631
    
    """Cp of fuel"""
    cp_fuel = 1967.79
    
    """Pr of fuel"""
    pr_fuel = 12.65
    
    """ K of fuel """
    k_fuel = 1.4
    
    """Inner diameter of the inner pipe in meters"""
    D1 = 10 
    
    """Outer diameter of the inner pipe in meters"""
    D2 = 12
     
    """Inner diameter of the outer pipe in meters"""
    D3 = 20
     
    """Length of heat exchanger in meters"""
    L = 3
    
    

    ReynoldsHot = (4.0*MassFlowRateHot)/(math.pi*D1*mu_fuel)
    ReynoldsCold = (4.0*MassFlowRateCold)/(math.pi*(D3+D2)*mu_cool)
    

    
    NuCold = 0
    NuHot = 0
    
    if(ReynoldsHot >= 4000 and ReynoldsCold >= 4000):
        NuHot = 0.023*(ReynoldsHot**(4/5))*(pr_fuel**(0.3))
        NuCold = 0.023*(ReynoldsCold**(4/5))*(pr_cool**(0.4))
    elif(ReynoldsHot <= 4000 and ReynoldsCold >= 4000):
        NuHot = 3.66 + ((0.668*(D1/L)*ReynoldsHot*pr_fuel)/(1+(0.04*((D1/L)*ReynoldsHot*pr_fuel)**(2/3))))
        NuCold = 0.023*(ReynoldsCold**(4/5))*(pr_cool**(0.4))
    elif(ReynoldsHot <= 4000 and ReynoldsCold <= 4000):
        NuHot = 3.66 + ((0.668*(D1/L)*ReynoldsHot*pr_fuel)/(1+(0.04*((D1/L)*ReynoldsHot*pr_fuel)**(2/3))))
        NuCold = 3.66 + ((0.668*(D1/L)*ReynoldsCold*pr_cool)/(1+(0.04*((D1/L)*ReynoldsCold*pr_cool)**(2/3))))
    elif(ReynoldsHot >= 4000 and ReynoldsCold <= 4000):
        NuHot = 0.023*(ReynoldsHot**(4/5))*(pr_fuel**(0.3))
        NuCold = 3.66 + ((0.668*(D1/L)*ReynoldsCold*pr_cool)/(1+(0.04*((D1/L)*ReynoldsCold*pr_cool)**(2/3))))
    else:
        print("Error")
        
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
    TcOut= temp_cool + (effectiveness*Cmin*(Fuel_Temp-temp_cool)/(MassFlowRateMin*cpmin))
    q = Cc*(TcOut-temp_cool)
    TfOut = Fuel_Temp - (q/Ch)
    #TfOutC = TfOut - 273.15
        
    return TfOut   

if (__name__ == "__main__"):
    """Define Inputs"""
    MassFlowRateHot = None
    MassFlowRateCold = None
    Fuel_Temp = None
    mu_fuel = None
    data = CounterFlowOutputs(MassFlowRateHot, MassFlowRateCold, Fuel_Temp, mu_fuel)