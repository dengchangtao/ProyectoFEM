import numpy as np
import matplotlib.pyplot as plt
from helmholtz import *
h0=4./9.81
c2=9.81*h0
N=28
xyz=np.loadtxt('xyz3.txt')
IEN=np.loadtxt('ien3.txt',dtype=np.int32)
LM=np.loadtxt('lm3.txt',dtype=np.int32)

c2=-xyz[:,2]*9.81
xyz = xyz[:,0:2]

plt.tripcolor(xyz[:,0],xyz[:,1],IEN,c2)
plt.triplot(xyz[:,0],xyz[:,1],IEN)
#Tri3SolPlot(xyz,IEN,c2,4)
##plt.show()


faltan = list(set(range(xyz.shape[0]))-set(np.unique(LM)))
plt.scatter(xyz[faltan,0],xyz[faltan,1])
plt.show()

print 'A calcular K,M'
K,M=Tri3HelmholtzAssemble(xyz,IEN,LM,c2)    
print 'M.I*K'
A1=M.I*K
print 'l1,v1'
l1,v1=np.linalg.eig(A1)
iv1=np.argsort(l1)

np.savetxt('l1.txt',l1)
np.savetxt('v1.txt',v1)

#def plotmany(nind,iv,l,v):
  #"""
  #Dibuja desde el vector 0 hasta el nind-1
  #"""
  #import numpy as np
  #for ind in range(nind):    
    #print ind
    #u=np.array(v[:,iv[ind]])[:,0]
    #plt.figure()
    #Tri3SolPlot(xyz,IEN,u,15)
    #plt.axis('equal')
    #plt.axis('off')
    #plt.colorbar()
    #w=2.*np.pi/np.sqrt(l[iv[ind]])
    #plt.title('ind=%i, n=%i  T1=%.3f'%(ind,iv[ind],w ) )
    #plt.savefig('modos%i.png'%ind)
    #plt.close()
#plotmany(1,iv1,l1,v1)

  