from scipy import integrate
from scipy import special
from math import pi

#geometry values
lam = 0.29 #tip to root ratio (lambda)
Cr = 6.76

#Set values
b = 41.1     #m
V_cruise = 233.105    #m/s
P_req = ((30*pi)/180)/1.5 #rad/s
da = 25 *(pi/180) #rad/s
b1 =  0.7*b/2 #m
tau = 0.42

#Values still to be determined by other groups
c_l_alpha = 0.0999 *180/pi #1/rad #Based on tip airfoil
c_d0 = 0.007     #Based on 
ca_c = 0.2 #Aileron chord to wing chord ratio

#Integration parameters
y1 = b1
y2 = y1
dy = 0.001



def c_1(y):#c(y)*y
    return ((lam*Cr-Cr)/(b/2)) * y**2 + 6.76*y
def c_2(y):# c(y)*y^2
    return ((lam*Cr-Cr)/(b/2)) * y**3 + 6.76*y**2

P=0.0
i = 0
while P < P_req and y2<(b/2): #rad/s

    P =      -((2.0*c_l_alpha*tau) * integrate.quad(c_1, y1, y2)[0])  #Clda
    P = P/   -((4*(c_l_alpha+c_d0)/b) * integrate.quad(c_2, 0, b/2)[0])#Clp
    P = P*   da * ((2*V_cruise)/(b)) #last bit of P eqn.

    if i%1000 == 0:
        print("calculating at iteration:",i, "with(P y1 y2):",P,y1,y2)
    i+=1
    y2 = y2 + dy

print(P_req,P)
print(y1, y2, y2-y1, b/2)
print(y1/(b/2),y2/(b/2) )


