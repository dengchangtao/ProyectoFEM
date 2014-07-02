
import numpy as np
import scipy.special
import matplotlib.pyplot as plt


def SolAnaliticaCirculo(x,y,n,m):
  theta = np.where(x==0,0.,np.arctan(y/x))
  theta = np.where(x<=0,theta+np.pi,theta)
  r = np.sqrt(x**2+y**2)
  jv = scipy.special.jn
  jpm0=scipy.special.jnp_zeros(m,n)

  kmn=jpm0[-1]/R
  wmn = np.sqrt(9.81*0.1) * kmn
  Tmn = 2*np.pi/wmn

  eta_mn = jv(m,kmn*r)*(np.cos(m*theta)+np.sin(m*theta))
  
  return Tmn, eta_mn

R = 1.
h0=0.1
dtheta= 360/100.
theta1 = np.linspace(0,2*np.pi,100)
r1 = np.linspace(0,R,100)
theta1, r1 = np.meshgrid(theta1,r1)

x = np.cos(theta1)*r1
y = np.sin(theta1)*r1

for n in range(1,5):
  for m in range(5):
    T_mn,eta_mn = SolAnaliticaCirculo(x,y,n,m)
    plt.pcolormesh(x,y,eta_mn)
    plt.title('%.2f, n=%i, m=%i'%(T_mn,n,m))
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('modo_analitico_%i_%i.png'%(n,m))
    plt.close()
    