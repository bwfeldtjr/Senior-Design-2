# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:35:46 2020

@author: Brenden
"""
#Assuming constant flux in a homogenous medium
#Big thing left to do is get temperature dependence for cross sections figured out

import numpy as np
import math
import matplotlib.pyplot as mp
import pandas as pd
import time
t1 = time.time()

#User inputs/Inputs from other modules
Diam = 10 #Diameter of Fuel Rod (cm)
vol = 8*2.5**2*math.pi*28316.8
volF = vol*.1 #Volume of Fuel (cm^3)
volM = vol*.9 #Volume of Moderator (cm^3)

dens = 6.7 #g/cm^3
dt = 0.01 #Time Step (given by user)
betai = np.array([[0.000215,0.001424,0.001274,0.002568,0.000748,0.000273]])
lambdai = np.array([[0.0124,0.0305,0.111,0.301,1.14,3.01]])

#Constants
ava = 6.022*10**23
atnum = 314
beta = 0.0065 #Effective Delayed Neutron Fraction
cLamda = 0.0001 #Prompt Neutron Life
v = 2.42 #Number of Neutrons produced per Fission

Temp1 = [0]*10**4
rho1 = [0]*10**4
k1 = [0]*10**4
power1 = [0]*10**4
for i in range(len(Temp1)):
    T0 = 293 #K (Reference Temp)
    if i ==0:
        T1 = 1300 #K (Actual Temp)
        n_pop = 10**10 #Neutron Population (to be determined)
        con = 10**10 #Concentration of Precursor (to be determined)
    else:
        T1 = Temp1[i-1]
        n_pop = newn  #Neutron Population (to be determined)
        con = newcon #Concentration of Precursor (to be determined)
    corr = math.sqrt(T0/T1) #Temperature correction factor for all cross sections (Assuming in 1/v region)

    UsigF = 585.1*corr #barns From https://wwwndc.jaea.go.jp/cgi-bin/Tab80WWW.cgi?lib=J40&iso=U235
    UsigG = 98.71*corr #barns 
    UsigA = (UsigF+UsigG)*corr
    UsigS = (698.9-UsigA)*corr
    
    BesigS = 0.023/.207*corr #Scattering Cross section for Berrylium (cm-1)
    BesigA = BesigS/144*.207*corr #Absorption Cross section for Berrylium (cm-1)
    
    LisigS = 0.041/.261*corr #Scattering Cross section for Lithium (cm-1)
    LisigA = LisigS/6*.261*corr #Absorption Cross section for Lithium (cm-1)
    
    FsigS = 0.018/0.102*corr #Scattering Cross section for Fluorine (cm-1)
    FsigA = FsigS/39*.102*corr #Absorption Cross section for Fluorine (cm-1)
    
    numdens = dens*ava/atnum
    
    eta = v*UsigF/(UsigA) #Eta is reproduction factor (average number of neutrons produced per fission) 
    I_eff = 4.45+26.6*math.sqrt(4/dens/Diam)
    p = math.exp(-2.73/((0.207+0.261+0.102)/3)*(ava/(ava*FsigA+numdens*UsigA))**0.514)   #Resonance Escape Probability (from https://www.nrc.gov/docs/ML1214/ML12142A089.pdf)
    f = UsigA*10**-24*numdens/(BesigA+LisigA+FsigA+UsigA*10**-24*numdens) #Thermal Utilization Factor
    epsilon = 1 #Fast Fission Factor (Assuming homogeneous core)
    
    k = 1+eta*p*f*epsilon #Multiplication Factor
    rho = (k-1)/k #Reactivity related to Multiplicaiton factor
    rho1[i]=rho
    k1[i]=k
    
#    if i < 2:
#        k = 1+eta*p*f*epsilon #Multiplication Factor
#        rho = (k-1)/k #Reactivity related to Multiplicaiton factor
#        rho1[i]=rho
#        k1[i]=k
#    else:
#        if Temp1[i-2]<Temp1[i-1]:
#            k = k1[i-1]-eta*p*f*epsilon #Multiplication Factor
#            rho = (k-1)/k #Reactivity related to Multiplicaiton factor
#            rho1[i]=rho
#            k1[i]=k
#        else:
#            k = k1[i-1]+eta*p*f*epsilon #Multiplication Factor
#            rho = (k-1)/k #Reactivity related to Multiplicaiton factor
#            rho1[i]=rho
#            k1[i]=k
            
    flux = n_pop * 220000
    power = flux*numdens*UsigF*10**-24*200*1.0622*10**-19 #MJ/cm^3 (200 MeV per fission assumed) Thermal Power per volume
    power1[i]=power
    heat = power*(volF+volM) #Heat added
    #Table 1 of 3
    #Table 1 The slow-down properties for Flibe (67%LiF–33%BeF2). The Σs is macroscopic scattering cross section and Σa is macroscopic absorption cross section
    #Materials   	Lethargyξ	    ξΣs (cm−1)	   ξΣs/Σa
    #Graphite	     0.158	         0.065         	223
    #H2O	         0.927	         1.265	        57
    #D2O	         0.510	         0.177	        3400
    #Be metal	     0.207	         0.153	        144
    #Be in Flibe	 0.207	         0.023	        144
    #Li in Flibe	 0.261	         0.041          6
    #F in Flibe	     0.102	         0.018	        39
    
    
    #Precursor Group Info for Uranium-235 Source: Keepin, G. R., Physics of Nuclear Kinetics. Addison-Wesley, 1965.
    #Precursor Group	    λi	         βi
    #1	                 0.0124	  0.000215
    #2	                 0.0305	  0.001424
    #3	                 0.111	  0.001274
    #4	                 0.301	  0.002568
    #5	                 1.14	  0.000748
    #6	                 3.01     0.000273
    
#    betai = np.array([[0.000215,0.001424,0.001274,0.002568,0.000748,0.000273]])
#    lambdai = np.array([[0.0124,0.0305,0.111,0.301,1.14,3.01]])
    
    
    dc = dt*(betai/cLamda*n_pop-lambdai*con)
    dn = dt*((rho-beta)/cLamda*n_pop+np.sum(dc*lambdai)) 
    
    newcon = con+dc
    newn = n_pop+dn
    
    dTT = heat/1.4/(volF+volM)
    newT = T1+dTT
    Temp1[i]=newT

    
t2 = time.time()
print('Time to run: '+str(t2-t1)+' seconds')

def fun(x):
    return Temp1[-1]
