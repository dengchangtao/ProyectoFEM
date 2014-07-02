import numpy as np
import scipy.io
import anuga
import matplotlib.pyplot as plt
from matplotlib import rc,cm
font = {'size'   : 6}
rc('font', **font)

#obtener los datos
mat=scipy.io.loadmat('ht.mat')
x = mat['xh'][0,4]
y = mat['yh'][0,4]
x,y = np.meshgrid(x,y)
z = mat['zh'][0,4]
#dibujar para comparar despues

plt.figure()
plt.pcolormesh(x,y,z,cmap=cm.gist_earth)
plt.axis('equal')
#plt.axis('off')
plt.savefig('00bati_original.png',bbox_inches='tight',dpi=300)
#plt.axis('off')
plt.close()

#--------la malla-----------
xa=668400
ya=5945600+550
xb=681300
yb=5955500+200

x0=xa
y0=y.min()
x1=xb
y1=y.min()
x2=32000+x.min()-1000
y2=17500+y.min()
x3=xb
y3=yb
x4=xa
y4=ya
x5=15600+x.min()
y5=9500+y.min()
#el poligono que encierra al dominio
b=[[x0,y0],
  [x1,y1],
  [x2,y2],
  [x3,y3],
  [x4,y4],
  [x5,y5],
  [x0,y0]]
b=np.array(b)

plt.figure()
plt.pcolormesh(x,y,z,cmap=cm.gist_earth)
plt.colorbar()
plt.plot(b[:,0],b[:,1])
plt.contour(x,y,z,[0.],colors='w')
plt.axis('equal')
#plt.axis('off')

plt.savefig('01bati_original+extent+curva0.png',bbox_inches='tight',dpi=300)

plt.close()

bounding_polygon=b[:-1,:]
tags={'left' : 	[3],  'bot' :	[0],'right' :	[1],'top' : [2]} 
#el tama\~no m\'aximo
dx=48*5
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

#archivo .asc con la bati en formato arcview
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


plt.figure()
plt.pcolormesh(x-b[:,0].min(),y-b[:,1].min(),z,cmap=cm.gray)
plt.tripcolor(xt,yt,t,zt,cmap=cm.gist_earth)
plt.contour(x-b[:,0].min(),y-b[:,1].min(),z,[0.],colors='w')
plt.axis('equal')
#plt.axis('off')
plt.savefig('02bati+batitriangular.png',bbox_inches='tight',dpi=300)
plt.close()

#----matrices ID y LM
#criterio: si z[x,y]=0 => no es un grado de libertad
#matriz ID primero


#primero quito losnodos que estan bajo
#un nivel dado, ojal\'a <0
#y ademas quito nodos 'malos', que estan bajo 0
#pero no son de la bah\'ia, sino de la playa
nodosmalos=[14,25,167,166,175,123,74,3373,3383,157,130,116,153,3470,\
  1284,1218,1016,956,970,1119,1009,1122,1123,1124,1479,1411,1685,1997,\
  1224,1994,1636,2827,3070,2953,2974,4768,4744,4733,3366,2968]
nodosbuenos=[]
p=-1
idm=-1*np.ones(xt.shape,dtype=int)
for a in range(xt.shape[0]):
  if zt[a]<-0. and not a in nodosmalos:# and not a in nodosmalos:
    p+=1
    idm[a]=p
    nodosbuenos.append(a)
otrosnodos=np.linspace(0,len(xt)-1,len(xt),dtype=int)
otrosnodos=list(set(otrosnodos)-set(nodosmalos)-set(nodosbuenos))
lm = np.zeros(t.shape)
for e in range(lm.shape[0]):
  for a in range(3):
    A=t[e,a]    
    lm[e,a]=idm[A]

nodosbuenos=list(set(nodosbuenos)-set(nodosmalos))
criterio1=np.nonzero((lm[:,0]>-1))[0]
criterio2=np.nonzero((lm[:,1]>-1))[0]
criterio3=np.nonzero((lm[:,2]>-1))[0]
todos=np.hstack([criterio1,criterio2,criterio3])
indices=np.unique(todos)

#---dibujos
plt.figure()
plt.tripcolor(xt,yt,t[indices,:],zt)
plt.triplot(xt,yt,t[indices,:],linewidth=0.1)
plt.scatter(xt[nodosbuenos],yt[nodosbuenos],s=1.,edgecolor='none',facecolor='k')
plt.scatter(xt[nodosmalos],yt[nodosmalos],s=1.,edgecolor='none',facecolor='r')
plt.scatter(xt[otrosnodos],yt[otrosnodos],s=1.,edgecolor='none',facecolor='b')
plt.axis('equal')
plt.savefig('03bati_gdl.png',dpi=300)
plt.close()
plt.figure(figsize=(24,24))
for a in range(xt.shape[0]):
  if idm[a]>-1:
    plt.text(xt[a],yt[a],'n%i'%a,fontsize=8)    
plt.tripcolor(xt,yt,t[indices,:],zt)
plt.triplot(xt,yt,t[indices,:],linewidth=0.1)
plt.savefig('nodos+text.png',dpi=300)
plt.close()

plt.figure()
criterio4=np.nonzero((lm[:,0]>-1)*(lm[:,1]>-1)*(lm[:,2]>-1))[0]
plt.pcolormesh(x-b[:,0].min(),y-b[:,1].min(),z,cmap=cm.gist_earth)
plt.contour(x-b[:,0].min(),y-b[:,1].min(),z,[0.],colors='w')
plt.triplot(xt,yt,t[criterio4],linewidth=0.3)
plt.axis('equal')
#plt.axis('off')
plt.savefig('04bati+malla.png',bbox_inches='tight',dpi=300)
plt.close()



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



#nodosmalos malla dx=48?
#nodosmalos=[19454,17914,20148,17085,18659,18941,16080,18947, \
  #15443,18361,17155,21533,21185,20914,18311,14573,18355,15563, \
  #20502,21187,21189,21540,22402,22400,22401,21528,21526,25165,\
  #17343,13910,12564,45632,13356,12406,14816,17974,16935,22348,17919,23524,23812,\
  #19134,16601,18401,16158,18751,19494,17521,17542,41113,19010,19005,19003,18999,20237,\
  #17569,17574,19744,41163,17561,19480,19004,17564,10956,41213, 
  #22847, 26930, 44956, 45444, 26609, 25468, 25941, 25632, \
  #26462, 26913, 44938, 24565, 25219, 25623, 42519, 42520, \
  #27942,26281,35234,25235,34690,34668,34512,33625,33584,\
  #34654,33515,34654,34639,43650,44192,44043,36963,38393,\
  #38044,38231,44269,38337,38467,44324,35235]