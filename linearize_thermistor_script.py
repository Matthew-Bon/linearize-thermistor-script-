# !/usr/bin/python3
#Linearized NTC Thermistor Script
#This code was developed with the help of this excellent article
#https://www.mathscinotes.com/2013/12/two-resistor-thermistor-linearizer/
import matplotlib.pyplot as plt
import math 
from tkinter import *

from tkinter import messagebox

top = Tk()
top.geometry("600x800")
resistor_number = IntVar()

#function for rounding resistor values to a standard 1% resistor 
def resistor_round(Rs):
    magnitude = [10, 100, 1000, 10000, 100000, 1000000]

    r_values = [ 10.0, 10.2, 10.5, 10.7, 11.0, 11.3, 11.5, 11.8, 12.1, 12.4, 12.7,
                 13.0, 13.3, 13.7, 14.0, 14.3, 14.7, 15.0, 15.4, 15.8, 16.2, 16.5,
                 16.9, 17.4, 17.8, 18.2, 18.7, 19.1, 19.6, 20.0, 20.5, 21.0, 21.5,
                 22.1, 22.6, 23.2, 23.7, 24.3, 24.9, 25.5, 26.1, 26.7, 27.4, 28.0,
                 28.7, 29.4, 30.1, 30.9, 31.6, 32.4, 33.2, 34.0, 34.8, 35.7, 36.5,
                 37.4, 38.3, 39.2, 40.2, 41.2, 42.2, 43.2, 44.2, 45.2, 46.4, 47.5,
                 48.7, 49.9, 51.1, 52.3, 53.6, 54.9, 56.2, 57.6, 59.0, 60.4, 61.9,
                 63.4, 64.9, 66.5, 68,1, 69.8, 71.5, 73.2, 75.0, 76.8, 78.7, 80.6,
                 82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6]

    divisor = 1

    #Determine devisor size

    if Rs < 10:
        divisor = 0.1
    elif Rs <100:
        divisor = 1
    elif Rs < 1000:
        divisor = 10
    elif Rs < 10000:
        divisor = 100
    elif Rs < 100000:
        divisor = 1000
    else:
        divisor = 10000

    Rs = min(r_values, key=lambda x:abs(x-(Rs/divisor)))  #Min function gets value from r_values that has the shortest distance from RS/Divisor 

    Rs = Rs * divisor # Set value back to the right magnitude

    return Rs 

def calccallback():
    #Get values and convert tempratures to Kelvin 
    To = int(To_entry.get()) + 273 
    Tl = int(Tl_entry.get()) + 273 
    Th = int(Th_entry.get()) + 273
    Ro = int(Ro_entry.get())
    B = int (B_entry.get())
    Tmid = (Th-Tl)/2
    
    #Calculate for the single resistor case
    if (resistor_number.get() == 1):

        T_values = list(range(Tl, Th))

        R_values = [Ro*math.exp(B*((1/T)-(1/To))) for T in T_values]
        Rs = R_values[int(Tmid)]*((B-2*Tmid)/(B+2*Tmid))
        Rs = resistor_round(Rs)
        Rs_values = [Rs/(R+Rs) for R in R_values] 
        R_slope =  (Rs_values[-1] - Rs_values[0])/(Th-Tl)
        intercept = Rs_values[0]
        
    #Calculate for the two resistor case
    if (resistor_number.get() == 2):
        Tr = (Th + Tl)/2 #determine mid temp for calculating ballast resistor
        Rbalast = Ro*math.exp(B*((1/Tr)-(1/To))) * 3

        T_values = list(range(Tl, Th))
        R_values = [Ro*math.exp(B*((1/T)-(1/To))) for T in T_values]

        R_linear_values = [(Ro*math.exp(B*((1/T)-(1/To))) * Rbalast)/(Ro*math.exp(B*((1/T)-(1/To))) + Rbalast) for T in T_values]

        Rs = (Ro*Rbalast)/(Ro+Rbalast)
        Rs_values = [(Rs/(Rs+(Ro*math.exp(B*((1/T)-(1/To))) * Rbalast)/(Ro*math.exp(B*((1/T)-(1/To))) + Rbalast))) for T in T_values]
        R_slope =  (Rs_values[-1] - Rs_values[0])/(Th-Tl)
        intercept = Rs_values[0]
        print("R balast is = ", Rbalast)

    #Print Results and Graphs
    T_values = [T-273 for T in T_values]
    print("R series is = ", round(Rs,1))
    print("Linear function is : ",R_slope,"*(Temp - ", (Tl-273), ") + ", intercept)
    fig, (R, V)= plt.subplots(2)
    fig.suptitle("Thermistor values and ratio") 
    R.plot(T_values, R_values, linewidth=1,color= 'red')
    if (resistor_number.get() == 2):
        R.plot(T_values, R_linear_values, linewidth=1, color = 'blue')
    R.set_ylabel('Resistance (ohms)')
    R.set_xlabel('Temperature (C)')
    V.plot(T_values, Rs_values, linewidth = 1)
    V.set_ylabel('Ratio')
    V.set_xlabel('Temperature (C)')
    plt.show()


#Setup label layout 
L1 = Label(top, text = "Thermistor resistance from datasheet")
L1.place(x = 75, y = 50)
L2 = Label(top, text = "Temperature of thermistor resistance in C")
L2.place(x = 75, y = 75)
L3 = Label(top, text = "Beta Value")
L3.place(x = 75, y = 100)
L4 = Label(top, text = "The lowest temp you wish to measure in C ")
L4.place(x = 75, y = 125)
L5 = Label(top, text = "The highest temp you wish to measure in C")
L5.place(x = 75, y = 150)

#Setup entry boxes
Ro_entry = Entry(top, bd = 2, justify = RIGHT)
Ro_entry.place(x = 325, y = 50)
To_entry = Entry(top, bd = 2, justify = RIGHT)
To_entry.place(x = 325, y = 75)
B_entry = Entry(top, bd = 2, justify = RIGHT)
B_entry.place(x = 325, y = 100)
Tl_entry = Entry(top, bd = 2, justify = RIGHT)
Tl_entry.place(x = 325, y = 125)
Th_entry = Entry(top, bd = 2, justify = RIGHT)
Th_entry.place(x = 325, y = 150)

#Setup Radiobutton
R1 = Radiobutton(top, text = "One Resistor Linerization", variable = resistor_number, value = 1)
R1.place(x = 75, y = 200)
R2 = Radiobutton(top, text = "Two Resistor Linerization", variable = resistor_number, value = 2)
R2.place(x = 300, y = 200) 

#Setup Button
Calc = Button(top, text = "Calculate" , command = calccallback)
Calc.place(x = 400, y = 250)

#Run loop 
top.mainloop()


        
    
