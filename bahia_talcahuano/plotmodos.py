import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import cm
from helmholtz import *
#import pypar
#r = pypar.rank()

h0=4./9.81
c2=9.81*h0
N=28
xyz=np.loadtxt('xyz3.txt')
IEN=np.loadtxt('ien3.txt',dtype=np.int32)
LM=np.loadtxt('lm3.txt',dtype=np.int32)

c2=-xyz[:,2]*9.81
xyz = xyz[:,0:2]

l1=np.loadtxt('l1.txt')
v1=np.loadtxt('v1.txt')
iv1=np.argsort(l1)


def plotmany(nind,iv,l,v):
  """
  Dibuja desde el vector 0 hasta el nind-1
  """
  import numpy as np
  for ind in range(nind):   
  #if True:
    print ind
    u=np.array(v[:,iv[ind]])
    plt.figure()
    Tri3SolPlot(xyz,IEN,u,5)
    plt.axis('equal')
    plt.axis('off')
    plt.colorbar()
    w=2.*np.pi/np.sqrt(l[iv[ind]])
    plt.title('n=%i,   Periodo=%.3f [minutos]'%(ind,w/60 ) )
    plt.savefig('modos%i.png'%ind)
    plt.close()
plotmany(4,iv1,l1,v1)
#pypar.finalize()
  
