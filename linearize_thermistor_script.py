#Linearized NTC Thermistor Script
import matplotlib.pyplot as plt
import math 

Ro = int(input("\n Input thermistor resistance from datasheet \n"))
To = int(input("\n Input temperature of thermistor resistance in C \n"))
B = int(input("\n Input Beta Value  \n"))
Tl = int(input("\n Input the lowest temp you wish to measure in C \n"))
Th = int(input("\n Input the highest temp you wish to measure in C \n"))

#convert temps to Kelvin
To = To + 273 
Tl = Tl + 273 
Th = Th + 273 

Tr = (Th + Tl)/2 #determine mid temp for calculating ballast resistor
Rbalast = Ro*math.exp(B*((1/Tr)-(1/To))) * 3

print(Rbalast) 

T_values = list(range(Tl, Th))
R_values = [Ro*math.exp(B*((1/T)-(1/To))) for T in T_values]

plt.subplot(T_values, R_values, linewidth=5)

plt.show()

R_linear_values = [(Ro*math.exp(B*((1/T)-(1/To))) * Rbalast)/(Ro*math.exp(B*((1/T)-(1/To))) + Rbalast) for T in T_values]

plt.subplot(T_values, R_linear_values, linewidth=5)

plt.show()
