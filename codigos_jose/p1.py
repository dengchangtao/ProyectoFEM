import numpy as np
import matplotlib.pyplot as plt
from helmholtz import *

#i)
t1,w1=Tri3QGauss(1)
t2,w2=Tri3QGauss(2)
print '\nt1(k=1)=',t1
print '\nw1(k=1)=',w1
print '\nt1(k=2)=',t2
print '\nw1(k=2)=',w2

#ii)
xi=np.array([1./3.,1./3.])
Nhat,DNhat=Tri3NDhat(xi)
print '\nNhat=',Nhat
print '\nDNhat=',DNhat

#iii)
xeset=np.array([[2.,0.],[2.,1.],[0.,1.]])
xhat,N,DN,detJ=Tri3shp(xeset,Nhat,DNhat)
print '\nxhat=',xhat
print '\nN=',N
print '\nDN=',DN
print '\ndetJ=',detJ

#iv)
kappa=[[1.,0],[0,1]]
f=1.
c2=9.81*10.
xeset=np.array([[1.,0.],[1.,1.],[0.,1.]])
ke1=Tri3keHelmholtz(xeset,c2,1)
ke2=Tri3keHelmholtz(xeset,c2,1)
me1=Tri3me(xeset,1.)
print '\nke(k=1)=',ke1
print '\nke(k=2)=',ke2

xyz,IEN,ID,LM=MeshDomain(20,21)
plt.triplot(xyz[:,0],xyz[:,1],IEN)
#plt.show()

K,M=Tri3HelmholtzAssemble(xyz,IEN,LM,c2)
Ml=np.zeros(M.shape)
for i in range(M.shape[0]):
  Ml[i,i]=np.sum(M[i,:])


invM=M.I
for i in range(M.shape[0]):
  for j in range(i):
    invM[j,i]=invM[i,j]    
    
A1=M.I*K
A2=np.dot(np.linalg.inv(Ml),K)
A3=invM*K

l1,v1=np.linalg.eig(A1)
l2,v2=np.linalg.eig(A2)
l3,v3=np.linalg.eig(A3)
iv1=np.argsort(l1)
iv2=np.argsort(l2)
iv3=np.argsort(l3)


for ind in range(10):
  #ind=3
  u1=np.array(v1[:,iv1[ind]])[:,0]
  u2=np.array(v2[:,iv2[ind]])[:,0]
  u3=np.array(v3[:,iv3[ind]])[:,0]

  from scipy.interpolate import griddata
  plt.figure()
  x,y=np.meshgrid(np.linspace(0,1.,400),np.linspace(0,1.,200))
  ui=griddata(xyz,u3,(x,y))
  #plt.tripcolor(xyz[:,0],xyz[:,1],IEN,u1)
  plt.pcolormesh(x,y,ui)
  plt.title('n=%i,l1=%3.15e'%(iv1[ind],l1[iv1[ind]]))
  plt.show()
