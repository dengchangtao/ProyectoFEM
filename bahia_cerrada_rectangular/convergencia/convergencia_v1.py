# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from helmholtz import *
h0=4./9.81
c2=9.81*h0

#Resultados teóricos
def ModPropSquare(m,n):
    L = 2*np.pi/(np.sqrt((m*np.pi)**2+(n*np.pi)**2))
    return L

def modosrectangular(m,n,x,y):
    u = cos(m*np.pi*x)*cos(n*np.pi*y)
    return u

#def vpropios(n):
 #   xyz,IEN,ID,LM=MeshDomain(n,n)
  #  K,M=Tri3HelmholtzAssemble(xyz,IEN,LM,c2)
   # Ml=np.zeros(M.shape)
   # for i in range(M.shape[0]):
   #     Ml[i,i]=np.sum(M[i,:])
   # A1=np.dot(np.inv(Ml),K)
   # l1,v1=np.linalg.eig(A1)
   # return l1

NN=np.array([2,4,6,8,10,12,16,20,24,32,40,50])
Modos=np.zeros((NN.shape[0],7))
Error=np.zeros((NN.shape[0],7))    
for i in np.arange(NN.shape[0]):
    xyz,IEN,ID,LM=MeshDomain(NN[i],NN[i])
    K,M=Tri3HelmholtzAssemble(xyz,IEN,LM,c2)
    Ml=np.zeros(M.shape)
    for j in range(M.shape[0]):
        Ml[j,j]=np.sum(M[j,:])
        Ml=np.mat(Ml)
    A=Ml.I*K
    l,v=np.linalg.eig(A)
    np.savez('modprop_N_'+str((NN[i]-1)*(NN[i]-1)*2),l=l, v=v)
    iv=np.argsort(l.real)
    w1 = np.sqrt(l[iv[1]].real)
    w2 = np.sqrt(l[iv[3]].real)
    Modos[i,0] = 1./(NN[i])
    Modos[i,1] = (2.*np.pi/w1)*np.sqrt(c2)
    Modos[i,2] = (2.*np.pi/w2)*np.sqrt(c2) 
    Error[i,1] = abs((2.*np.pi/w1)*np.sqrt(c2) - ModPropSquare(1,0))
    Error[i,2] = abs((2.*np.pi/w2)*np.sqrt(c2) - ModPropSquare(1,1))
    if i>0:
        
        w3 = np.sqrt(l[iv[5]].real)
        w4 = np.sqrt(l[iv[7]].real)
        w5 = np.sqrt(l[iv[9]].real)
        w6 = np.sqrt(l[iv[11]].real)
        
        Modos[i,3] = (2.*np.pi/w3)*np.sqrt(c2)
        Modos[i,4] = (2.*np.pi/w4)*np.sqrt(c2)
	Modos[i,5] = (2.*np.pi/w5)*np.sqrt(c2)
	Modos[i,6] = (2.*np.pi/w6)*np.sqrt(c2)
	
        Error[i,3] = abs((2.*np.pi/w3)*np.sqrt(c2) - ModPropSquare(2,0))
        Error[i,4] = abs((2.*np.pi/w4)*np.sqrt(c2) - ModPropSquare(2,1))
	Error[i,5] = abs((2.*np.pi/w5)*np.sqrt(c2) - ModPropSquare(3,0))
	Error[i,6] = abs((2.*np.pi/w6)*np.sqrt(c2) - ModPropSquare(3,1))
plt.figure()
plt.subplot(121)
plt.loglog(Modos[:,0],Error[:,1],'o')
plt.loglog(Modos[:,0],Error[:,2],'o')
plt.loglog(Modos[1:,0],Error[1:,3],'o')
plt.loglog(Modos[1:,0],Error[1:,4],'o')
plt.loglog(Modos[1:,0],Error[1:,5],'o')
plt.loglog(Modos[1:,0],Error[1:,6],'o')
plt.xlabel('Longitud h del elemento [m]')
plt.ylabel('Error aproximacion por FEM')
plt.legend(('Modo 1','Modo 3','Modo 5','Modo 7','Modo 9','Modo 11'), 1)
plt.grid()

plt.subplot(122)
plt.plot(Modos[:,0],Modos[:,1])
plt.plot(Modos[:,0],Modos[:,2])
plt.plot(Modos[1:,0],Modos[1:,3])
plt.plot(Modos[1:,0],Modos[1:,4])
plt.plot(Modos[1:,0],Modos[1:,5])
plt.plot(Modos[1:,0],Modos[1:,6])
plt.xlabel('Longitud h del elemento [m]')
plt.ylabel('Longitud de onda')
plt.legend(('Modo 1','Modo 3','Modo 5','Modo 7','Modo 9','Modo 11'), 0)
plt.grid()
plt.show()

plt.savefig('valores_propios.png')
plt.savefig('Modos_propios.pdf')

