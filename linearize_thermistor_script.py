#Linearized NTC Thermistor Script
#This code was developed with the of this excellent article
#https://www.mathscinotes.com/2013/12/two-resistor-thermistor-linearizer/
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

T_values = list(range(Tl, Th))
R_values = [Ro*math.exp(B*((1/T)-(1/To))) for T in T_values]

R_linear_values = [(Ro*math.exp(B*((1/T)-(1/To))) * Rbalast)/(Ro*math.exp(B*((1/T)-(1/To))) + Rbalast) for T in T_values]

Rs = (Ro*Rbalast)/(Ro+Rbalast)
Rs_values = [(Rs/(Rs+(Ro*math.exp(B*((1/T)-(1/To))) * Rbalast)/(Ro*math.exp(B*((1/T)-(1/To))) + Rbalast))) for T in T_values]
R_slope =  (Rs_values[-1] - Rs_values[0])/(Th-Tl)
B = R_slope * Tl -0.5
print("R balast is = ", Rbalast)
print("R series is = ", Rs)
print("Linear function is : ",R_slope,"x -", B)
fig, (R, V)= plt.subplots(2)
fig.suptitle("Thermistor values and ratio") 
R.plot(T_values, R_values, linewidth=5,color= 'red')
R.plot(T_values, R_linear_values, linewidth=5, color = 'blue')
R.set_ylabel('Resistance (ohms)')
R.set_xlabel('Temperature (K)')
V.plot(T_values, Rs_values, linewidth = 5)
V.set_ylabel('Ratio')
V.set_xlabel('Temperature (K)')
plt.show()
