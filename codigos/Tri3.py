# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pylab as plt

##########################
def Tri3QGauss(k):
    if k == 1 :
        tl = np.array([1./3.,1./3.,1./3.])
        wl = 1.
        return tl, wl
    if k == 2 :
        tl = np.array([[2./3.,1./6.,1/6.],
        [1./6.,2./3.,1/6.],
        [1./6.,1./6.,2./3.]])
        wl = 1/3.
        return tl, wl

##########################
def Tri3NDNHat(xi) :
    Nhat = np.zeros((1,3))
    Nhat[0,0] = xi[0]
    Nhat[0,1] = xi[0]
    Nhat[0,2] = 1-xi[0]-xi[1]
    DNhat = np.array([[1., 0.],[0., 1.],[-1., -1.]])
    return Nhat, DNhat


##########################
def Tri3shp(xeset,Nhat,DNhat) :
    xeset = np.array(xeset)
    xhat = np.zeros((1,2))
    xhat[0,0] = Nhat[0,0]*xeset[0,0]+Nhat[0,1]*xeset[1,0]+Nhat[0,2]*xeset[2,0]
    xhat[0,1] = Nhat[0,0]*xeset[0,1]+Nhat[0,1]*xeset[1,1]+Nhat[0,2]*xeset[2,1]

    N = Nhat

    JX = np.zeros((2,2))    
    JX[0,0] = DNhat[0,0]*xeset[0,0]+DNhat[1,0]*xeset[1,0]+DNhat[2,0]*xeset[2,0]
    JX[0,1] = DNhat[0,1]*xeset[0,0]+DNhat[1,1]*xeset[1,0]+DNhat[2,1]*xeset[2,0]
    JX[1,0] = DNhat[0,0]*xeset[0,1]+DNhat[1,0]*xeset[1,1]+DNhat[2,0]*xeset[2,1]
    JX[1,1] = DNhat[0,1]*xeset[0,1]+DNhat[1,1]*xeset[1,1]+DNhat[2,1]*xeset[2,1]
    JX = np.mat(JX)
    J = JX.I
    
    detJ=np.linalg.det(JX)

    DN = DNhat*J
    
    return xhat, N, DN, detJ


##########################
def Tri3kefePoisson(xeset, C2, k):
    
    # Cuadratura Gaussiana
    tl, wl = Tri3QGauss(k)
    tlaux = np.mat(tl)
    aux = int(tlaux.shape[0])
    
    # Definición puntos de integración
    x = np.zeros((aux,2))
    if aux == 1 :
        x[0,0] = tl[0]
        x[0,1] = tl[1]
    else :
        for i in np.arange(aux):
            x[i,0] = tl[i,0]
            x[i,1] = tl[i,1]

    ke = np.zeros((3,3))
    
    for j in np.arange(aux) :
        Nhat, DNhat = Tri3NDNHat(x[j,:])
        xhat, N, DN, detJ = Tri3shp(xeset,Nhat,DNhat)
        ke = ke + np.dot(DN,DN.T)*abs(detJ)*wl*0.5*C2
        N = np.mat(N)
    return ke

##########################
def Tri3me(xeset):
    me = np.zeros((3,3))
    tl, wl = Tri3QGauss(2)
    for l in np.arange(tl.shape[0]):
        Nhat, DNhat = Tri3NDNHat([tl[l,0],tl[l,1]])
        xhat, N, DN, detJ = Tri3shp(xeset,Nhat,DNhat)
        me = np.outer(N,N)*wl*detJ*0.5 + me
    return me


##########################
def MeshDomain(Largo,Ancho,ndx,ndy):
    npx = ndx+1
    npy = ndy+1
    xyz = np.zeros(((npx*npy),2))
    aux1 = (ndx)*(ndy)*2
    elem = np.arange(aux1)
    x = np.linspace(0.0,Largo,npx)
    y = np.linspace(0.0,Ancho,npy)
    aux2 = 0
    l = 0
    for j in np.arange(npy) :
        for i in np.arange(npx) :
            l = i+j+aux2
            xyz[l,0] = x[i]
            xyz[l,1] = y[j]

        aux2 = i+aux2
        
    IEN = np.zeros((3,elem.shape[0]),np.int)
    auxp = 0
    auxd = 0
    for j in np.arange(npy-1) :
        for i in np.arange(npx-1) :
            IEN[0,i*2+auxd] = i+auxp
            IEN[1,i*2+auxd] = i+1+auxp
            IEN[2,i*2+auxd] = npx+1+i+auxp
            IEN[0,i*2+1+auxd] = i+auxp
            IEN[1,i*2+1+auxd] = npx+1+i+auxp
            IEN[2,i*2+1+auxd] = npx+i+auxp
        auxp=npx + auxp
        auxd=auxd + ndx*2    
    IEN = IEN+1    
    
    return xyz, IEN

##########################
def Tri3HelmholtzAssembleMKF(xyz, IEN, LM, C2, Mlumped):
    nel, nen = IEN.shape
    neq = LM.max()
    K = np.mat(np.zeros((neq, neq)))
    M = np.mat(np.zeros((neq, neq)))
    for e in np.arange(nel):
        xeset = np.array([xyz[IEN[e,0]-1,:], xyz[IEN[e,1]-1,:], xyz[IEN[e,2]-1,:]])
        ke = Tri3kefePoisson(xeset, C2, 1)
        me = Tri3me(xeset)
        for a in np.arange(nen) :
            A = LM[e,a]
            if A != 0 :
                for b in np.arange(nen) :
                    B = LM[e,b]
                    if B != 0 :
                        K[A-1,B-1] = K[A-1,B-1] + ke[a,b]
                        M[A-1,B-1] = M[A-1,B-1] + me[a,b]
    if Mlumped == True:
        Mlump = np.mat(np.zeros((neq, neq)))
        for i in np.arange(neq):
            Mlump[i,i] = np.sum(M[:,i])
        M = Mlump
    
    return M, K

def Plot2DQuadGeometry(xyz,IEN,nodeId,elemId):
    for i in np.arange(IEN.shape[0]):
        x = np.zeros(4)
        y = np.zeros(4)
        index = IEN[i,0]
        x[0] = xyz[index-1,0]
        y[0] = xyz[index-1,1]
        index = IEN[i,1]
        x[1] = xyz[index-1,0]
        y[1] = xyz[index-1,1] 
        index = IEN[i,2]
        x[2] = xyz[index-1,0]
        y[2] = xyz[index-1,1]
        x_mean = np.mean(x[0:3])
        y_mean = np.mean(y[0:3])
        x[3] = x[0]
        y[3] = y[0]
        plt.plot(x,y,color='black')
        if elemId == True:
            plt.annotate(str(i+1),(x_mean,y_mean))
    for i in np.arange(xyz.shape[0]):
        if nodeId == True:
            plt.plot(xyz[:,0],xyz[:,1],'go')
            plt.annotate(str(i+1),(xyz[i,0],xyz[i,1]))
            for i in np.arange(xyz.shape[0]):
                x = xyz[i,0]
                y = xyz[i,1]        
