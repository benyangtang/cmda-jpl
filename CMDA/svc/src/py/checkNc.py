# import__
# def_checkNc(fn, dict1):
  # loop_vars
    # find_units
    # find_longname
    # collect_dims
  # loop_dim_vars
    # if_hasUnits
      # replace_ref_time_of 0000
    # dim_range
  # collect_vars
  # construct_dim2

# import__
from netCDF4 import Dataset
import netCDF4 
import os
import cf_units as cf
import cfunits as cf1
import copy

def checkNc_w(nc, fn, dict1):
  print('in checkNc_w')
  nc.close()
  # call checkNc(overwrite=1)
  checkNc(fn, dict1, overwrite=1)
  return None

# def_checkNc(fn, dict1):
def checkNc(fn, dict1, overwrite=0, allowShift=1):

  dict9 = copy.deepcopy(dict1)

  varList = []
  varDict = {}
  check1 = ''
  warning = ''

  temp1 = os.path.split(fn)
  dict1['filename'] = temp1[1]

  print("in checkNc: ", fn)
  try:
    if overwrite:
      nc = Dataset(fn, 'r+')
    else:
      nc = Dataset(fn)

  except Exception as e :
    dict1['message'] += "File on server is not found: %s \n\n%s"%(fn, repr(e))
    dict1['success'] = False
    return None

  # loop_vars
  varListAll = list(nc.variables.keys())
  
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
    print('here 1')
    longName = var
    try:
      longName = d1.lone_name 
    except: pass
    try:
      longName = d1.lonename 
    except: pass
    try:
      longName = d1.name 
    except: pass
      
    # collect_dims
    print('here 2')
    # to remove u' (unicode thing)
    dim1 = list(d1.dimensions)
    for i in range(len(dim1)):
      dim1[i] = str(dim1[i])
    dim1 = tuple(dim1)
 
    if var.find('_bnds')==-1:
      str1 += '%s: %s\n'%(var, str(dim1))
      dimList += list(dim1)

    varDict[var] = {'dim':  dim1, 
                    'units': units1,
                    'longName': longName,
                   }

  # loop_dim_vars
  print('here 3')
  str1 += '\nDimension Variables\n'
  dimList = list(set(dimList))
  dimDict = {}
  for dimVar in dimList:
    print('here 4a')
    dimWhat = ''
    d2 = nc.variables[dimVar]
    try:
      units1 = d2.units
      hasUnits = 1
    except:
      hasUnits = 0
      if overwrite==0:
        return checkNc_w(nc, fn, dict9)
      
    # if_hasUnits
    if hasUnits:
      cfUnits = cf1.Units(units1)
      if cfUnits.islongitude:
        dimWhat = 'lon'
      elif cfUnits.islatitude:
        dimWhat = 'lat'
      elif cfUnits.isreftime:
        dimWhat = 'time'
      elif cfUnits.ispressure:
        dimWhat = 'z'
      else:
        dimWhat = 'z'

      # replace_ref_time_of 0000
      print('here 4b')
      if dimWhat=='time':
        print('here 4ba')
        if str(cfUnits.reftime)[:4]=='0000':
          if overwrite==0:
            return checkNc_w(nc, fn, dict9)
          
          units2 = units1.replace( '0000', '1800' ) 
          cfUnits1 = Units( units1 )
          cfUnits2 = Units( units2 )
          d2[:] = cf1.conform( d2[:], cfUnits1, cfUnits2 )
          units1 = units2
          d2.units = units1

    else:  # no units
      print('here 4c')
      if dimVar.lower().find('lon')>-1: 
        dimWhat = 'lon'
        units1 = 'degrees_east'

      elif dimVar.lower().find('lat')>-1: 
        dimWhat = 'lat'
        units1 = 'degrees_north'

      elif dimVar.lower().find('time')>-1: 
        dimWhat = 'time'
        units1 = 'days since 1800-01-01'
        warning += '!!! made up time units: %s !!! \n'%(units1)
        check1 += '!!! made up time units: %s !!! \n'%(units1)

      elif (dimVar.lower().find('z')>-1) \
         or (dimVar.lower().find('plev')>-1)  \
         or (dimVar.lower().find('depth')>-1)  \
         or (dimVar.lower().find('height')>-1)  \
         or (dimVar.lower().find('vert')>-1) :
        print('here 4d')
        dimWhat = 'z'
        units1 = 'm'
        warning += '!!! made up vertical units: %s !!! \n'%(units1)
        check1 += '!!! made up vertical units: %s !!! \n'%(units1)

      else:
        print('here 4e')
        dimWhat = 'z'
        units1 = 'i'
        warning += '!!! made up i units: %s !!! \n'%(units1)
        check1 += '!!! made up i units: %s !!! \n'%(units1)

      d2.units = units1

    # dim_range
    print('d2: ', d2)
    print('here 5')
    #   a1 = '00000101'
    #   a2 = '29991231'

    
    if dimWhat=='time':
      print('here 3aa')
      time1 = netCDF4.num2date(d2[0], d2.units).timetuple()
      print('time1: ', time1)
      a1 = '%04d%02d%02d %02d:%02d:%02d'%(time1[0], time1[1], time1[2], time1[3], time1[4], time1[5])
      time2 = netCDF4.num2date(d2[-1], d2.units).timetuple()
      a2 = '%04d%02d%02d %02d:%02d:%02d'%(time2[0], time2[1], time2[2], time2[3], time2[4], time2[5])
      a1 = a1[:8]
      a2 = a2[:8]

    else:  # not time
      try:
        d2a = d2[:]
        a1 = str(d2a.min())
        a2 = str(d2a.max())      
        print('here 3ab')
      except:
        a1 = '0'
        a2 = '0'
        print('here 3ac')
    print('here 3ad')
    str1 += '%s: %s to %s (%s)\n'%(dimVar, a1, a2, units1)
    varDict[dimVar]['min'] = a1
    varDict[dimVar]['max'] = a2
    varDict[dimVar]['units'] = units1
    varDict[dimVar]['what'] = dimWhat
    print(varDict[dimVar])
    print('here 3b')

  # collect_vars
  print('here 4')
  varList = []
  for k in varListAll:
    if k not in dimList and k.find('_bnds')==-1: 
      varList.append(k)

  # construct_dim2
  print('calc dim2')
  print(' varDict.keys(): ', end=' ')
  print(list(varDict.keys()))
  for var1 in list(varDict.keys()):
    print('var1: ', var1)
    dim2 = []
    print("varDict[var1]['dim']: ", end=' ')
    print(varDict[var1]['dim'])
    for i in varDict[var1]['dim']:
      dim2.append( varDict[i]['what'] )
    print('dim2: ', dim2)
    varDict[var1]['dim2'] = dim2

  print('here 7')
  nc.close()
  print('here 7a')
  check1 += '\nThe netCDF file has %d variables:\n%s'%(len(varList), str1) 

  dict1['varDict'] = varDict 
  dict1['varList'] = varList
  dict1['dimList'] = dimList 
  dict1['check'] = check1
  dict1['warning'] = warning

  return None


