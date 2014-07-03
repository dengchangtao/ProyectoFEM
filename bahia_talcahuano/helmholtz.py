import numpy as np
def Tri3QGauss(k):  
  """
  Puntos de cuadratura de gauss2d para Tri3
  in: k = grado de exactitud
  out: t1=puntos
  out: w1=pesos
  """
  if k==1:
    t1=[[1./3.,1./3.,1./3.]]
    w1=[1.]
  elif k==2:
    t1=[[2./3.,1./6.,1./6.],\
      [1./6.,2./3.,1./6.],\
      [1./6.,1./6.,2./3.]]
    w1=[1./3.,1./3.,1./3.]
  return np.array(t1),np.array(w1)

def Tri3NDhat(xi):
  """
   Funciones  de forma dominio standard
   evaluadas en xi
   in: xi= punto del dominio estandard
   out: Nhat = Nhat(xi)
   out: DNhat = grad_xi Nhat
  """
  nen=3
  Nhat=[xi[0],xi[1],1-xi[0]-xi[1]]
  DNhat=[[1.,0.],[0.,1.],[-1.,-1.]]
  return np.array(Nhat),np.array(DNhat)
def Tri3shp(xeset,Nhat,DNhat):
  """
    Para pasar Nhat,DNhat de dominio standard a real
    in: xeset=vertices del triangulo
    in: Nhat=Nhat(xi)
    in: DNhat=grad_xi Nhat(xi)
    out: xhat = x(xi)
    out: N=N(x)
    out: DN=grad N (x)
    out: detJ
  """
  nen=len(xeset)
  ndim=DNhat[0,:].size
  xhat=0.
  J=np.matrix(np.zeros((ndim,ndim)))
  DN=np.zeros(DNhat.shape)
  for a in range(nen):
    xhat+=Nhat[a]*xeset[a]
    J+=np.outer(xeset[a,:],DNhat[a,:])  
  detJ=np.linalg.det(J)
  G=J.I
  for a in range(nen):
    DN[a,:]=np.dot(DNhat[a,:],G)
  N=Nhat  
  return xhat,N,DN,detJ

def Tri3keHelmholtz(xeset,c2e,k):
  """
    Integra con precision k
    fe y ke, usando cuadratura de Gauss
    
    in: xeset	= vertices del triangulo
    in: kappa	=t ensor de cond termica (matrix like)
    in: f 	= fuente en el elemento (float)
    in: k	= precision de las integrales (int)
    out: ke	= matriz de rigidez  (matrix)
    out: fe	= vector lado derecho (array)
  """
  xq,wq= Tri3QGauss(k)
  nen=len(xeset)
  ke=np.matrix(np.zeros((nen,nen))) 
  for iq in range(xq.shape[0]):
    Nhat,DNhat=Tri3NDhat([xq[iq,0],xq[iq,1]])
    xhat,N,DN,detJ=Tri3shp(xeset,Nhat,DNhat)
    B=np.matrix(DN).T
    #print '-------------B\n',B
    #print '----------kappa\n',c2
    c2 = Tri3SquareCelerity(N,c2e)
    ke+=0.5*wq[iq]*B.T*c2*B*np.abs(detJ)
  return ke
def Tri3SquareCelerity(N,c2e):
  c2e = np.array(c2e)
  c2 = 0.
  for a in range(c2e.shape[0]):
    c2+=N[a]*c2e[a]
  return c2
  
def Tri3me(xeset,rho):
  """
    me = int( rho* outer( N(x(xi)), N(x(xi)))* detJ} )
  """
  tl,wl=Tri3QGauss(2)
  nl=len(wl)
  nen=xeset.shape[0]
  me=np.zeros((nen,nen))
  for l in range(nl):
    Nhat,DNhat = Tri3NDhat(tl[l,:])    
    xhat,N,DN,detJ = Tri3shp(xeset,Nhat,DNhat)
    me+=0.5*rho*np.outer(N,N)*abs(detJ)*wl[l]
  return me

def MeshDomain(ndx,ndy):
  """
    Para crear las malla xyz y 
    las tablas IEN,ID,LM
    La malla divide cada cuadrado del
    meshgrid en 2, pero alternadamente,
    para no dar preferencia a una direccion.
    Se ve como rectangulos cruzados asi.
    
    Se pueden 'ajustar' los ifelse para 
    orientar todos los triangulos para un mismo lado
    (las diagonales-hipotenusas)
  """
  #los puntos
  x=np.linspace(0.,1.,ndx)
  y=np.linspace(0.,1.,ndy)
  x,y=np.meshgrid(x,y)
  x=x.ravel()
  y=y.ravel()
  xyz=np.vstack([x,y]).T
  
  #IEN
  nel=2*(ndx-1)*(ndy-1)#
  IEN=np.zeros((nel,3),dtype=np.int32)
  
  for j in range(ndy-1):
    for i in range(ndx-1):
      e=2*j*(ndx-1)+i
      n=j*ndx+i
      if np.mod(j,2)==0: #and False: # True:
	if np.mod(i,2)==0:# and False:
	  IEN[e,:]=[n,n+1,n+ndx+1]
	  IEN[e+ndx-1]=[n,n+ndx,n+ndx+1]
	else:
	  IEN[e,:]=[n,n+1,n+ndx]
	  IEN[e+ndx-1]=[n+1,n+ndx,n+ndx+1]
      else:	
	if np.mod(i,2)==0: # True:
	  IEN[e,:]=[n,n+1,n+ndx]
	  IEN[e+ndx-1]=[n+1,n+ndx,n+ndx+1]
	else:
	  IEN[e,:]=[n,n+1,n+ndx+1]
	  IEN[e+ndx-1]=[n,n+ndx,n+ndx+1]

	  
  #ID
  ID=np.zeros((ndx*ndy,))
  eq=-1#para contar el numero de nodo activo (ecuacion)
  for a in range(ndx*ndy):    
    if True:
      eq+=1
      ID[a]=eq
    else:
      ID[a]=-1.    
  
  #LM
  LM=np.zeros((nel,3),dtype=np.int32) 
  for e in range(nel):
    LM[e,:]=[ID[IEN[e,0]], ID[IEN[e,1]], ID[IEN[e,2]] ]  
  return xyz,IEN,ID,LM

def Tri3HelmholtzAssemble(xyz,IEN,LM,c2):
  """
    Ensambla la matriz K,F globales
  """
  nel=IEN.shape[0]
  nen=IEN.shape[1]
  neq=LM.max()+1
  K=np.zeros((neq,neq))
  M=np.zeros((neq,neq))
  F=np.zeros((neq,))
  for e in range(nel):
    xeset=np.array([xyz[i] for i in IEN[e,:]])
    c2e = np.array([c2[i] for i in IEN[e,:]])
    ke=Tri3keHelmholtz(xeset,c2e,1)
    me = Tri3me(xeset,1.)
    for a in range(nen):
      A=LM[e,a]
      if A != -1:
	for b in range(nen):
	  B=LM[e,b]
	  if B != -1:
	    K[A,B]+=ke[a,b]
	    M[A,B]+=me[a,b]
  return np.matrix(K),np.matrix(M)

def Tri3SolPlot(xyz,IEN,u,Ninterp):
  #creo los xi de elemento isoparametrico
  from scipy.interpolate import griddata
  import numpy as np
  import matplotlib.pyplot as plt
  from matplotlib import cm
  xi1=np.linspace(0,1.,Ninterp)
  xi2=np.linspace(0,1.,Ninterp)
  xi1,xi2=np.meshgrid(xi1,xi2)
  for i in range(xi1.shape[1]):
    xi2[:,i]=np.linspace(0.,1-xi1[0,i],Ninterp)
  for e in range(IEN.shape[0]):
    xeset=xyz[IEN[e,:],:]
    ueset=u[IEN[e,:]]
    x1=0.*xi1
    x2=0.*xi2
    for a1 in range(xi1.shape[0]):
      for a2 in range(xi1.shape[1]):
	Nhat, DNhat = Tri3NDhat([xi1[a1,a2],xi2[a1,a2]])
	xhat,N,DN,detJ = Tri3shp(xeset, Nhat, DNhat)
	x1[a1,a2]=xhat[0]
	x2[a1,a2]=xhat[1]
    uinterp=griddata(xeset,ueset,(x1,x2))
    p=plt.pcolormesh(x1,x2,uinterp,vmin=u.min(),vmax=u.max(),cmap=cm.hsv)
  return p