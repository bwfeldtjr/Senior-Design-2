# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:09:39 2020

@author: cjh1_000
"""
"""
temp
cp  
visc=mu 
pr 
k 
"""

import math 
import numpy as np


x = 1046.7

z = 11.8

T = 390

y = .0159*math.exp(3179/(T+273))

w = .45

p = 2800

vf = 850 * .0000631

"""Cp"""
xx = 1967.79


"""Pr"""
zz = 12.65


import heatexchangercode1 as h1

TT = h1.Tfout


import viscfuel as muf

yy = muf.fun('mu')


""" K """
ww = 1.4



import fluiddynamics as fd

MassFlowRateHot = fd.fun('m') 


MassFlowRateCold = p * vf
 

D1 = 10 

D2 = 12 

D3 = 20 

L = 40


"""
def PropertiesCold(T):
    a = x
    b = y    
    c = z      
    d = w      
    return a, b, c, d
    print(" ")                   
    print("Properties of coolant: ")       
    print("Specific Heat, Cp = ", a , " J/kg*K")
    print("Dynamic Viscosity, mu = " , b, " N*s/m^2")
    print("Prandtl Number, Pr = ", c)
    print("Thermal Conductivity, k = ", d, " W/m*K")
    print(" ")


    
    
def PropertiesFuel(TT):
    e = xx
    f = yy
    g = zz
    h = ww
    return e, f, g, h
    print("Properties of fuel ")       
    print("Specific Heat, Cp = ", e, " J/kg*k")
    print("Dynamic Viscosity, mu = " , f, " N*s/m^2")
    print("Prandtl Number, Pr = ", g)
    print("Thermal Conductivity, k = ", h, " W/m*K")
    print(" ")
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
"""do i need to put Nucold and Nuhot in this """

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