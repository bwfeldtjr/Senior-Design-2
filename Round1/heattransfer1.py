# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:45:07 2020

@author: Brenden
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

"""Temp of coolant in C"""
T = 455

"""Cp of coolant"""
x = 976.78 + 1.0634 * T

"""Pr of coolant"""
z = 5.938

"""mu of coolant"""
y = (4*10**-5)*math.exp(4170/T)

"""k of coolant"""
w = 0.36 + (5.6 * 10**-4) * T

"""density of coolant"""
p = 2020

"""Volumetric flow of coolant"""
vf = 850 * .0000631

"""Cp of fuel"""
xx = 1967.79


"""Pr of fuel"""
zz = 12.65


import kinetics as tempf
"""Temp of fuel set by user"""
TT = tempf.fun('temp')


import chemistry as c
"""mu of fuel taken from chemisty"""
yy = c.primary_viscosity(TT)

""" K of fuel """
ww = 1.4


import Fluids as fd
"""Mass flow rate of fuel taken from fluid dynamics"""
MassFlowRateHot = fd.function(TT,TT)[1]


""" Mass flow rate of coolant= denisty * volumetric flow rate"""
MassFlowRateCold = p * vf

"""inner diameter of the inner pipe in meters"""
D1 = 10 

"""outer diameter of the inner pipe in meters"""
D2 = 12
 
"""inner diameter of the outer pipe in meters"""
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
        NuHot = 3.66 + ((0.668*(D1/L)*ReynoldsHot*zz)/(1+(0.04*((D1/L)*ReynoldsHot*zz)**(2/3))))
        NuCold = 0.023*(ReynoldsCold**(4/5))*(z**(0.4))
    elif(ReynoldsHot < 4000 and ReynoldsCold < 4000):
        NuHot = 3.66 + ((0.668*(D1/L)*ReynoldsHot*zz)/(1+(0.04*((D1/L)*ReynoldsHot*zz)**(2/3))))
        NuCold = 3.66 + ((0.668*(D1/L)*ReynoldsCold*z)/(1+(0.04*((D1/L)*ReynoldsCold*z)**(2/3))))
    elif(ReynoldsHot > 4000 and ReynoldsCold < 4000):
        NuHot = 0.023*(ReynoldsHot**(4/5))*(zz**(0.3))
        NuCold = 3.66 + ((0.668*(D1/L)*ReynoldsCold*z)/(1+(0.04*((D1/L)*ReynoldsCold*z)**(2/3))))
    
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
TcOut= Tc + (effectiveness*Cmin*(Th-Tc)/(MassFlowRateMin*cpmin))
q = Cc*(TcOut-Tc)
TfOut = Th - (q/Ch)
TfOutC = TfOut - 273.15
TcOutC = TcOut - 273.15

print("The heat exchange rate, q = " ,q, "J/s")
print("Output temperature of coolant is ", TcOut, "K", " or ", TcOutC, "C")
print("Output temperature of fuel is ", TfOut, "K", " or ", TfOutC, "C")

def fun():
    return TfOutC