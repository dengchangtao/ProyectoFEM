
"""
Module to create topo and qinit data files for this example.
"""

from clawpack.geoclaw import topotools
import numpy as np

T=2.
lx=10.
ly=lx/20.
h=1./9.81*(2*lx/T)**2
dx=0.01*lx

#caso 1
#xl=0.
#xr=lx
#yl=0.
#yu=ly
#nx=int(lx/dx)+1
#ny=int(ly/dx)+1

#caso 2
xl=-lx
xr=lx
yl=-10*ly
yu=10*ly
nx=int((xr-xl)/dx)+1
ny=int((yu-yl)/dx)+1

#caso3
#xl=0.
#xr=lx
#yl=0.
#yu=ly*5
#nx=int((xr-xl)/dx)+1
#ny=int((yu-yl)/dx)+1


def maketopo():
    """
    Output topography file for the entire domain
    """
    nxpoints = nx
    #nypoints = nxpoints/4+1
    nypoints= ny
    xlower = xl
    xupper = xr
    ylower = yl
    yupper = yu
    
    outfile= "bati.tt2"     
    topotools.topo2writer(outfile,topo2,xlower,xupper,ylower,yupper,nxpoints,nypoints)

def makeqinit():
    """
    Create qinit data file
    """
    nxpoints = nx
    #nypoints = nxpoints/4+1
    nypoints= ny
    xlower = xl
    xupper = xr
    ylower = yl
    yupper = yu
    outfile1= "q0.xyz"     
    topotools.topo1writer(outfile1,qinit,xlower,xupper,ylower,yupper,nxpoints,nypoints)
    
def qinit(x,y):
  """ solo me aseguro
  que x>14. quede seco 
  """
  import numpy as np
  z=np.zeros(x.shape)
  return z
def topo(x,y):
  z=-h*np.ones(x.shape)
  return z

def topo2(x,y):
  z=-h*np.ones(x.shape)
  z=np.where( (x>=0.)*(y>ly/2),20.,z)
  z=np.where( (x>=0.)*(y<-ly/2),20.,z)
  z=np.where((x<=0.),-1000,z)
  return z

  
if __name__=='__main__':
    maketopo()
    makeqinit()
