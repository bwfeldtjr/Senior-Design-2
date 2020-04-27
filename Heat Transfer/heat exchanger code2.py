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

"""Cp of coolant"""
x = 1046.7

"""Pr of coolant"""
z = 11.8

"""Temp of coolant in C"""
T = 390

"""mu of coolant"""
y = .0159*math.exp(3179/(T+273))

"""k of coolant"""
w = .45

"""density of coolant"""
p = 2800

"""Volumetric flow of coolant"""
vf = 850 * .0000631



"""Cp of fuel"""
xx = 1967.79


"""Pr of fuel """
zz = 12.65


import heatexchangercode1 as h1
"""Temp of fuel set by user"""
TT = h1.TfoutC


import viscfuel as muf
"""mu of fuel taken from chemisty"""
yy = muf.fun('mu')


""" K of fuel"""
ww = 1.4



import fluiddynamics as fd
"""Mass flow rate of fuel taken from fluid dynamics"""
MassFlowRateHot = fd.coolant('m') 

""" Mass flow rate of coolant= denisty * volumetric flow rate"""
MassFlowRateCold = p * vf
 
"""inner diameter of the inner pipe in inches"""
D1 = 10 

"""outer diameter of the inner pipe in inches"""
D2 = 12 

"""inner diameter of the outer pipe in inches"""
D3 = 20 

"""Length of heat exchanger in meters"""
L = 40


"""
I used reynolds number to find the Nu for hot and cold fuild then used the effectivness to find the final Temp of both the fuel and the coolant.
These reynolds numbers will change equations if the same shell and tube heat exchanger is not used.
if different heat exchanger is used just switch the reynolds number equations and then code should work as intended.

"""      

    
def CounterFlowOutputs(MassFlowRateHot, MassFlowRateCold, D1, D2, D3):
    ReynoldsHot = (4.0*MassFlowRateHot)/(math.pi*D1*yy)
    ReynoldsCold = (4.0*MassFlowRateCold)/(math.pi*(D3+D2)*y)
    NuCold = 0
    NuHot = 0
    if(ReynoldsHot > 4000 and ReynoldsCold > 4000):
        NuHot = 0.023*(ReynoldsHot**(4/5))*(zz**(0.3))
        NuCold = 0.023*(ReynoldsCold**(4/5))*(z**(0.4))
    elif(ReynoldsHot < 4000 and ReynoldsCold > 4000):
        NuHot = 3.66 + ((0.668(D1/L)*ReynoldsHot*zz)/(1+(0.04((D1/L)*ReynoldsHot*zz)**(2/3))))
        NuCold = 0.023*(ReynoldsCold**(4/5))*(z**(0.4))
    elif(ReynoldsHot < 4000 and ReynoldsCold < 4000):
        NuHot = 3.66 + ((0.668(D1/L)*ReynoldsHot*zz)/(1+(0.04((D1/L)*ReynoldsHot*zz)**(2/3))))
        NuCold = 3.66 + ((0.668(D1/L)*ReynoldsCold*z)/(1+(0.04((D1/L)*ReynoldsCold*z)**(2/3))))
    elif(ReynoldsHot > 4000 and ReynoldsCold < 4000):
        NuHot = 0.023*(ReynoldsHot**(4/5))*(zz**(0.3))
        NuCold = 3.66 + ((0.668(D1/L)*ReynoldsCold*z)/(1+(0.04((D1/L)*ReynoldsCold*z)**(2/3))))
    
    else:
        print("Error")
    return NuCold, NuHot, MassFlowRateHot, MassFlowRateCold, D1, D2, D3   

temp = CounterFlowOutputs(MassFlowRateHot, MassFlowRateCold, D1, D2, D3) 

"""
All code below will not change with a change in the heat exchanger
"""

NuCold = temp[0]
NuHot = temp[1]
MassFlowRateHot = temp[2]
MassFlowrateCold = temp[3]
hCold = (NuCold*w)/(D3-D2)
hHot = (NuHot*ww)/D1
Ai = math.pi*D1*L
Ao = math.pi*D3*L
log = np.log(D2/D1)
Rtot= ((1/(hHot*Ai)) + (1/(hCold*Ao))) + (log/(2*math.pi*237*L))
UA = 1/Rtot
Ch = MassFlowRateHot*xx
Cc = MassFlowRateCold*x
Cmin = 0 
Cmax = 0
if Ch < Cc:
    Cmin = Ch
    Cmax = Cc
    MassFlowRateMin = MassFlowRateHot
    cpmin = xx
else:
    Cmin = Cc
    Cmax = Ch
    MassFlowRateMin = MassFlowRateCold
    cpmin = x
    
Tc = T
"""Input Temp Cold"""
Th = TT 
"""Input temp hot"""

"""Calculation of effectiveness and Tout"""
Cr = Cmin/Cmax
NTU = UA/Cmin
e = math.exp(-NTU*(1-Cr))
effectiveness = (1-e)/(1-(Cr*e))
Tc2Out= Tc + (effectiveness*Cmin*(Th-Tc)/(MassFlowRateMin*cpmin))
q = Cc*(Tc2Out-Tc)
Tf2Out = Th - (q/Ch)
Tf2OutC = Tf2Out - 273.15
Tc2OutC = Tc2Out - 273.15

print("The heat exchange rate, q = " ,q, "J/s")
print("Output temperature of coolant is ", Tc2Out, "K", " or ", Tc2OutC, "C")
print("Output temperature of fuel is ", Tf2Out, "K", " or ", Tf2OutC, "C")
