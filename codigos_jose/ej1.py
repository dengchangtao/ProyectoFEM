import numpy as np
import matplotlib.pyplot as plt
from helmholtz import *
import anuga
h0=4./9.81
c2=9.81*h0
#omega=[2*3.14
xyz,IEN,ID,LM=MeshDomain(25,26)
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
#plotmany(5,iv2,l2,v2) 
plotmany(15,iv3,l3,v3)