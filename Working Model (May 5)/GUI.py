"""
Created on Wed Apr  7 12:22:08 2020

@author: minim
"""

# Standard Imports
import tkinter
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

# Module Imports
import Control
import Chemistry

#Global Variables
global time
time = None


# Creates and saves Temperature VS Time Graph
def Concentration_Graph(concentration, time):
    
    x_ticks_len = len(time)/280
    x_ticks = np.arange(0,x_ticks_len)
    x_ticks_loc = x_ticks*280
    
    plt.plot(time, concentration, color="#E16600")
    plt.xlabel("Time (Years)")
    plt.ylabel("Concentration (%)")
    plt.xticks(x_ticks_loc, x_ticks)
    plt.title("Concentration Over Time")
    plt.savefig("Concentration_Graph")
    plt.figure()
    
    return

# Creates and saves Power VS Time Graph
def Power_Graph(power, time):
    
    x_ticks_len = len(time)/280
    x_ticks = np.arange(0,x_ticks_len)
    x_ticks_loc = x_ticks*280

    plt.plot(time, power, "r")
    plt.xlabel("Time (Years)")
    plt.ylabel("Power (MW)")
    plt.xticks(x_ticks_loc, x_ticks)
    plt.title("Reactor Power")
    plt.savefig("Power_Graph")    
    plt.figure()
    
    return

# Creates and saves Pressure VS Time Graph
def Temperature_Graph(temperature, time):
    
    x_ticks_len = len(time)/280
    x_ticks = np.arange(0,x_ticks_len)
    x_ticks_loc = x_ticks*280
    
    plt.plot(time, temperature)
    plt.xlabel("Time (Years)")
    plt.ylabel("Temperature (C)")
    plt.xticks(x_ticks_loc, x_ticks)
    plt.title("Reactor Temperature")
    plt.savefig("Temperature_Graph")    
    plt.figure()
    
    return

# Creates and saves Purity VS Time Graph
def Solubility_Graph():
    # Create temperature pool
    temperatures = np.zeros(61)
    start_temp = 450
    i = 0
    while i < len(temperatures):
        temperatures[i] = start_temp + i*10
        i = i + 1
        
    # Create Solubility Pool
    solubilities = np.zeros(61)
    i = 0
    while i < len(solubilities):
        solubilities[i] = Chemistry.solubilitypercentage(temperatures[i])
        i = i + 1
    
    plt.plot(temperatures, solubilities, color="#55FF55")
    plt.xlabel("Temperature (C)")
    plt.ylabel("Solubility %")
    #plt.ylim(70,100)
    plt.title("Solubility VS Temperature")
    plt.savefig("Solubility_Graph")    
    plt.figure()
    
    return

# Sets time variable to 5 years
def Five_Years():
    global time
    time=1
    return

# Sets time variable to 10 years
def Ten_Years():
    global time
    time=2
    return

# Sets time variable to 20 years
def Twenty_Years():
    global time
    time=4
    return

# Shows model of reactor
    
def Show_Model():
    
    Model_Window = Toplevel()
    Model_Window.title("Reactor Model")
    
    Model_Image = PhotoImage(file="FluidsModel.png")
    Model = Label(Model_Window, image=Model_Image)
    Model.image = Model_Image
    Model.pack()


# Opens Input window
def Input():
    global time
    
    window = Tk()
    window.title("Welcome")
    window.attributes("-topmost", True)
    
    title = Label(window, text="MSRE Simulation", font=("Times New Roman", 16)).grid(row=0,columnspan=2, padx=50)
    
    button_title = Label(text="Reactor runtime:").grid(row=1)
    v = IntVar()
    Radiobutton(text="5 years", variable=v, value=1,
                command=Five_Years).grid(row=2)
    Radiobutton(text="10 years", variable=v, value=2,
                command=Ten_Years).grid(row=3)
    Radiobutton(text="20 years", variable=v, value=3,
                command=Twenty_Years).grid(row=4)
    
    run = Button(text="Run Simulation", command=window.destroy).grid(row=5, column=0, sticky=E, pady=5, padx=50)
    
    mainloop()
    
    
    return

# Creates simluation Output
def Output():
    global mma
    
    graph_window = Tk()
    
    graph_window.title("Results")
    
    title = Label(text="Simulation Results", font=("Times New Roman", 20, "bold")).grid(row=0, columnspan=8)
    
    # Correctly formats each section of the Output window
    ##########################################################################
    Concentration_Image = PhotoImage(file="Concentration_Graph.png")
    ConcentrationG = Label(image=Concentration_Image).grid(row=1,column=0,columnspan=4)
    ConcentrationMaxL = Label(text="Max Concentration:",bg="#F94F5B").grid(row=2,column=0,sticky=E)
    ConcentrationMax = Label(text=mma[0],bg="#F94F5B").grid(row=2,column=1,sticky=W)
    ConcentrationMinL = Label(text="Min Concentration:",bg="#CFFCFF").grid(row=2,column=2,sticky=E)
    ConcentrationMin = Label(text=mma[1],bg="#CFFCFF").grid(row=2,column=3,sticky=W)
    ConcentrationAvgL = Label(text="Average Concentration:").grid(row=3,column=0,columnspan=2,sticky=E)
    ConcentrationAvg = Label(text=mma[2]).grid(row=3,column=2,columnspan=2,sticky=W)
    
    Power_Image = PhotoImage(file="Power_Graph.png")
    PowerG = Label(image=Power_Image).grid(row=1,column=4,columnspan=4)
    PowerMaxL = Label(text="Max Power:",bg="#F94F5B").grid(row=2,column=4,sticky=E)
    PowerMax = Label(text=mma[3],bg="#F94F5B").grid(row=2,column=5,sticky=W)
    PowerMinL = Label(text="Min Power:",bg="#CFFCFF").grid(row=2,column=6,sticky=E)
    PowerMin = Label(text=mma[4],bg="#CFFCFF").grid(row=2,column=7,sticky=W)
    PowerAvgL = Label(text="Average Power:").grid(row=3,column=4,columnspan=2,sticky=E)
    PowerAvg = Label(text=mma[5]).grid(row=3,column=6,columnspan=2,sticky=W)
    
    Temperature_Image = PhotoImage(file="Temperature_Graph.png")
    TemperatureG = Label(image=Temperature_Image).grid(row=4,column=0,columnspan=4)
    TemperatureMaxL = Label(text="Max Temperature:",bg="#F94F5B").grid(row=5,column=0,sticky=E)
    TemperatureMax = Label(text=mma[6],bg="#F94F5B").grid(row=5,column=1,sticky=W)
    TemperatureMinL = Label(text="Min Temperature:",bg="#CFFCFF").grid(row=5,column=2,sticky=E)
    TemperatureMin = Label(text=mma[7],bg="#CFFCFF").grid(row=5,column=3,sticky=W)
    TemperatureAvgL = Label(text="Average Temperature:").grid(row=6,column=0,columnspan=2,sticky=E)
    TemperatureAvg = Label(text=mma[8]).grid(row=6,column=2,columnspan=2,sticky=W)
    
    Solubility_Image = PhotoImage(file="Solubility_Graph.png")
    SolubilityG = Label(image=Solubility_Image).grid(row=4,column=4,columnspan=4)
    ##########################################################################
    
    m = Button(text="Show Reactor Model", command=Show_Model).grid(row=7, column=0, columnspan=4, pady=5)
    b = Button(text="Exit", command=graph_window.destroy).grid(row=7, column=4, columnspan=4, pady=5)
    
    mainloop()
    
    
    return

# Function that will be used to initiate the calculative iterations and obtain data
def Data_Processing():
    global time
    global mma
    
    data = Control.Run_Sim(time)
    
    concentration = data[0]/1000000000
    power = data[1]
    rk_temperature = data[2] #fill in later
    solubility = data[3]
    HX1_Temp = data[4]
    HX2_Temp = data[5]
    
    time_array = np.zeros(time * 1440)
    
    i = 0
    while (i < time * 1440):
        time_array[i] = i + 1
        i = i + 1
    
    Concentration_Graph(concentration, time_array)
    Power_Graph(power, time_array)
    Temperature_Graph(rk_temperature, time_array)
    Solubility_Graph()
    
    mma = np.zeros(12)
    mma[0] = round(max(concentration), 2)
    mma[1] = round(min(concentration), 2)
    mma[2] = round(sum(concentration)/(time*1440), 2)
    mma[3] = round(max(power), 2)
    mma[4] = round(min(power), 2)
    mma[5] = round(sum(power)/(time*1440), 2)
    mma[6] = round(max(rk_temperature), 2)
    mma[7] = round(min(rk_temperature), 2)
    mma[8] = round(sum(rk_temperature)/(time*1440), 2)
    mma[9] = round(max(solubility), 2)
    mma[10] = round(min(solubility), 2)
    mma[11] = round(sum(solubility)/(time*1440), 2)
    
    return

# Alerts the user when no input was detected
def Error_Message():
    
    error = Tk()
    
    message = Label(text="Reactor runtime was not chosen.", padx=10,pady=10).pack()
    message2 = Label(text="Please try again.", padx=10,pady=10).pack()
    
    mainloop()
    
    return

# Used to run this script from an outside file
def RunGUI():
    Input()
    if not (time == None):
        Data_Processing()
        Output()
    else:
        Error_Message()    
    return

if __name__ == "__main__":
    Input()
    if not (time == None):
        Data_Processing()
        Output()
    else:
        Error_Message()