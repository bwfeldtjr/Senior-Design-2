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
global is_short_run
is_short_run = False
global short_run_time



# Creates and saves Temperature VS Time Graph
def Concentration_Graph(concentration, time):
    global is_short_run
    
    if is_short_run == True:
        x_ticks = [0,1,2,3]
        x_ticks_loc = [0,5,10,15]
        plt.plot(time, concentration, color="#E16600")
        plt.xlabel("Time (Days)")
        plt.ylabel("Concentration (%)")
        plt.xticks(x_ticks_loc, x_ticks)
        plt.title("Concentration Over Time")
        plt.savefig("Concentration_Graph")
        plt.figure()
    else:
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
    global is_short_run
    
    if is_short_run == True:
        x_ticks = [0,1,2,3]
        x_ticks_loc = [0,5,10,15]
        plt.plot(time, power, "r")
        plt.xlabel("Time (Days)")
        plt.ylabel("Power (MW)")
        plt.xticks(x_ticks_loc, x_ticks)
        plt.title("Reactor Power")
        plt.savefig("Power_Graph")    
        plt.figure()
    else:
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
def Temperature_Graph(r_temperature, hx_temperature, time):
    global is_short_run
    
    if is_short_run == True:
        x_ticks = [0,1,2,3]
        x_ticks_loc = [0,5,10,15]
        plt.plot(time, r_temperature, label="Reactor")
        plt.plot(time, hx_temperature, label="Heat Exchanger")
        plt.legend()
        plt.xlabel("Time (Days)")
        plt.ylabel("Temperature (C)")
        plt.xticks(x_ticks_loc, x_ticks)
        plt.title("Reactor Temperature")
        plt.savefig("Temperature_Graph")    
        plt.figure()
    else:
        x_ticks_len = len(time)/280
        x_ticks = np.arange(0,x_ticks_len)
        x_ticks_loc = x_ticks*280
        plt.plot(time, r_temperature, label="Reactor")
        plt.plot(time, hx_temperature, label="Heat Exchanger")
        plt.legend()
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

# Sets time variable to 3 days
def Short_Run():
    global time
    global is_short_run
    is_short_run = True
    time="SHORT"
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
    
def Show_Pressures():
    global Fuel_Pressures
    global Coolant_Pressures
    
    # Create new window
    Model_Window = Toplevel()
    Model_Window.title("Reactor Model")
    # Place image
    Model_Image = PhotoImage(file="FluidsModel.png")
    Model = Label(Model_Window, image=Model_Image)
    Model.image = Model_Image
    Model.grid(row=0, column=0, columnspan=4)
    # Fuel pressures
    F1 = Label(Model_Window, text=("F1:", round(Fuel_Pressures[0]), "kPa")).grid(row=1,column=0)
    F2 = Label(Model_Window, text=("F2:", round(Fuel_Pressures[1]), "kPa")).grid(row=2,column=0)
    F3 = Label(Model_Window, text=("F3:", round(Fuel_Pressures[2]), "kPa")).grid(row=3,column=0)
    F4 = Label(Model_Window, text=("F4:", round(Fuel_Pressures[3]), "kPa")).grid(row=4,column=0)
    F5 = Label(Model_Window, text=("F5:", round(Fuel_Pressures[4]), "kPa")).grid(row=1,column=1)
    F6 = Label(Model_Window, text=("F6:", round(Fuel_Pressures[5]), "kPa")).grid(row=2,column=1)
    F7 = Label(Model_Window, text=("F7:", round(Fuel_Pressures[6]), "kPa")).grid(row=3,column=1)
    # Coolant Pressures
    C1 = Label(Model_Window, text=("C1:", round(Coolant_Pressures[0]), "kPa")).grid(row=1,column=2)
    C2 = Label(Model_Window, text=("C2:", round(Coolant_Pressures[1]), "kPa")).grid(row=2,column=2)
    C3 = Label(Model_Window, text=("C3:", round(Coolant_Pressures[2]), "kPa")).grid(row=3,column=2)
    C4 = Label(Model_Window, text=("C4:", round(Coolant_Pressures[3]), "kPa")).grid(row=1,column=3)
    C5 = Label(Model_Window, text=("C5:", round(Coolant_Pressures[4]), "kPa")).grid(row=2,column=3)
    C6 = Label(Model_Window, text=("C6:", round(Coolant_Pressures[5]), "kPa")).grid(row=3,column=3)


# Opens Input window
def Input():
    global time
    
    window = Tk()
    window.title("Welcome")
    window.attributes("-topmost", True)
    
    title = Label(window, text="MSR Simulation", font=("Times New Roman", 16)).grid(row=0,columnspan=2, padx=50)
    
    button_title = Label(text="Reactor runtime:").grid(row=1)
    v = IntVar()
    Radiobutton(text="First 3 days", variable=v, value=1,
                command=Short_Run).grid(row=2)
    Radiobutton(text="5 years", variable=v, value=2,
                command=Five_Years).grid(row=3)
    Radiobutton(text="10 years", variable=v, value=3,
                command=Ten_Years).grid(row=4)
    Radiobutton(text="20 years", variable=v, value=4,
                command=Twenty_Years).grid(row=5)
    
    run = Button(text="Run Simulation", command=window.destroy).grid(row=6, column=0, sticky=E, pady=5, padx=50)
    
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
    ConcentrationG = Label(image=Concentration_Image).grid(row=1,column=0,columnspan=2)
    ConcentrationMax = Label(text=("Max Concentration:", mma[0]),bg="#F94F5B").grid(row=2,column=0,sticky=E, padx=5)
    ConcentrationMin = Label(text=("Min Concentration:", (mma[1])),bg="#CFFCFF").grid(row=2,column=1,sticky=W, padx=5)
    ConcentrationAvg = Label(text=("Average Concentration:", mma[2])).grid(row=3,column=0,columnspan=2)
    
    Power_Image = PhotoImage(file="Power_Graph.png")
    PowerG = Label(image=Power_Image).grid(row=1,column=2,columnspan=2)
    PowerMax = Label(text=("Max Power:", mma[3], "MW"),bg="#F94F5B").grid(row=2,column=2,sticky=E, padx=5)
    PowerMin = Label(text=("Min Power:", mma[4], "MW"),bg="#CFFCFF").grid(row=2,column=3,sticky=W, padx=5)
    PowerAvg = Label(text=("Average Power:", mma[5], "MW")).grid(row=3,column=2,columnspan=2)

    
    Temperature_Image = PhotoImage(file="Temperature_Graph.png")
    TemperatureG = Label(image=Temperature_Image).grid(row=4,column=0,columnspan=2)
    TemperatureMax = Label(text=("Reactor Max Temperature:", mma[6], "C"),bg="#F94F5B").grid(row=5,column=0,sticky=W, padx=5)
    TemperatureMin = Label(text=("Reactor Min Temperature:", mma[7], "C"),bg="#CFFCFF").grid(row=6,column=0,sticky=W, padx=5)
    TemperatureAvg = Label(text=("Reactor Average Temperature:", mma[8], "C")).grid(row=7, column=0,sticky=W, padx=5)
    HXTemperatureMax = Label(text=("HX Max Temperature:", mma[9], "C"),bg="#F94F5B").grid(row=5,column=1,sticky=W)
    HXTemperatureMin = Label(text=("HX Min Temperature:", mma[10], "C"),bg="#CFFCFF").grid(row=6,column=1,sticky=W)
    HXTemperatureAvg = Label(text=("HX Average Temperature:", mma[11], "C")).grid(row=7,column=1,sticky=W)
    
    Solubility_Image = PhotoImage(file="Solubility_Graph.png")
    SolubilityG = Label(image=Solubility_Image).grid(row=4,column=2,columnspan=2)
    ##########################################################################
    
    m = Button(text="Show Reactor Pressures", command=Show_Pressures).grid(row=8, column=0, columnspan=2, pady=5)
    b = Button(text="Exit", command=graph_window.destroy).grid(row=8, column=2, columnspan=2, pady=5)
    
    mainloop()
    
    
    return

# Function that will be used to initiate the calculative iterations and obtain data
def Data_Processing():
    global time
    global mma
    global Coolant_Pressures
    global Fuel_Pressures
    global short_run_time
    
    data = Control.Run_Sim(time)
    
    concentration = data[0]/1000000000
    power = data[1]
    rk_temperature = data[2] #fill in later
    solubility = data[3]
    HX1_Temp = data[4]
    HX2_Temp = data[5]
    Fuel_Pressures = np.array(data[6])/1000
    Coolant_Pressures = np.array(data[7])/1000
    
    if is_short_run == True:
        short_run_time = 15
        time_array = np.arange(0,short_run_time)
    else:
        time_array = np.zeros(time * 1440)
        
        i = 0
        while (i < time * 1440):
            time_array[i] = i + 1
            i = i + 1
    
    Concentration_Graph(concentration, time_array)
    Power_Graph(power, time_array)
    Temperature_Graph(rk_temperature, HX2_Temp, time_array)
    Solubility_Graph()
    
    if is_short_run == True:
        mma = np.zeros(12)
        mma[0] = round(max(concentration), 2)
        mma[1] = round(min(concentration), 2)
        mma[2] = round(sum(concentration)/(short_run_time), 2)
        mma[3] = round(max(power), 2)
        mma[4] = round(min(power), 2)
        mma[5] = round(sum(power)/(short_run_time), 2)
        mma[6] = round(max(rk_temperature), 2)
        mma[7] = round(min(rk_temperature), 2)
        mma[8] = round(sum(rk_temperature)/(short_run_time), 2)
        mma[9] = round(max(HX2_Temp), 2)
        mma[10] = round(min(HX2_Temp), 2)
        mma[11] = round(sum(HX2_Temp)/(short_run_time), 2)
    else:
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
        mma[9] = round(max(HX2_Temp), 2)
        mma[10] = round(min(HX2_Temp), 2)
        mma[11] = round(sum(HX2_Temp)/(time*1440), 2)
    
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