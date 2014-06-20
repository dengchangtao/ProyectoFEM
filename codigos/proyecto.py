# -*- coding: utf-8 -*-
#! python
####################################
######## PROYECTO SEMESTRAL ########

import numpy as np
import Tri3
import matplotlib.pylab as plt

####################################
#########      Parte 1      ########
####  Bahia y lago rectangular  ####
####################################

l = 20.
L = 50.
h = 2.
g = 9.8
ndx = 5
ndy = 2
C2 = g*h
eta_g = 0.0

xyz, IEN = Tri3.MeshDomain(L, l, ndx, ndy)
IEN = np.transpose(IEN)

########   Bahia Cerrada   #######
LM = IEN
ID = np.arange(xyz.shape[0]) + 1

M, K = Tri3.Tri3HelmholtzAssembleMKF(xyz, IEN, LM, C2, Mlumped=False)
A = np.dot(M.I, K)
eigenvalues, eigenvectors = np.linalg.eig(A)

#Primer modo
Modo1 = np.zeros((xyz.shape[0], 1))
posmin = np.argmin(eigenvalues)

w = np.sqrt(eigenvalues[posmin])
period = 2.*np.pi/w
wavelength = np.sqrt(C2)*period
eta = eigenvectors[:, posmin]
print 'wavelength = ', wavelength

for i in np.arange(ID.shape[0]):
    if ID[i] != 0:
        Modo1[i, 0] = eta[ID[i]-1,0]
    else:
        Modo1[i, 0] = eta_g

x = xyz[:, 0]
y = xyz[:, 1]
triangles = IEN-1
plt.tricontourf(x, y, triangles, Modo1[:, 0])

Tri3.Plot2DQuadGeometry(xyz,IEN,nodeId=True,elemId=False)
plt.colorbar()
plt.show()

########   Narrow Bay   #######
CBdirichlet = np.arange(ndx+1, (ndx+1)*(ndy+2), ndy+1)
ID = np.zeros(xyz.shape[0], dtype=int)
aux1 = 1
for i in np.arange(ID.shape[0]):
    aux2 = 1
    for j in np.arange(CBdirichlet.shape[0]):
        if i+1 == CBdirichlet[j]:
            aux2 = aux1*0
        else:
            aux2 = aux2
    if aux2 != 0:
        ID[i] = aux1
        aux1 = aux1 + 1

LM = np.zeros((IEN.shape[0], 3), dtype=int)

for i in np.arange(IEN.shape[0]):
    for j in np.arange(IEN.shape[1]):
        LM[i, j] = ID[IEN[i, j]-1]

