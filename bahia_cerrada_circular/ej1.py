import numpy as np
import matplotlib.pyplot as plt
from helmholtz import *
h0=4./9.81
c2=9.81*h0
N=28
xyz=np.loadtxt('xyz%i.txt'%N)
IEN=np.loadtxt('ien%i.txt'%N,dtype=np.int32)
LM=np.loadtxt('lm%i.txt'%N,dtype=np.int32)

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
  """
  Dibuja desde el vector 0 hasta el nind-1
  """
  import numpy as np
  for ind in range(nind):    
    print ind
    u=np.array(v[:,iv[ind]])[:,0]
    plt.figure()
    Tri3SolPlot(xyz,IEN,u,15)
    plt.axis('equal')
    plt.axis('off')
    plt.colorbar()
    w=2.*np.pi/np.sqrt(l[iv[ind]])
    plt.title('ind=%i, n=%i  T1=%.3f'%(ind,iv[ind],w ) )
    plt.savefig('modos%i.png'%ind)
    plt.close()
plotmany(10,iv3,l3,v3)

  