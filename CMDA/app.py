#== todo___
#== 2to3___
#== import___
#== import_for_services__
#== timeStr___
#== setting_CMU
#== crossdomain___
#==def_assignUrl
#== def_serviceFunc__
#== correlationMap__
#== universalPlotting3b__   for universalPlotting
#== universalPlotting6b__   
#== universalPlotting6c__   
#== cmda1__   
#== static_html

'''
export FLASK_APP=app.py
flask run

'''

#== todo___
'''
- pytz

'''
#== 2to3___
'''
- basestring -> str
- urllib2.request -> urllib.request.Request
- urllib2.urlopen -> urllib.request.urlopen
- urllib2.HTTPError -> urllib.error.HTTPError
- import urllib -> import urllib.parse, urllib.error, urllib.request



'''
#== import___
from flask import Flask

app = Flask(__name__)

import os, hashlib, shutil
from datetime import datetime, timedelta
import hashlib 
#import urllib2
import urllib.request as urllib2
#import httplib
import http.client as httplib

import time, json

from flask import jsonify, request, url_for, make_response
from flask import render_template
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename

#== import_for_services__
from svc.src.universalPlotting3 import call_universalPlotting3
from svc.src.universalPlotting6b import call_universalPlotting6b
from svc.src.universalPlotting import call_universalPlotting  # only this one is used
#from svc.src.py import download_file_from_url
#from svc.src.py import checkNc
#from svc.src.py import checkNc2


#== timeStr___
#count0 = 0
with open('count','w') as f:
    f.write('%d'%0)

from datetime import datetime
#from pytz import timezone
def timeStr():
  #usPac = timezone('US/Pacific')
  #time1 = datetime.now(usPac)
  time1 = datetime.now()
  return time1.strftime('%Y-%m-%d %H:%M:%S')

#== setting_CMU
CMU_PROVENANCE_URL = 'http://hawking.sv.cmu.edu:9075/serviceExecutionLog/addServiceExecutionLog' 
CMU_PROVENANCE_URL_2 = 'http://hawking.sv.cmu.edu:9038/serviceExecutionLog/addServiceExecutionLog'  
#CMU_PROVENANCE_URL_3 = 'https://hawking.sv.cmu.edu:9016/opennex/serviceExecutionLog/addAPIExecutionLog'  
CMU_PROVENANCE_URL_3 = 'https://opennex.org/serviceExecutionLog/addAPIExecutionLog'
 
### VIRTUAL_EINSTEIN_URL = 'http://ec2-54-183-194-175.us-west-1.compute.amazonaws.com:9034/serviceExecutionLog/addServiceExecutionLog'
### Why do we need virtual einstein?
### VIRTUAL_EINSTEIN_URL = 'http://ec2-54-183-11-107.us-west-1.compute.amazonaws.com:9034/serviceExecutionLog/addServiceExecutionLog'

HEADERS = {'Content-Type': 'application/json'}
#USE_CMU = True
#USE_CMU_3 = True
#USE_CMU_3 = True
USE_CMU_3 = False
USE_CMU = False

IPDict = { 
              "54.183.194.175": 26,

              }

#== crossdomain___
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    #def decorator(f):
    #    def wrapped_function(*args, **kwargs):
    #        if automatic_options and request.method == 'OPTIONS':
    #            resp = current_app.make_default_options_response()
    #        else:
    #            resp = make_response(f(*args, **kwargs))
    #        if not attach_to_all and request.method != 'OPTIONS':
    #            return resp

    #        h = resp.headers

    #        h['Access-Control-Allow-Origin'] = origin
    #        h['Access-Control-Allow-Methods'] = get_methods()
    #        h['Access-Control-Max-Age'] = str(max_age)
    #        if headers is not None:
    #            h['Access-Control-Allow-Headers'] = headers
    #        return resp

    #    f.provide_automatic_options = False
    #    return update_wrapper(wrapped_function, f)
    #return decorator

#==def_assignUrl
def assignUrl(service1, tag, imgFileName, dataFileName):
      hostname1 = "api.jpl-cmda.org"
      backend_url = 'https://' + hostname1 + '/svc/' + service1
      print(('backend_url: ', backend_url))
      plotUrl = 'https://' + hostname1 + '/static/' + service1 + '/' + tag + '/' + imgFileName
      print(('plotUrl: ', plotUrl))
      dataUrl = 'https://' + hostname1 + '/static/' + service1 + '/' + tag + '/' + dataFileName
      print(('dataUrl: ', dataUrl))
      failedImgUrl = 'https://' + hostname1 + '/static/plottingFailed.png'
      print(('failedImgUrl: ', failedImgUrl))

      return backend_url, plotUrl, dataUrl, failedImgUrl

#def get_host_port(cfg_file):
#    myvars = {}
#    myfile =  open(cfg_file)
#    for line in myfile:
#        name, var = line.partition("=")[::2]
#        name = name.strip()
#        var = var.strip('\n').strip()
#        if name is not '' and var is not '':
#            myvars[name] = var
#
#    return myvars["HOSTNAME"], myvars["PORT"]
#
##== def_get_host_port2(cfg_file):
#def get_host_port2(cfg_file):
#  hostname0, port = get_host_port(cfg_file)
#  if hostname0 == 'EC2':
#    try:
#      req = urllib.request.Request('http://169.254.169.254/latest/meta-data/public-ipv4')
#      response = urllib.request.urlopen(req)
## ://ec2-13-56-67-192.us-west-1.compute.amazonaws.com
#      temp1 = response.read().split('.')
#      temp2 = '-'.join(temp1)
#      hostname = 'ec2-%s.us-west-1.compute.amazonaws.com'%temp2
#    except Exception as e:   
#      print(('e: ', e))
#
#  else: 
#    hostname = hostname0
#
#  return hostname, port

def url_is_alive(url):
  request = urllib.request.Request(url)
  print(request)
  request.get_method = lambda: 'HEAD'
  print((request.get_method))

  try:
    print((urllib.request.urlopen(request)))
    return True
  except urllib.error.HTTPError:
    return False
  except urllib.error.URLError:
    return False


def exists(site, path):
  conn = httplib.HTTPConnection(site)
  conn.request('HEAD', path)
  response = conn.getresponse()
  conn.close()
  return response.status == 200


#== def_convertPres
def convertPres(var1, pres1):
  if int(pres1) == -999999 :
    return str(pres1)
  if var1=='ot' or var1=='os':
    fac = 10000
  else:
    fac = 100
  return str(int(pres1)*fac)

#== def_serviceFunc__
# This is for opennex api
# used by:
#   universalPlotting3b
#   universalPlotting6b

def serviceFunc(service):
    #global count0
    with open('count','r') as f:
        count0 = int(f.read())

    count0 += 1
    print(timeStr())
    print('###################zzzz count=%d #############################xxxx'%count0)

    with open('count','w') as f:
        f.write('%d'%count0)

    print(('running %s'%service))
    executionStartTime = int(time.time())
    # status and message
    success = True
    message = "ok"
    plotUrl = ''
    dataUrl = ''

    json2 = {}
    keys = list(request.args.keys())
    for k in keys:
      json2[k] = request.args.get(k, '')

    try:
      userId = int(json2['userId'])
    except:
      userId = 0

    try:
      serviceId = int(json2['serviceId'])
    except:
      serviceId = 34

    frontend_url = 'not_passed'
    try:
      frontend_url = json2['fromPage']
    except:
      pass

    try:
      purpose = json2['purpose']
    except:
      purpose = ''

    # get where the input file and output file are
    #current_dir = os.getcwd()
    #current_dir = '/home/btang/projects/CMDA0'
    current_dir = '/home/ubuntu/CMDA0'
    print('current_dir: ', current_dir, flush=True)
    if 1:
    #try:
      seed_str = str(time.time())
      tag = hashlib.md5(seed_str.encode('utf-8')).hexdigest()
      #tag = 'aazz'
      output_dir = current_dir + '/svc/static/%s/'%service + tag
      print(('output_dir: ', output_dir))
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      json2['outDir'] = output_dir

      import pickle
      pFile = '%s/p.pickle'%output_dir
      fid = open(pFile,'wb')
      pickle.dump(json2, fid)
      fid.close()

      # chdir to where the app is
      os.chdir(current_dir+'/svc/src/%s'%service)
      # instantiate the app. class
      c1 = call_universalPlotting.call_universalPlotting(pFile)
      # call the app. function (0 means the image created is scatter plot)
      ### (message, imgFileName) = c1.displayScatterPlot2V(0)
      (message, imgFileName, dataFileName) = c1.display()
      #message = message.decode()
      #imgFileName = imgFileName.decode()
      #dataFileName = dataFileName.decode()

      # chdir back
      os.chdir(current_dir)

      print('qqqq', message)
      failedCheck = 0    
      if message.find('failedCheck')>-1:
        failedCheck = 1    

      #ind1 = message.find('No Data')
      #if ind1>0:
      #  message1 = message[ind1:(ind1+200)]
      #  message1a = message1.split('\n')
      #  print((message1a[0]))
      #  print((message1a[1]))
     
      #hostname, port = get_host_port2("host.cfg")
      #hostname, port = '127.0.0.1', '5000'
      #hostname, port = 'EC2', '8080'
      #hostname, port = '54.193.239.191', '8080'
      #hostname, port = '54.193.239.191', '8080'
      hostname, port = 'jpl-cmda.org', ''
      if hostname == 'EC2':
        try:
          req = urllib.request.Request('http://169.254.169.254/latest/meta-data/public-ipv4')
          response = urllib.request.urlopen(req)
          hostname = response.read()
        except Exception as e:
          print(('e: ', e))

      print(('userId: ', userId))
      print(('hostname: ', hostname))
      print(('port: ', port))

      #purpose = request.args.get('purpose')#"Test .\'\"\\purpose"

      
      httpStr = 'https'
      #httpStr = 'http'
      if port:
        portSep = ':'
      else:
        portSep = ''

      #backend_url = '%s://'%httpStr + hostname + ':' + port + '/svc/%s'%service
      #print(('backend_url: ', backend_url))
      print(('imgFileName: ', imgFileName))
      #plotUrl = 'http://' + hostname + ':' + port + '/static/%s/'%service + tag + '/' + imgFileName
      if imgFileName:
        plotUrl = '%s://'%httpStr + hostname + portSep + port + '/static/%s/'%service + tag + '/' + imgFileName
      else:
        plotUrl = ''

      print(('plotUrl: ', plotUrl))
      #dataUrl = 'http://' + hostname + ':' + port + '/static/%s/'%service + tag + '/' + dataFileName
      if dataFileName:
        dataUrl = '%s://'%httpStr + hostname + portSep + port + '/static/%s/'%service + tag + '/' + dataFileName
      else:
        dataUrl = ''
      print(('dataUrl: ', dataUrl))

      failedImgUrl = '%s://'%httpStr + hostname + portSep + port + '/static/plottingFailed.png'
      #print 'failedImgUrl: ', failedImgUrl

      #if imgFileName is '' or not os.path.exists(output_dir+'/'+imgFileName):
      #  print(('****** Error: %s not exist' % imgFileName))
      #  plotUrl = failedImgUrl

      #if dataFileName is '' or not os.path.exists(output_dir+'/'+dataFileName):
      #  print(('****** Error: %s not exist' % dataFileName))
      #  dataUrl = failedImgUrl

      #print(('message: ', message))

      #if failedCheck or (len(message) == 0) or (message.find('No Data') >= 0):
      if failedCheck:
        success = False
        plotUrl = ''
        dataUrl = ''

    executionEndTime = int(time.time())

    print(type(success))
    print(type(message))
    print(type(plotUrl))
    print(type(dataUrl))

    try:
        success = success.decode('UTF-8') 
    except:
        pass

    try:
        message = message.decode('UTF-8') 
    except:
        pass

    try:
        plotUrl = plotUrl.decode('UTF-8') 
    except:
        pass

    try:
        dataUrl = dataUrl.decode('UTF-8') 
    except:
        pass

    #import json
    #return json.dumps({

    print('======================== end_Route =============================',flush=True)

    return jsonify({
        'success': success,
        'message': message,
        #'message': 'Jos is done. No further message.',
        'url': plotUrl,
        'dataUrl': dataUrl
    })

#== correlationMap__
@app.route('/svc/correlationMap', methods=["GET"])
def correlationMap():
    return serviceFunc('correlationMap')

#== universalPlotting3b__
@app.route('/svc/universalPlotting3b', methods=["GET"])
def displayUniversalPlotting3b():
    return serviceFunc('universalPlotting3')

#== universalPlotting6b__   
@app.route('/svc/universalPlotting6b', methods=["GET"])
#@crossdomain(origin='*')
def displayUniversalPlotting6b():
    return serviceFunc('universalPlotting6b')

#== universalPlotting6c__   
@app.route('/svc/universalPlotting6c', methods=["GET"])
#@crossdomain(origin='*')
def displayUniversalPlotting6c():
    return serviceFunc('universalPlotting6c')


#== cmda1__   
@app.route('/svc/cmda1', methods=["GET"])
#@crossdomain(origin='*')
def displayCmda1():
    return serviceFunc('cmda1')

#== static_html
from flask import send_from_directory
#htmlDir = '/home/svc/new_github/CMDA/JPL_CMDA/frontend/public/html/'
#htmlDir = '/home/btang/projects/CMDA0/html/'
htmlDir = '/home/ubuntu/CMDA0/html'
#staticDir = '/home/ubuntu/CMDA0/svc/static/universalPlotting6b/aazz'
staticDir = '/home/ubuntu/CMDA0/svc/static'

@app.route('/assets/html/<path:fileName>')
def serveStaticFile(fileName):
    return send_from_directory(htmlDir, fileName)

#@app.route('/<path:fileName>')
#def serveResult(fileName):
#    print(staticDir)
#    print(fileName,flush=True)
#    return send_from_directory(staticDir, fileName)

# just for debugging:
@app.route('/static/universalPlotting6b/aazz/<path:fileName>')
def serveResult2(fileName):
    print(staticDir)
    print(fileName,flush=True)
    return send_from_directory(staticDir, fileName)

# for serving resulting plot and data file
@app.route('/static/<path1>/<path2>/<fileName>')
def serveResult(path1,path2,fileName):
    #print(staticDir)
    #print(path1)
    #print(path2)
    #print(fileName,flush=True)
    return send_from_directory(staticDir+'/'+path1+'/'+path2, fileName)

@app.route('/<path:fileName>')
def serveStaticFile2(fileName):
    return send_from_directory(htmlDir, fileName)

@app.route('/services')
def serveStaticFile3():
    fileName = 'cmda_services.html'
    return send_from_directory(htmlDir, fileName)

@app.route('/')
def serveStaticFile4():
    fileName = 'CMDA_intro.html'
    return send_from_directory(htmlDir, fileName)

# for test
@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

#===

'''
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
#
#@app.route("/index")
#def index():
#    return "<p>In index page zz</p>"
'''
