import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from helmholtz import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
import anuga

font = {'size'   : 6}

matplotlib.rc('font', **font)
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
#A2=np.dot(np.linalg.inv(Ml),K)
#A3=invM*K

l1,v1=np.linalg.eig(A1)
#l2,v2=np.linalg.eig(A2)
#l3,v3=np.linalg.eig(A3)
iv1=np.argsort(l1)
#iv2=np.argsort(l2)
#iv3=np.argsort(l3)

def plotmany(nind,iv,l,v):
  for ind in range(nind):
    from scipy.interpolate import griddata
    import numpy as np
    u=np.array(v[:,iv[ind]])[:,0]
    plt.figure()
    x,y=np.meshgrid(np.linspace(0,1.,400),np.linspace(0,1.,200))
    ui=griddata(xyz,u,(x,y))
    #plt.tripcolor(xyz[:,0],xyz[:,1],IEN,u1)
    plt.figure(figsize=(2.3,1.8))
    im=plt.pcolormesh(x,y,ui,cmap=cm.hsv)
    plt.axis('equal')
    T=2.*np.pi/np.sqrt(l[iv[ind]])
    L = T*np.sqrt(c2)
    #plt.title('n=%i  T1=%.3f'%(iv[ind],w ) )
    plt.title('L=%.3f'%L)
    ax=plt.gca()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb=plt.colorbar(im, cax=cax)
    plt.savefig('modonum_%i.png'%ind,dpi=300)
    plt.close()
plotmany(15,iv1,l1,v1)


x=np.linspace(0,1,200)
x,y=np.meshgrid(x,x)
for n in range(5):
  for m in range(5):
    ui=np.cos(n*np.pi*x)*np.cos(m*np.pi*y)
    T=2./np.sqrt(c2)/np.sqrt(n*n+m*m)
    L = T*np.sqrt(c2)
    
    plt.figure(figsize=(2.3,1.8))
    im=plt.pcolormesh(x,y,ui,cmap=cm.hsv)
    plt.axis('equal')
    #plt.title('n=%i  T1=%.3f'%(iv[ind],w ) )
    plt.title('L=%.3f'%L)
    #plt.show()
    ax=plt.gca()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb=plt.colorbar(im, cax=cax)
    plt.savefig('modoanalitico_%i_%i.png'%(n,m),dpi=300)
    plt.close()