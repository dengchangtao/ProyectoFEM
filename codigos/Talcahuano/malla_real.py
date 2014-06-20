import numpy as np
import scipy.io
import anuga
import matplotlib.pyplot as plt

#obtener los datos
mat=scipy.io.loadmat('ht.mat')
x = mat['xh'][0,4]
y = mat['yh'][0,4]
x,y = np.meshgrid(x,y)
z = mat['zh'][0,4]
#dibujar para comparar despues
plt.pcolormesh(x,y,z)
plt.axis('equal')
plt.savefig('00bati_original.png')

plt.axis('off')
plt.tight_layout()
plt.close()

#--------la malla-----------
bounding_polygon=[[x.min(),y.min()],
		    [x.max(),y.min()],
		    [x.max(),y.max()],
		    [x.min(),y.max()]]
tags={'left' : 	[3],  'bot' :	[0],'right' :	[1],'top' : [2]} 
#el tama\~no m\'aximo
dx=48*3
anuga.create_mesh_from_regions(bounding_polygon,
				    boundary_tags=tags,
				    maximum_triangle_area=dx*dx,     
				    filename='talcahuano4.msh',
				    use_cache=False,
				    verbose=True)


#----------la batimetria------------

#archivo con info de la proyeccion
sprj='Projection    UTM \n'+ \
'Zone          55\n'+\
'Datum         WGS84\n'+\
'Zunits        NO\n'+\
'Units         METERS\n'+\
'Spheroid      WGS84\n'+\
'Xshift        500000\n'+\
'Yshift        10000000\n'+\
'Parameters'
fprj=open('talcahuano4.prj','w')
fprj.write(sprj)
fprj.close()

#archivo con .asc con la bati en formato arcview
nx=len(mat['xh'][0,4][0])
ny=len(mat['yh'][0,4][0])
f=open('talcahuano4.asc','w')
f.write('ncols\t%i\n'%(nx))
f.write('nrows\t%i\n'%(ny))
f.write('xllcorner\t%.2f\n'%(x.min()))
f.write('yllcorner\t%.2f\n'%(y.min()))
f.write('cellsize\t%.2f\n'%(54.))
f.write('NODATA_value\t-9999\n')
for j in range(ny):
  s=''
  for i in range(nx):
    s+='%.7f '%z[ny-j-1,i]
  f.write('%s\n'%s)
f.close()
anuga.asc2dem('talcahuano4.asc', use_cache=True, verbose=True)
anuga.dem2pts('talcahuano4.dem')

#ahora quiero sacar la triangulacion e interpolacion
domain = anuga.Domain('talcahuano4.msh', use_cache=False, verbose=True)
domain.set_quantity('elevation', filename='talcahuano4.pts')
t=domain.get_triangles()
xy=domain.get_nodes()
xt,yt,zt,t=domain.get_quantity('elevation').get_vertex_values()

#plt.triplot(xy[:,0],xy[:,1],t)
plt.tripcolor(xt,yt,t,zt)
plt.axis('equal')
plt.savefig('01bati_triangular.png')
plt.close('all')

plt.figure(figsize=(16.,16.))
plt.tripcolor(xt,yt,t,zt)
plt.triplot(xt,yt,t,linewidth=0.5)
plt.axis('equal')
plt.xlim(10000.,20000.)
plt.ylim(5000,25000)
plt.savefig('02bati_triangular_zoom.png')
plt.close()
#----matrices ID y LM
#criterio: si z[x,y]=0 => no es un grado de libertad
#matriz ID primero
nodosmalos=[19454,17914,20148,17085,18659,18941,16080,18947, \
  15443,18361,17155,21533,21185,20914,18311,14573,18355,15563, \
  20502,21187,21189,21540,22402,22400,22401,21528,21526,25165,\
  17343,13910,12564,45632,13356,12406,14816,17974,16935,22348,17919,23524,23812,\
  19134,16601,18401,16158,18751,19494,17521,17542,41113,19010,19005,19003,18999,20237,\
  17569,17574,19744,41163,17561,19480,19004,17564,10956,41213, 
  22847, 26930, 44956, 45444, 26609, 25468, 25941, 25632, \
  26462, 26913, 44938, 24565, 25219, 25623, 42519, 42520, \
  27942,26281,35234,25235,34690,34668,34512,33625,33584,\
  34654,33515,34654,34639,43650,44192,44043,36963,38393,\
  38044,38231,44269,38337,38467,44324,35235]
p=-1
idm=-1*np.ones(xt.shape,dtype=int)
for a in range(xt.shape[0]):
  if zt[a]<-0.1 and not a in nodosmalos:
    p+=1
    idm[a]=p
#gdl=np.nonzero(zt<-0.1)[0]
#p=np.linspace(0,len(gdl)-1,len(gdl),dtype=int)
#idm[gdl]=p
#matriz LM
lm = np.zeros(t.shape)
for e in range(lm.shape[0]):
  for a in range(3):
    A=t[e,a]    
    lm[e,a]=idm[A]
    
criterio1=np.nonzero((lm[:,0]>-1))[0]
criterio2=np.nonzero((lm[:,1]>-1))[0]
criterio3=np.nonzero((lm[:,2]>-1))[0]
todos=np.hstack([criterio1,criterio2,criterio3])
indices=np.unique(todos)
plt.tripcolor(xt,yt,t[indices,:],zt)
plt.triplot(xt,yt,t[indices,:],linewidth=0.1)
plt.axis('equal')
plt.savefig('03bati_triangular_gdls.png')
plt.close()

plt.figure(figsize=(12.,12.))
plt.tripcolor(xt,yt,t[indices,:],zt)
plt.triplot(xt,yt,t[indices,:],linewidth=0.2)
plt.savefig('04bati_triangular_gdls_filtrada.png')
#for a in range(xt.shape[0]):
  #if idm[a]>-1 and xt[a]>31000 and xt[a]<32000 and yt[a]>14000 and yt[a] < 18000:
  ##and xt[a]>20000 and xt[a]<28000 and yt[a]<8000 and yt[a]>0:
    #print a,idm[a]
    #plt.text(xt[a],yt[a],'n%i'%a,fontsize=12)    
plt.scatter(xt[nodosmalos],yt[nodosmalos],c='r',facecolors='none')
plt.savefig('06bati_nodos_malos.png')
plt.close('all')

#escribir a archivos
fxyz = open('xyz.txt','w')
fid = open('id.txt','w')
for a in range(xt.shape[0]):
  fxyz.write('%3.14e %3.14e %3.14e\n'%(xt[a],yt[a],zt[a]))
  fid.write('%i\n'%idm[a])
fxyz.close()
fid.close()

fien = open('ien.txt','w')
flm  = open('lm.txt','w')
for e in range(lm.shape[0]):
  fien.write('%i %i %i\n'%(t[e,0],t[e,1],t[e,2]))
  flm.write('%i %i %i\n'%(lm[e,0],lm[e,1],lm[e,2]))
fien.close()
flm.close()

xyz= np.loadtxt('xyz.txt')
ID = np.loadtxt('id.txt')
IEN = np.loadtxt('ien.txt')
LM = np.loadtxt('lm.txt')

