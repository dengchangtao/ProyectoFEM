from clawpack.visclaw.data import ClawPlotData
from clawpack.visclaw import frametools
import matplotlib.pyplot as plt
plotdata = ClawPlotData()
plotdata.outdir = '_output'
plotdata.plotdir = '_plots'

frame=plotdata.getframe(0)

toplotlevel=[1]
plt.figure()
for patch in frame.domain.patches:
  print patch.level
  #if grid.level in toplotlevel:
  
    
    
#Traceback (most recent call last):
File "/home/jose/clawpack-5.1.0//visclaw/src/python/visclaw/plotclaw.py", line 58, in <module>
  plotclaw(sys.argv[1], sys.argv[2], sys.argv[3])

File "/home/jose/clawpack-5.1.0//visclaw/src/python/visclaw/plotclaw.py", line 47, in plotclaw
  plotpages.plotclaw_driver(plotdata, verbose=False, format=format)
File "/home/jose/clawpack-5.1.0/clawpack/visclaw/plotpages.py", line 1806, in plotclaw_driver
  frametools.plotframe(frameno, plotdata, verbose)

File "/home/jose/clawpack-5.1.0/clawpack/visclaw/frametools.py", line 71, in plotframe
  plot_frame(framesolns, plotdata, frameno,verbose=verbose)
File "/home/jose/clawpack-5.1.0/clawpack/visclaw/frametools.py", line 253, in plot_frame
  current_data = plotitem_fun(framesoln,plotitem,current_data,stateno)
File "/home/jose/clawpack-5.1.0/clawpack/visclaw/frametools.py", line 623, in plotitem2
  var  = get_var(state,pp['plot_var'],current_data)
File "/home/jose/clawpack-5.1.0/clawpack/visclaw/frametools.py", line 920, in get_var
  var = plot_var(current_data)
File "/home/jose/clawpack-5.1.0/clawpack/visclaw/geoplot.py", line 180, in surface
  h = q[0,:,:]
  