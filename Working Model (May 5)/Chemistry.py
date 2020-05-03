"""
Spyder Editor

This is a temporary script file.
"""
import math

def primary_density(T):
    """ This function returns density of the fuel 
    mixture in g/cm^3, T must be in celsius """
    
    density = 2.38 - (40E-5) * T
    return density

def primary_viscosity(T):
    """ This function returns viscosity of the 
    fuel mixture in cP, T must be in celsius """
    
    viscosity = 8.4 
    return viscosity

def secondary_density(T): 
    """ This function returns density of the coolant 
    mixture in g/cm^3, T must be in celsius """
    
    density = 2.16 - (40E-5) * T
    return density

def secondary_viscosity(T):
    """ This function returns viscosity of the coolant 
    mixture in cP, T must be in celsius """
    
    T= T+273
    viscosity = 0.118 * math.exp(3624 / T) 
    return viscosity


def solubilitypercentage(T):
    """ This function takes a temperature and 
    returns the solubility of the fuel mixture 
    in decimal form 
    x = BeF2
    y = ZrF4
    z = UF4
    T must be in celcius """
    
    def solubility(w,x,y,z):
        solubility = 0.65 * w + 0.29 * x + 0.05 * y + 0.01 * z
        return solubility
    
    if T < 458:
        sol = solubility(0, 0, 0, 0)
        # print sol
    
    elif T < 560:
        sol = solubility(0, 1, 0, 0)  
        # print sol
    
    elif T < 910:
        sol = solubility(1, 1, 0, 0)
        # print sol
        
    elif T < 1035:
        sol = solubility(1, 1, 1, 0)
        # print sol
    
    else:
        sol = solubility(1, 1, 1, 1)
        # print sol
    return sol

if (__name__ == "__main__"):
    """Define inputs"""
    T = None
    data_fuel_density = primary_density(T)
    data_fuel_viscosity = primary_viscosity(T)
    data_coolant_density = secondary_density(T)
    data_coolant_viscosity = secondary_viscosity(T)
    data_solubility = solubilitypercentage(T)
    
    
    