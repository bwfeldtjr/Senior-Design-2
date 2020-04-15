import math

#Function for fuel Reynolds number
def Reynoldsnum(density, volumetricFlowRate, pipeDiameter, viscosity):

    '''
    Returns the Reynolds number for a flow in the pipe
    '''
    return 4*density*volumetricFlowRate/(pipeDiameter*math.pi*viscosity)
