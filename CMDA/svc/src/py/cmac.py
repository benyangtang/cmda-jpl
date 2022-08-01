'''
kk src7 
cd py
rsync8022 checkNc2.py $cmda4:/home/svc/new_github/CMDA/JPL_CMDA/services/svc/svc/src/py

rsyncec2 cmac.py $ec20:/home/ubuntu/cmac/cmac_docker1/user

''' 

#== def_ferretViewAspect
#== def_ferretPlot  used in universalPlotting6, the linear combination service
#== def_ferretAnomaly
#== def_find_bound(x):
#== def_getRootDir():
#== class_MAPPLOT(): using matplotlib. in universalPlotting6, but not used yet
  #== def_plot(self):
#== def_num2date():


import os
os.environ["PROJ_LIB"] = "/home/ubuntu/miniconda3/envs/FERRET/share/proj"

import traceback
import numpy as np
import matplotlib 
matplotlib.use('Agg')  
import matplotlib.pylab as Mat
Mat.ioff()
from mpl_toolkits.basemap import Basemap


#== def_ferretViewAspect
def ferretViewAspect(runF, isMap, lonS, lonE, latS, latE, viewName):
    #-- aspect_ratio
    import math

    if isMap:
      dLat = float(latE - latS)
      mLat = (latE + latS)/2.0
      dLon = float(lonE - lonS) * math.cos(mLat/180.0*math.pi)

      if dLat/dLon>5 :
        dLon=dLat*0.2
      if dLat/dLon<0.2 :
        dLon=dLat*5.0

    else:
      dLat = 100.0
      dLon = 100.0

    aspect1 = dLat/dLon
    print(('aspect1: '), end=' ')
    print(aspect1)

    marginL = marginR = marginD = marginU = 0.2 * max(dLon, dLat)
    #marginL = 0.2 * dLon
    #marginR = 0.2 * dLon
    #marginD = 0.3 * dLat
    #marginU = 0.2 * dLat
    hor = marginL + dLon + marginR
    vert = marginD + dLat + marginU

    #-- set_viewport
    # to remove the thin white lines. A work around to a Ferret problem
    temp1 = 'set window/outline=0.5/aspect=%.3f '%(vert/hor)
    runF(temp1)

    temp1 = 'def vi/axes/xli=%.4f,%.4f/yli=%.4f,%.4f %s'%(\
              marginL/hor, \
              (marginL+dLon)/hor, \
              marginD/vert, \
              (marginD+dLat)/vert, \
              viewName)
    runF(temp1)

    temp1 = 'set vi %s'%viewName
    runF(temp1)

#== def_ferretPlot
def ferretPlot(runF, plotType, indexStr, varName, d, isMap,lonS,lonE,latS,latE, plotTitle, colorMap, ferretLevel):
    if d>0:
      dStr = 'd=%d '%d
    else:
      dStr = ''

    if dStr=='' and indexStr=='':
      bracketStr = ''
    else: 
      bracketStr = '['
      if dStr != '':
        bracketStr += '%s,'%(dStr)
      if indexStr != '':
        bracketStr += '%s]'%(indexStr)
      else:
        bracketStr += bracketStr[:-1] + ']'

    if plotTitle:
      titleStr = '/title="%s"'%plotTitle
    else:
      titleStr = ''
      
    print(('plotType: '), end=' ')
    print(plotType)
    if plotType=='shade':
      viewName = 'view_99'
      ferretViewAspect(runF, isMap, lonS, lonE, latS, latE, viewName)

      #-- set_pallette
      temp1 = str( 'palette %s'%colorMap )
      runF(temp1)

      #-- set_level
      if len(ferretLevel)>0:
        vminStr = '/level=%s'%(ferretLevel)
      else:
        vminStr = ''

      #-- plot command
      temp1 =  '%s%s%s %s%s'\
        %(plotType, vminStr, titleStr, varName, bracketStr) 
      runF(temp1)

      #-- go_land__
      if isMap==1:
        if plotType in ('contour',):
          temp1 = 'go land blue'
        else:
          temp1 = 'go land'
        runF(temp1)

    #-- plot__
    elif plotType=='plot':
      temp1 = 'plot/symbol=1/line%s %s%s'%(titleStr, varName, bracketStr) 
      runF(temp1)

    elif plotType=='stats':
      temp1 = 'let aa = %s%s'%(varName,bracketStr)
      runF(temp1)

      temp1 = 'let aa1 = floatstr(aa, "(g10.4)")'
      runF(temp1)
      
      temp1 = 'list aa1'
      runF(temp1)

      temp1 = 'plot%s/i=1:100 0*i, 0*i+1'%titleStr
      runF(temp1)
      temp1 = 'label 50,.5,0,0,.2 average=`aa1`'
      #temp1 = 'label 50,.5,0,0,3 aaddfdfdfdf'
      runF(temp1)

#== def_ferretAnomaly(runF, indexStr, varName, d, varNameOut):
def ferretAnomaly(runF, indexStr, varName, d, varNameOut):
    if d>0:
      dStr = 'd=%d '%d
    else:
      dStr = ''

    temp1 = 'USE climatological_axes'
    runF(temp1)
    temp1 = 'CANCEL DATA climatological_axes'
    runF(temp1)

    temp1 = 'define axis/%s:30.436875/units=days tax1'%indexStr
    runF(temp1)

    refStr = 'GT=month_reg@MOD'

    # regrid to monthly
    temp1 = 'let dd1 = %s[gt=tax1, %s]'%(varName,dStr)
    runF(temp1)

    # regrid to monthly climatology
    temp1 = 'let dd2c = dd1[%s]'%refStr
    runF(temp1)

    #temp1 = 'let dd1b = dd1[t=@ave]'
    #runF(temp1)

    # regrid the climatology to monthly
    temp1 = 'let dd2ca = dd2c[gt=tax1]'
    runF(temp1)

    # calc anomaly
    temp1 = 'let dd1a = dd1 - dd2ca'
    runF(temp1)

    # define new var for anomaly
    temp1 = 'define var/bad=-999999.0/title="`%s.long_name`"/units="`%s.units`" %s = dd1a'%(
      varName,
      varName,
      varNameOut,
      )
    runF(temp1)

#== def_getRootDir():
def getRootDir():
  # use data.cfg to set the data root dir.

  # assuming the cwd is where this code file is
  cwd = os.getcwd()
  cmacDir = os.path.abspath(os.path.join(cwd, '../../../../../..'))
  configFile = os.path.join(cmacDir, 'JPL_CMDA/services/svc/data.cfg')
  desDir = os.path.join(cmacDir, 'JPL_CMDA/services/svc/svc/src/des')
  print(('cmacDir: '), end=' ') 
  print(cmacDir)
  print(('desDir: '), end=' ') 
  print(desDir)
  print(('configFile: '), end=' ') 
  print(configFile)

  # if not, use 'services' to figure it out  
  if not os.path.isfile(configFile):
    print('use "JPL-CMDA" to figure out')
    cwd = os.getcwd()
    print(('in getRootDir, cwd: '), end=' ') 
    print(cwd)
    #ind1 = cwd.find('services')
    ind1 = cwd.find('JPL_CMDA')
    if ind1>-1:
      cmacDir = cwd[:(ind1-1)]
      print(('cmacDir: '), end=' ') 
      print(cmacDir)
      #configFile = os.path.join(cmacDir, 'services/svc/data.cfg')
      configFile = os.path.join(cmacDir, 'JPL_CMDA/services/svc/data.cfg')
      print(('configFile: '), end=' ') 
      print(configFile)
      desDir = os.path.join(cmacDir, 'JPL_CMDA/services/svc/svc/src/des')
      print(('desDir: '), end=' ') 
      print(desDir)

    if not os.path.isfile(configFile):
      print(('failed to find data.cfg: %s'%(configFile)))
      return None 
    
  if not os.path.isfile(configFile):
    print(('Check again. failed to find data.cfg: %s'%(configFile)))
    return None 
    
  try:
    temp1 = open(configFile).read() 
    print(('temp1: '), end=' ') 
    print(temp1)
    if temp1[-1]=='\n':
      temp1 = temp1[:-1]
    if temp1[-1]=='/':
      temp1 = temp1[:-1]
    # zzzz
    #if os.path.isdir(temp1):
    if 1:
      dataDir = temp1 + '/cmip5' 
      #a.dataDir = temp1  # should change to this when data.cfg is without 'cmip5'
      return dataDir, cmacDir, desDir
        
  except:
    traceback.print_exc()
    print('failed to read data.cfg.')
    return None

  print('failed to get data.cfg.')
  return None

#== def_find_bound(x):
# for used in matplotlib as axis variable
def find_bound(x, min1=None, max1=None):
  '''
Modify x so it becomes the end points.
'''
  temp1 = np.zeros((len(x)+1,), dtype=x.dtype)
  temp1[1:-1] = (x[1:,]+x[:-1])/2.
  temp1[0] = x[0] - (temp1[1]-x[0])
  temp1[-1] = x[-1] + (x[-1] - temp1[-2])

  if min1:
    temp1[0] = max(temp1[0], min1)
  if max1:
    temp1[-1] = min(temp1[-1], max1)

  return temp1


#== class_MAPPLOT():  in universalPlotting6, but not used yet
class MAPPLOT():
  def __init__(self):

    self.data1 = None

    self.lon1 = None
    self.lat1 = None

    self.vmin1 = None
    self.vmax1 = None

    self.xLable = None
    self.yLable = None
    self.title = None

    self.plotH = None

    self.outFile = None

  #== def_plot(self):
  def plot(self):
    # convert lon/lat for calling pcolor()
    lon2 = find_bound(self.lon1)
    lat2 = find_bound(self.lat1)

    lat2[0] = max(-90, lat2[0])
    lat2[-1] = min(90, lat2[-1])

    # aspect ratio
    lat12 = (self.lat1[0] + self.lat1[-1])/2.0
    aspect1 = (self.lat1[-1]-self.lat1[0]) / (self.lon1[-1]-self.lon1[0])*np.cos(np.pi*lat12/180.0)
    aspect2 = np.cos(np.pi*lat12/180.0)
    self.plotW = min( self.plotH/aspect1, 12)

    print((self.lat1[-1]))
    print((self.lat1[0]))
    print(aspect1)
    print(('plotW, plotH: '), end=' ')
    print((self.plotW), end=' ') 
    print((self.plotH))

    # calc data range
    print(('self.vmin1, vmax1: '), end=' ')
    print((self.vmin1))
    print((self.vmax1))
    if self.vmin1 is None:
      self.vmin1 = self.data1.min()
      self.vmax1 = self.data1.max()
    print(('self.vmin1, vmax1: '), end=' ')
    print((self.vmin1))
    print((self.vmax1))

    # start plotting
    #f1 =Mat.figure(figsize=(self.plotW, self.plotH))
    f1 =Mat.figure(figsize=(14, 10))

    m = Basemap(lon2[0], lat2[0], lon2[-1], lat2[-1], 
         resolution='c', suppress_ticks=False)
    im = m.pcolor(lon2, lat2, self.data1, vmin=self.vmin1, vmax=self.vmax1, shading='flat', cmap='gist_rainbow')
    ax1 = Mat.gca()
    Mat.setp(ax1, aspect=1./aspect2)
    m.drawcoastlines(color=(.7,.7,.7))

    # title, labels
    Mat.title(self.title)
    Mat.xlabel(self.yLabel)
    Mat.ylabel(self.xLabel)
    labels = ax1.get_xticklabels()
    Mat.setp(labels, rotation=45, fontsize=10)

    # colorbar
    hc = Mat.colorbar(orientation='horizontal')

    # save to file
    Mat.savefig(self.outFile, dpi=300)
    
#== class_ANOMALY():
#class ANOMALY():
#  def __init__(self):
#    self.data1 = None
#    self.data2 = None
#
#    self.time1 = None
#    self.time2 = None

#== def_num2date():
def num2date(netCDF4, num1, units1):

  date1 = None
  aa = units1.split()
  if aa[0] in ('month', 'months'): 
    aa[0] = 'day'
    units1a = ' '.join(aa)
    if 0:  # why this not working?
      units1a = units1
      units1a.replace(a[0], 'day')
    #print('units1a')
    #print(units1a)
    #print(aa)
    try:
      date1 = netCDF4.num2date(num1*30, units1a, calendar='360_day')
    except:
      print((traceback.format_exc())) 

  else:
    timeOk = 1
    try:
      date1 = netCDF4.num2date(num1, units1)
    except:
      print((traceback.format_exc())) 
      timeOk = 0

    if not timeOk:
      timeOk = 1
      try:
        date1 = netCDF4.num2date(num1, units1, calendar='365_day')
      except:
        print((traceback.format_exc())) 
        timeOk = 0

  return date1

