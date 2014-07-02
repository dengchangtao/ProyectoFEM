import numpy as np
import scipy.special

dtheta= 360/100.
theta = np.linspace(0,2*np.pi,100)
r = np.linspace(0,1,100)

theta,r = np.meshgrid(theta,r )

jv = scipy.special.jn

R = 1.
h0=0.1
n=1
m=1

jpm0=scipy.special.jnp_zeros(m,n)

kmn=jpm0/R
wmn = np.sqrt(9.81*0.1) * kmn
Tmn = 2*np.pi/wmn

eta_mn = jv(m,kmn*r)*(np.cos(m*theta)+np.sin(m*theta))

import matplotlib.pyplot as plt
x = np.cos(theta)*r
y = np.sin(theta)*r
plt.pcolormesh(x,y,eta_mn)