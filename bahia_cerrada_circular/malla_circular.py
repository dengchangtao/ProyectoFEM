import numpy as np
import scipy.io
import anuga
import matplotlib.pyplot as plt
from matplotlib import rc,cm
font = {'size'   : 6}
rc('font', **font)

#obtener los datos
#--------la malla-----------
for N in range(4,132,8):
  #N=16
  dx=2*np.pi/N
  theta = np.linspace(0,2*np.pi-dx,N) # cada 18 grados

  xbound = np.cos(theta)
  ybound = np.sin(theta)
  b = np.vstack([xbound,ybound]).T


  bounding_polygon=list(b)
  tags={'borde' : range(b.shape[0]) } 
  #el tama\~no m\'aximo

  anuga.create_mesh_from_regions(bounding_polygon,
				      boundary_tags=tags,
				      maximum_triangle_area=dx*dx,     
				      filename='circulo.msh',
				      use_cache=False,
				      verbose=False)

  #ahora quiero sacar la triangulacion e interpolacion
  domain = anuga.Domain('circulo.msh', use_cache=False, verbose=False)
  t=domain.get_triangles()
  xy=domain.get_nodes()
  
  id1 = np.linspace(0,xy.shape[0],xy.shape[0]+1)
  lm = np.zeros(t.shape)
  for e in range(lm.shape[0]):
    for a in range(2):
      A=t[e,a]    
      lm[e,a]=id1[A]
  np.savetxt('xyz%i.txt'%N,xy)
  np.savetxt('id%i.txt'%N,id1)
  np.savetxt('lm%i.txt'%N,lm)
  np.savetxt('ien%i.txt'%N,t)  
  plt.figure()
  plt.triplot(xy[:,0],xy[:,1],t)
  plt.plot(xbound-xbound.min(),ybound-ybound.min())
  plt.axis('equal')
  plt.axis('off')
  print t.shape,N
  plt.title('N=%i, nel=%i'%(N,t.shape[0]))
  plt.savefig('circulo%i.png'%N)
  plt.close()