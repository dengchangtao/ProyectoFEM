import numpy as np
import matplotlib.pyplot as plt
from helmholtz import *
h0=4./9.81
c2=9.81*h0
#omega=[2*3.14

#un circulo
r=np.linspace(0,1,10)
theta=np.linspace(0,2*np.pi,10)
r,theta=np.meshgrid(r,theta)
x=r*np.cos(theta)
y=r*np.sin(theta)
x=x.ravel()
y=y.ravel()
xy=np.vstack([x,y]).T
from scipy.spatial import Delaunay
tri=Delaunay(xy)
plt.triplot(xy[:,0],xy[:,1],tri.vertices)
plt.show()
plt.close()

#otro circulo
N=21
dy=1./(N-1)
dx=1./(N-1)
x=np.array([])
y=np.array([])
for i in range(N):  
  x0=i*dx
  y0=np.arange(0.,np.sqrt(1.-x0**2),dy)
  x0=i*dx*np.ones(y0.shape)
  y=np.append(y,y0)
  x=np.append(x,x0)
#x=np.append(x,-x)
#y=np.append(y,y)
#x=np.append(x,x)
#y=np.append(y,-y)
#x=np.unique(x)
#y=np.unique(y)
xy=np.vstack([x,y]).T
tri=Delaunay(xy)
plt.triplot(xy[:,0],xy[:,1],tri.vertices)
plt.scatter(x,y,edgecolor='none',s=1.)
plt.show()


#----tablas ien,id,lm
IEN = tri.vertices
xyz = tri.points
ID=np.zeros((xyz.shape[0],),dtype=int)
eq=-1#para contar el numero de nodo activo (ecuacion)
for a in range(ID.shape[0]):    
  if True:
    eq+=1
    ID[a]=eq
  else:
    ID[a]=-1. 
#LM
nel=IEN.shape[0]
LM=np.zeros((nel,3),dtype=np.int32) 
for e in range(nel):
  LM[e,:]=[ID[IEN[e,0]], ID[IEN[e,1]], ID[IEN[e,2]] ]  

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

def plotmany(nind,iv,l,v):
  for ind in range(nind):
    from scipy.interpolate import griddata
    import numpy as np
    u=np.array(v[:,iv[ind]])[:,0]
    plt.figure()
    x,y=np.meshgrid(np.linspace(0,1.,400),np.linspace(0,1.,200))
    ui=griddata(xyz,u,(x,y))
    #plt.tripcolor(xyz[:,0],xyz[:,1],IEN,u1)
    plt.pcolormesh(x,y,ui)
    w=2.*np.pi/np.sqrt(l[iv[ind]])
    plt.title('n=%i\t l1=%.3f'%(iv[ind],w ) )
    plt.show()
plotmany(5,iv1,l1,v1)
plotmany(5,iv2,l2,v2) 
plotmany(15,iv3,l3,v3)