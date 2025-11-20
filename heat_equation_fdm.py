import numpy as np 
import matplotlib.pyplot as plt 
 
 
dx = 0.02 
dt = 0.001 
 

D = 0.1 
if D >= dx**2 / (2 * dt):
    raise ValueError(f"Условие Куранта нарушено! Убедитесь, что D * dt / dx^2 <= 0.5. Текущее значение: {D * dt / dx ** 2}")
Tm = 4.0 
L = 1.0  
 
x = np.arange(0, L + dx, dx) 
t = np.arange(0, Tm + dt, dt) 
 
xn = len(x)
tn = len(t) 
 
T = np.zeros((xn, tn)) 
 
T[0, :] = 0 
 
for j in range(1, tn): 
    for i in range(1, xn - 1): 
        T[i, j] = D * T[i - 1, j - 1] + (1 - 2 * D) * T[i, j - 1] + D * T[i + 1, j - 1] 
 
    T[0, j] = T[1, j] + 2*dx  
    T[-1, j] = 1 
 
 
for j in range(0, tn, 1000): 
    plt.plot(x, T[:, j])
 
 
plt.legend([f't = {round(t[j], 3)} с' for j in range(0, tn, 1000)]) 
plt.xlabel("Расстояние, L") 
plt.ylabel('Температура, T') 
plt.grid(True) 
plt.show()