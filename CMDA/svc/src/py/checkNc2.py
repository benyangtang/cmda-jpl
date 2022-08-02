'''
xxxx  -- attention

rsyncec2 /home/btang/projects/cmda1/CMDA/svc/src/py/checkNc2.py $ec21:/home/ubuntu/CMDA0/svc/src/py 

kk src7 
cd py
rsync8022 checkNc2.py cmac.py $cmda4:/home/svc/new_github/CMDA/JPL_CMDA/services/svc/svc/src/py

rsync8022 checkNc2.py $cmda4:/home/svc/new_github/CMDA/JPL_CMDA/services/svc/svc/src/py
 

'''
# import__
#== providers_models
# def_checkNc_w(nc, fn, dict1):
# def_checkNc(fn, dict1):
  # loop_vars
    # find_units
    # find_longname
    # collect_dims

    # if_hasUnits
      # replace_ref_time_of 0000
    # dim_range
  # collect_vars
  # collect_the_real dim
  # check_dimList
      # check_time_limits
  # construct_dim2

# import__
from netCDF4 import Dataset
from netCDF4 import MFDataset
import netCDF4 
import os, sys
#import cf_units as cf
import cfunits as cf1
import copy
import glob
import traceback
myPyDir = '/home/ubuntu/CMDA0/svc/src/py'
sys.path.insert(0, myPyDir)
#from . import cmac
import cmac

vb = 1

#== providers_models
sources = {
'staged',
'online',
'uploaded',
}

providers = {
'tkubar': 'T. Kubar',
'fli': 'F. Li',
'noaa': 'NOAA',
'inm': 'INM',
'wcrp': 'WCRP',
'wrf': 'WRF',
'ecmwf': 'ECMWF',
'fub-dwd': 'FUB-DWD',
'bcc': 'BCC',
'nasa': 'NASA',
'uoe': 'UOE',
'ukmo': 'UKMO',
'iap': 'IAP',
'giss': 'GISS',
'mpi': 'MPI',
'argo': 'ARGO',
'ncc': 'NCC',
'cnrm': 'CNRM',
'ipsl': 'IPSL',
'cccma': 'CCCMA',
'miroc': 'MIROC',
'mri': 'MRI',
'ncar': 'NCAR',
'csiro': 'CSIRO',
'cmcc': 'CMCC',
'gfdl': 'GFDL',
}

models = [
'TRMM-L3',
'IPSL-CM5A-LR',
'ECMWF_interim',
'ERA_interim',
'GFDL-ESM2G',
'SSMI-MERIS',
'GFDL-CM3',
'GISS-E2-H',
'GISS-E2-R',
'FGOALS-s2',
'PSL-CM5A-LR',
'MIROC5',
'MIROC4h',
'MPI-ESM-LR',
'MRI-CGCM3',
'MODIS',
'TRMM',
'CESM1-CAM5',
'NorESM1-ME',
'NorESM1-M',
'NOAA',
'HadGEM2-A',
'HadGEM2-ES',
'ATSR',
'ISCCP',
'ARGO',
'CanESM2',
'CanAM4',
'CNRM-CM5',
'CSIRO-MK3-6-0',
'CMCC-CM',
'NCC-NORESM',
'bbc-csm1-1',
'inmcm4',
'CM3',
'CM5A-LR',
'MIROC5',
'HadGEM2-A',
'CM5',
'SSMI-MERIS',
'ESM-LR',
'CGCM3',
'GRACE',
'AMSRE',
'MLS',
'AIRS',
'GPCP-SG',
'CERES-SG',
'CERES-EBAF',
'QuikSCAT',
'AVISO',
'cloudSat-CALIPSO',
'MISR',
'2C-ICE',
'TES',
'CALIOP',
'CALIOP-GOCCP-v2.1',
'CESM1-CAM5',
'ARGO',
#
'wrf_st',
'wrf_ra-cam',
'wrf_pbl-ysu',
'wrf_pbl-nn2',
'wrf_mp-wdm',
'wrf_mp-mor',
'wrf_co-kf',
'wrf_co-tie',
'wrf_st',
#
'bcc-csm1-1',
'inmcm4',
]

models2 = {}
for mod1 in models:
  #models2[mod1] =  ['-' + mod1.lower() + '_', '_' + mod1.lower() + '_']
  models2[mod1] =  '_' + mod1.lower() + '_'

experiments = [
'historical',
'esmHistorical',
'historicalExt',
'amip',
'amip4XCO2',
'obs4MIPs',
]

experiments2 = {}
for exp1 in experiments:
  experiments2[exp1] =  '_' + exp1.lower() + '_' 

runs = [
'r1i1p1',
]

runs2 = {}
for rr in runs:
  runs2[rr] =  '_' + rr.lower() + '_' 

def num2dateStr(num1, units9):
  timeOk = 1
  try:
    time1 = netCDF4.num2date(num1, units9).timetuple()
  except:
    print((traceback.format_exc())) 
    timeOk = 0

  if not timeOk:
    timeOk = 1
    try:
      time1 = netCDF4.num2date(num1, units9, calendar='365_day').timetuple()
    except:
      print((traceback.format_exc())) 
      timeOk = 0

  if not timeOk:
    timeOk = 1
    try:
      time1 = cmac.num2dateMonth(netCDF4,num1*30, units9).timetuple()
    except:
      print((traceback.format_exc())) 
      timeOk = 0
  return time1


# def_checkNc_w(nc, fn, dict1):
def checkNc_w(nc, fn, dict1):
  print('in checkNc_w')
  nc.close()
  # call checkNc(overwrite=1)
  ok1 = checkNc(fn, dict1, overwrite=1)
  return ok1

# def_checkNc(fn, dict1):
def checkNc(fn, dict1, overwrite=0, allowOverwrite=1, vb=0):
  '''
return ok1:
0 -- good
1 -- dimension is not a var itself
2 -- dimension has no units
3 -- dimension units not recognized
4 -- ref time is 0000
5 -- cannot open file
6 -- make up dim as 'i'
11-- 2d dim
12-- dimension is not a var itself. same as 1?

'''
  ok1 = 0
  dict9 = copy.deepcopy(dict1)

  varList = []
  varDict = {}
  check1 = ''
  warning = ''

  if fn.find('*')>-1:
    fn2 = glob.glob(fn)
  else:
    fn2 = [fn,]

  if 0:
    temp2 = os.path.split(fn2[0])
    dict1['filename'] = temp2[1]
    dict1['filepath'] = fn2[0]

  dict1['nFile'] = len(fn2)

  # facets from fn
  #fn3 = fn2[0]
  fn3a = fn.lower()

  if 1:
    pp = '_'
    if fn3a.find('/mnt/')>-1:
      pp = 'staged'

    if fn3a.find('/home/svc/upload')>-1:
      pp = 'uploaded'

    if fn3a.find('http')>-1:
      pp = 'online'
    dict1['source'] = pp

  pp = '_'
  for prov in providers:
    if fn3a.find('cmip5/%s'%prov)>-1:
      pp = providers[prov]

  dict1['provider'] = pp
  
  pp = '_'
  for mod1 in models2:
    if fn3a.find(models2[mod1])>-1:
      pp = mod1
  dict1['model'] = pp

  pp = '_'
  for exp1 in experiments2:
    if fn3a.find(experiments2[exp1])>-1:
      pp = exp1
  dict1['experiment'] = pp

  pp = '_'
  for rr in runs2:
    if fn3a.find(runs2[rr])>-1:
      pp = rr
  dict1['run'] = pp


  try:
    if len(fn2)>1:
      nc = MFDataset(fn2)
      nc1 = Dataset(fn2[0])
      nc2 = Dataset(fn2[-1])

    else:
      if overwrite:
        nc = Dataset(fn2[0], 'r+')
      else:
        nc = Dataset(fn2[0])

  except Exception as e :
    dict1['message'] += "File on server is not found: %s "%(fn)
    dict1['success'] = False

    ok1 = 5
    print(('ok1 = %d'%ok1))
    print(("cannot open file: %s "%(fn2[0])))
    if len(fn2)>1:
      print(("cannot open file: %s "%(fn2[-1])))

    print((traceback.format_exc())) 
    return ok1

  # loop_vars
  varListAll = list(nc.variables.keys())
  varListAll = [str(i) for i in varListAll]
  
  
  # gather global att
  title2 = ''
  try:
    title2 = nc.title
  except:
    pass

  summary2 = ''
  try:
    summary2 += nc.obs_project
  except:
    pass

  try:
    summary2 += nc.source
  except:
    pass

  try:
    summary2 += nc.history
  except:
    pass

  freq2 = ''
  try:
    if nc.frequency == 'mon':
      freq2 += 'monthly'
  except:
    pass

  # find dim
  str1 = ''
  dimList = []
  for var in varListAll:

    # find_units
    units1 = ''
    d1 = nc.variables[var]
    try:
      units1 = d1.units 
    except:
      temp1 = var.find('_bnds')
      if temp1==-1:
        check1 += var + ': need the units attribute.\n'

    # find_longname
    longName = '_'

    try:
      longName = d1.long_name 
    except: pass

    try:
      longName = d1.longname 
    except: pass
      
    # collect_dims

    # to remove u' (unicode thing)
    dim1 = list(d1.dimensions)
    for i in range(len(dim1)):
      dim1[i] = str(dim1[i])

    if var.find('_bnds')==-1:
      str1 += '%s: %s\n'%(var, str(dim1))
      dimList += list(dim1)

    varDict[var] = {'dim':  dim1, 
                    'units': units1,
                    'longName': longName,
                   }

  str1 += '\nDimension Variables\n'
  dimList = list(set(dimList))

  # only if the dim is a variable itself
  dimList2 = []
  for d in dimList:
    if d in varListAll:
      dimList2.append(d)
  dimList = dimList2
  dimList0 = dimList

  if vb==1: print('dimList0')
  if vb==1: print(dimList0)

  dimList = []

  # collect_vars, only they are not dim var

  dimList0a = [i.lower() for i in dimList0]

  varList = []
  varListLong = []
  for k in varListAll:
    k1 = k.lower()
    if k not in dimList0:
      if not k1.endswith('_bnds') \
          and not k1.endswith('err') \
          and not k1.endswith('nobs') \
          and not k1.endswith('stddev') \
          and k1 not in (
            'month', 
            'year',
            'height',
            'plev',
            'not_used',
            'model_lat',
            'model_lon'): 
        varList.append(k)
        varListLong.append(varDict[k]['longName'])

  
  if vb==1: print('varList:')
  if vb==1: print(varList)

  # from the varList, 
  # collect_the_real dim
  dimList = []
  for var in varList:
    d1 = nc.variables[var]
    dim1 = list(d1.dimensions)
    for i in range(len(dim1)):
      dim1[i] = str(dim1[i])

    if vb==1: print('dim1')
    if vb==1: print(dim1)
      
    str1 += '%s: %s\n'%(var, str(dim1))
    dimList += list(dim1)

  # this is the list of dims of the real vars
  dimList = list(set(dimList))

  if vb==1: print('dimList:')
  if vb==1: print(dimList)

  # check_dimList
  for dimVar in dimList:
    dimWhat = ''
    dimAsI = 0 

    try: 
      d2 = nc.variables[dimVar]

      if len(fn2)>1:
        d2a1 = nc1.variables[dimVar]
        d2a2 = nc2.variables[dimVar]

    except:
      dimAsI = 1 
      hasUnits = 0
      ok1 = 1
      print(('this dim is not a var: %s'%dimVar))
      print((traceback.format_exc())) 

    # test if 2d dim
    if not dimAsI:
      # check_var_dim
      for var1 in varList:
        for dimV in varDict[var1]['dim']:
          if dimV in varListAll:
            shape0 =  nc.variables[dimV].shape 
            if len(shape0)>1:
              ok1 = 11
              return ok1

      try:
        units1 = str(d2.units)
        if len(fn2)>1:
          #xxxx should not do this. should do the dim of the real var.
          units1a1 = str(d2a1.units)
          units1a2 = str(d2a2.units)

        hasUnits = 1
        print(('units1: '), end=' ')  
        print(units1)

      except:
        hasUnits = 0
        ok1 = 2
        print(('this var has no units: %s'%dimVar))
        print((traceback.format_exc())) 
        return ok1
        #if overwrite==0 and allowOverwrite==1:
        #  return checkNc_w(nc, fn, dict9)

    # if_hasUnits
    if hasUnits:
      goodUnits = 1
      try:
        cfUnits = cf1.Units(units1)
      except:
        print((traceback.format_exc())) 
        goodUnits = 0

      # month since, and 0000 are ok with 360_day
      if not goodUnits:
        goodUnits = 1
        try:
          cfUnits = cf1.Units(units1, calendar='360_day')
        except:
          print((traceback.format_exc())) 
          goodUnits = 0

      if 0:
        if not goodUnits:
          goodUnits = 1
          try:
            cfUnits = cf1.Units(units1, calendar='365_day')
          except:
            print((traceback.format_exc())) 
            goodUnits = 0

      if not goodUnits:
        ok1 = 3
        print('ok1=3')
        print(('units not recgnized: %s'%units1))
        print((traceback.format_exc())) 
        goodUnits = 0
        return ok1

      if goodUnits:
        if vb==1: print('cfUnits:')
        if vb==1: print(cfUnits)
   
        if cfUnits.islongitude:
          dimWhat = 'lon'
        elif cfUnits.islatitude:
          dimWhat = 'lat'
        elif cfUnits.isreftime:
          dimWhat = 'time'
        elif cfUnits.ispressure or units1=='hPa':
          dimWhat = 'z'

    #if hasUnits:
      # check_time_limits
      if dimWhat=='time':

        if len(fn2)>1:
          units9 = units1a1
        else:
          units9 = units1

        if vb==1: print('units9')
        if vb==1: print(units9)
        date1 = cmac.num2date(netCDF4,d2[0], units9)
        date2 = cmac.num2date(netCDF4,d2[-1], units9)
 
        if vb==1: print(date1)
        if vb==1: print(date2)

        if (date1 is None) or (date2 is None):
          ok1 = 11      
          return ok1

        time1 = date1.timetuple()
        time2 = date2.timetuple()

        a1 = '%04d%02d%02d %02d:%02d:%02d'%(time1[0], time1[1], time1[2], time1[3], time1[4], time1[5])

        a2 = '%04d%02d%02d %02d:%02d:%02d'%(time2[0], time2[1], time2[2], time2[3], time2[4], time2[5])

        a1 = a1[:8]
        a2 = a2[:8]
        a3 = '1'

      else:  # not time
        try:
          d2a = d2[:]
          a1 = ('%.2f'%d2a.min()).rstrip('0').rstrip('.')
          a2 = ('%.2f'%d2a.max()).rstrip('0').rstrip('.')     
          try:
            a3 = ('%.2f'%(d2a[1]-d2a[0])).rstrip('0').rstrip('.')
          except: a3 = '0'
        except:
          a1 = '0'
          a2 = '0'
          a3 = '0'

        try:
          if dimWhat=='z':
            a3 = ''
            for aa in d2a: 
                a3 += ('%.2f'%aa).rstrip('0').rstrip('.')+','
            a3 = a3[:-1]
        except: a3 = '0'

      str1 += '%s: %s to %s (%s)\n'%(dimVar, a1, a2, units1)
      varDict[dimVar]['min'] = a1
      varDict[dimVar]['max'] = a2
      varDict[dimVar]['res'] = a3
      varDict[dimVar]['units'] = units1
      varDict[dimVar]['what'] = dimWhat

      # end
    #if hasUnits:
  if ok1 > 0:
    return ok1

  # construct_dim2
  if 1:
    for var1 in varList:
    #for var1 in varDict.keys():

      dim2 = []
      for i in varDict[var1]['dim']:
        try:
          dim2.append( varDict[i]['what'] )
        except:
          dim2.append( 'unknown' )
      varDict[var1]['dim2'] = dim2

  # place the significant var to front
  if 1:
    import numpy as np
    def varDL(e):
      dim2z = varDict[e]['dim2']
      return len(dim2z)
      
    order1 = [varDL(i) for i in varList]
    order1Ind = np.argsort(order1)[::-1]
    varList = [varList[i] for i in order1Ind]
    varListLong = [varListLong[i] for i in order1Ind]

    print("varList:")
    print(varList)
    print(varListLong)

  if 0:  # cannot sort varListLong
    def varDL(e):
      dim2z = varDict[e]['dim2']
      return len(dim2z)
      
    varList.sort(reverse=True, key=varDL)
    varListLong.sort(reverse=True, key=varDL)
    print("varList:")
    print(varList)
       
  # construct_global_dim2
  dim22 = []
  for d in dimList:
    try:
      dim22.append( varDict[d]['what'] ) 
    except:
      dim22.append( 'unknown' )
  

  nc.close()
  check1 += '\nThe netCDF file has %d variables:\n%s'%(len(varList), str1) 

  dict1['varDict'] = varDict 
  dict1['varList'] = varList
  dict1['varListLong'] = varListLong
  dict1['dimList'] = dimList 
  dict1['dim2'] = dim22 
  dict1['check'] = check1
  dict1['warning'] = warning
  dict1['title'] = title2
  dict1['summary'] = summary2
  dict1['frequency'] = freq2
  dict1['ok'] = 0

  return ok1



