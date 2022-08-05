// The following is for the code navigation purpose.
//
// disableButton__(id1)
// parse_pres__
// get_querystring__

//function_getQs(queries, k) {

// processQS5__
// makeQueryStr__
// makeBrowserUrl__
// copyBrowserUrl__
// function_setTimeFullRange__() {
// addDataList_(ID) {
// ajaxCall__
// combineList__

// ==url_classes
//

// ==url_classes
// urlDirect_() {
// urlYearMonthDay_() {
// urlYearMonth_() {
// urlEscape_() {
// url2escape_() {
// urlModel__() {              not used 
// urlMultiModel__() {         not used
// urlPres_() {
// urlSubs__
// cumSubs__
// forMethod3__
// subs2Url__
// urlPlotP__
// urlTimeMean___
// urlAxisMethod__() {
// urlDatasets__() {
// urlVars__() {
// urlList__() {

//==  not ready yet
// urlCheckbox_() {
// urlTime_() {
// urlRadioTwo_() {
// urlDataUrl_() {
// urlMonths_() {
// urlScale1_() {
// urlScale1a_() {
// urlScale2_() {
// urlScale3_() {
// urlNumber_() {
// urlNumberCheck_() {

console.log("reload common.js");
var naValue = "-999999";
// test3__
function test3a() {
  vueApp.var1 = 'lai';
}

// disableButton__(id1)
function disableButton(id1)
{
  var x=document.getElementById(id1);
  x.disabled=true;
  x.style.background="#999999";
}

function enableButton(id1)
{
  var x=document.getElementById(id1);
  x.disabled=false;
  x.style.background="#4dffa6";
  //x.style.background="#ccff99";
}


// parse_pres__
function parse_pres(pres10) {
  var pres1 = "";

  if (pres10=="") {pres1 = naValue; }
  else {
    //if (!(isNaN(Number(pres10)))) { 
    //  pres1 = pres10; 
    //} else {
      var checkNan = 0;
      var pres2 = [];
      var temp1=pres10.split(",");
      //for (var i in temp1) {
      for (var i=0; i<temp1.length; i++) {
        if (isNaN(Number(temp1[i]))) {
          checkNan = 1; 
        } else {
          pres2.push(Number(temp1[i]));
        }
      }
      if (pres2.length>0) { pres1 = pres2.join(); }
      else { pres1 = naValue; }
    //}
  }
  return pres1;
}

// get_querystring__
function get_querystring() {
  var queries = {};
  $.each(document.location.search.substr(1).split('&'),function(c,q){
    var i = q.split('=');
    try { 
      queries[i[0].toString()] = i[1].toString();
    } catch(err) {}
  });
  return queries;
}

function fetchQValue(queries, key0) {
  var vq;
  if (!queries.hasOwnProperty(key0)) { 
    return false; 

  } else {
    return queries[key0];
  }
}

//function_getQs(queries, k) {
function getQs(queries, k, default1) {
  var default2 = typeof default1 !== 'undefined' ? default1:false;
  if (queries.hasOwnProperty(k)) {
    return queries[k];
  } else {
    return default2;
  }
}

// processQS5__
function processQS5() {
  var queries = get_querystring();
  if (queries.length<1) {return;}

  var service0 = fetchQValue(queries,'service');
  if (service0 !== false) {
    //vueApp.service0 = service0;  // only if want to make individual service
    vueApp.service = service0;
    vueApp.changeService();
    vueApp.title = vueApp.service9.title;
    vueApp.description = vueApp.service9.description;
    document.title = vueApp.title;
  }

  vueApp.checkApi();
  var key0, key1, vq, nVar;

  var mapping = $.extend(mappingAll['base'], 
       mappingAll[vueApp.service] );

  //console.log(mapping);

  var paras = [];
  for (key0 in mapping) {
    //console.log(key0);

    if (key0 == 'subs') {
      // datasets and vars in queries?
			var dim2a, subs2a;
      var datasets = fetchQValue(queries,'datasets');
      var vars = fetchQValue(queries,'vars');
      if (datasets !== false && vars !==false) {
        var datasets9 = datasets.split(','); 
        var vars9 = vars.split(','); 

        vueApp.aaa1 = datasets9;
        vueApp.aaa2 = vars9;

        var dataset9, var9;
				var dim2, subs2, a1, k1, v1;

        // loop over datasets
        for (var i=0; i<datasets9.length; i++){ 
					// get var9, var9.subs2
					dataset9 = vueApp.fileDict[datasets9[i]];
					var9 = dataset9.varDict[vars9[i]];
					dim2 = var9.dim2;
          
				  if (var9.hasOwnProperty(subs2)) {	
            subs2 = var9.subs2;
          } else {
						var9.subs2 = jQuery.extend(true, {}, subsDef);
            subs2 = var9.subs2;
          } 

					vueApp.aaa3 = dataset9;
					vueApp.aaa4 = var9;
					vueApp.aaa5 = subs2;

					// assign subs2
          var axes = [
            'lon',
            'lat',
            'press',
            'time',
          ]

					for (var ii=0; ii<4; ii++) {
            a1 = axes[ii];
            k1 = a1 + 'Method';
            v1 = fetchQValue(queries, k1);
            if (v1 !== false){
							subs2[k1] = v1.split(',')[i];
            } else {
              continue;
            }

            k1 = a1 + 'S';
            v1 = fetchQValue(queries, k1);
            if (v1 !== false){
              if (subs2[a1+'Method']=='1') {
								subs2[k1+'1'] = v1.split(',')[i];
              } else {
								subs2[k1+'23'] = v1.split(',')[i];
              }
            }

            k1 = a1 + 'E';
            v1 = fetchQValue(queries, k1);
            if (v1 !== false){
							subs2[k1] = v1.split(',')[i];
            }

					}
        }
      }
    }

    if (key0 == 'plotP') {
      var colorMap = fetchQValue(queries,'colorMap');
      var ferretLevel = fetchQValue(queries,'ferretLevel');
      var plotTitle = fetchQValue(queries,'plotTitle');
      if (colorMap !== false && ferretLevel !==false) {
        colorMap = colorMap.split(',');
        ferretLevel = ferretLevel.split(',');
        plotTitle = plotTitle.split(',');

        for (var i=0; i<colorMap.length; i++){ 
          vueApp.plotP9[i].colorMap = colorMap[i];
          vueApp.plotP9[i].ferretLevel = ferretLevel[i].replace(/_C_/g, ','); 
          vueApp.plotP9[i].plotTitle = unescape(unescape(plotTitle[i]));
        }
      }
    }

    vq = fetchQValue(queries, key0);
    if (vq ===false) { continue; }
    paras.push(key0);
    vq = vq.trim();
    mapping[key0].toHtml(vq);
  }
  // key0 will not necessarily represent a parameter; can be a method for a group of para.
  //for (key0 in queries) {
  //  if (key0 == 'userid') continue;
  //  vq = fetchQValue(queries, key0);
  //  if (vq ===false) { continue; }

  //  vq = vq.trim();
  //  mapping[key0].toHtml(vq);
  //}

  if (paras.includes('datasets') && paras.includes('vars')) {
		vueApp.changedDatasetSelected();
		vueApp.changedBeingSubsetted();
		vueApp.timeMethodChange();
  }
}

// makeQueryStr__
function makeQueryStr(toServer) {
  toServer = typeof toServer !== 'undefined' ? toServer:false;

  var mapping = jQuery.extend(mappingAll['base'], 
       mappingAll[vueApp.service] );

  var temp1 = "";
  var temp3 = "";
  var key0, key1;
  for (var key0 in mapping) {
    if (!mapping.hasOwnProperty(key0)) { continue; }

		if (toServer) { 
			if (key0 == 'plotUrl') continue;
			if (key0 == 'dataUrl') continue;
		}

    key1 = mapping[key0].key1;
    //temp3 += app[key1]; 
    temp3 = mapping[key0].fromHtml();
    temp1 += temp3 + "&";
  }
  temp1 = temp1.slice(0,-1);

  if (toServer) { 
    temp1 += "&fromPage=" + document.location.href.split('?')[0] ;
	}

  return temp1;
}

// makeServiceUrl__
function makeServiceUrl(backEngin) {
  //var service1 = "universalPlotting6b";
  //vueApp.browserUrl = "https://jpl-cmda.org/svc/" + service1 + "?" + makeQueryStr(true);
  vueApp.browserUrl = document.location.href.split('org')[0] + "org/svc/" + backEngin + "?" + makeQueryStr();
}

// makeBrowserUrl__
function makeBrowserUrl() {
  vueApp.browserUrl = document.location.href.split('?')[0] + "?" + makeQueryStr();
}

// copyBrowserUrl__
function copyBrowserUrl() {
  vueApp.browserUrl = document.location.href.split('?')[0] + "?" + makeQueryStr();
  try {
    $("#browserUrl").select();
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    //console.log('Copying text command was ' + msg);
  } catch (err) {
    console.log('Oops, unable to copy');
  }
}

// function_setTimeFullRange__() {
function setTimeFullRange() {
  if (vueApp.timeELim>= vueApp.timeSLim) {
    if (vueApp.yN<0) {
      vueApp.subs2.timeS23 = timeDash(vueApp.timeSLim);
      vueApp.subs2.timeE = timeDash(vueApp.timeELim);
      vueApp.yN = Math.round((vueApp.timeELim - vueApp.timeSLim)/10000);
      console.log('yN in fun: ' + vueApp.yN);
      
    } else {
      if (vueApp.yNFix==0) {
        var time9 = vueApp.timeELim;
        vueApp.subs2.timeE = timeDash(time9);
      } else {
        var time9 = Number(vueApp.subs2.timeE.replaceAll("-",""));
      }
      var time1 = time9 - vueApp.yN * 10000;
      console.log(vueApp.timeSLim);
      console.log('time1: ' +  time1);
      time1 = Math.max( time1, vueApp.timeSLim);
      vueApp.subs2.timeS23 = timeDash(time1);
      console.log('time1: ' +  time1);
    }
  }
}

function setTimePick() {
  if (vueApp.timeELim>= vueApp.timeSLim) {
    if (vueApp.yMGo==0) {
      if (vueApp.yM==0) {
        var time9 = vueApp.timeSLim;
      } else if (vueApp.yM==10) {
        var time9 = vueApp.timeELim;
      }
    } else {
      var time9 = Number(vueApp.subs2.timeS1.replaceAll("-","")) + vueApp.yMGo * 10000;
    }
    vueApp.subs2.timeS1 = timeDash(time9);
  }
}

function timeDash(t1) {
  var t2 = t1.toString();
  if (t2.length==6) {
    return t2.slice(0,4) + "-" + t2.slice(4,6) 
  }
  return t2.slice(0,4) + "-" + t2.slice(4,6) + "-" + t2.slice(6,8)
}

// addDataList_(ID) {
function addDataList(ID) {
  var list1=document.getElementById("data"+ID);

  for(var key in dataList) {
    if (key.slice(0,5)==="group") {
      var og = document.createElement("OPTGROUP");
      og.setAttribute('label', dataList[key][0]);
      list1.add(og);

    } else {
      var toAdd = true;

      // whether the dataset has only 2D or only 3D variables
      if   ( dList[ID-1]["only2D"] 
        ||  dList[ID-1]["only3D"] ) {
        var dims = "";
        var varList2 = dataList[key][1];  
        for(var i=0; i<varList2.length; i++)   
          dims += String(varList[ varList2[i] ][2]);

        if   ( dList[ID-1]["only2D"] ) 
          if (dims.indexOf('2')==-1) toAdd = false;
        if   ( dList[ID-1]["only3D"] ) 
          if (dims.indexOf('3')==-1) toAdd = false;
      }
  
      // add to the option group
      if (toAdd) og.appendChild(new Option(key,key));
    }
  }
}

// ajaxCall__
function ajaxCall(service) {

  vueApp.action1Disabled = true;
  vueApp.downloadDataDisabled = true;


  vueApp.responseHtml = "Calculating ...";
  vueApp.dataUrl = "Calculating ...";
  vueApp.plotUrl = "";
  //vueApp.imageHtml = "Image will appear here.";
  //$("#image").html("Image will appear here.");

  // for localhost:
  //var url = "http://" + window.location.hostname + ":" + window.location.port + "/svc/" + service + "?";

  // for deployment
  var url = "https://" + window.location.hostname + "/svc/" + service + "?";
  var argList = makeQueryStr(true);
  url = url + argList;
  console.log("server url:");
  console.log(url);

  $.ajax({
    type: "GET",
    url: url,
    dataType: "json",
    data: null,
    success: function(data, textStatus, xhr) {
      Response = data;
      var message1 = data.message;
      var text = JSON.stringify(data, null, 4);

      console.log(data.success);
      if (data.success == false) {
        console.log(data.message);
        if (data.message.search('failedCheck')>-1) {
          message1 = data.message.slice(14);
        } 
        console.log(data.message);

          //if (text.indexOf("No Data") != -1) {
          //  //vueApp.imageHtml = "No Data";
          //  $("#image").html("No Data.");
          //  vueApp.dataUrl = "No Data";
          //  vueApp.responseHtml = data.message;
          //  vueApp.action1Disabled = false;
          //  return;
          //}

          //text = "Error in backend: <br>" + text; 
          //text = "<span style='color:red'>" + text + "</span>";
          //vueApp.responseHtml = text;
        //} // if message.slice(0,2)=='99'

        
        vueApp.responseHtml = message1;
        //vueApp.plotUrl = "";
        //vueApp.dataUrl = "No data file due to backend error.";
        vueApp.dataUrl = "";
        vueApp.action1Disabled = false;
        vueApp.downloadDataDisabled = true;
        return;
      }  // if (data.success == false)

      // alert(text);
      vueApp.responseHtml = message1;
      vueApp.plotUrl = data.url;
      vueApp.dataUrl = data.dataUrl;
      vueApp.action1Disabled = false;
      vueApp.downloadDataDisabled = false;
      if (data.dataUrl==="") {
        vueApp.downloadDataDisabled = true;
      }

    }, // success: function(data, textStatus, xhr)
    error: function(xhr, textStatus, errorThrown) {
        vueApp.responseHtml = "<font color='red'>error!</font>";
        vueApp.dataUrl = "error!";
        vueApp.action1Disabled = false;
        // alert("xhr.status: "+xhr.status);
        // alert("error status: "+textStatus);
    }, // success: function()
    complete: function(xhr, textStatus) {
        //alert("complete status: "+textStatus);
    },
  }); // .ajax
} // action1.click


// combineList__
function combineLists(lists) {
  if (lists.length==0) { return null }
  if (lists.length==1) { return lists[0] }

  var dict1 = {};
  var list1; 
  for (var i1=0; i1<lists.length; i1++) { //>
    list1 = lists[i1];
    for (var i2=0; i2<list1.length; i2++) { //>
      try { dict1[list1[i2]] +=1;}
      catch(err) { dict1[list1[i2]] = 1; }
    }
  }
  return Object.keys(dict1);
}

// urlDirect_() {
function urlDirect() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    return this.key0 + '=' + vueApp[this.key1];
  }
  this.toHtml = function(vq){
    vueApp[this.key1] = vq;
  }
}

// urlCheckbox_() {
// it is the same as checkbox2num()
function urlCheckbox() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    if ( document.getElementById(this.key1).checked ) {
      return 1;
    } else {
      return 0;
    }
  }
  this.toHtml = function(vq){
    if ( Number(vq)==1 ) {
      $("#"+this.key1).prop('checked', true);
      $("#"+this.key1).change();
    } else {
      $("#"+this.key1).prop('checked', false);
    }
  }
}

// urlYearMonthDay_() {
function urlYearMonthDay() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = vueApp[this.key1];
    vq = vq.split("-").join("");
    return this.key0 + '=' + vq;
  }
  this.toHtml = function(vq){
    if (vq.length>6) {
      vueApp[this.key1] = vq.slice(0,4) + "-" + vq.slice(4,6) + "-" + vq.slice(6,8);
    } else {
      vueApp[this.key1] = vq.slice(0,4) + "-" + vq.slice(4,6);
    }
  }
}

// urlYearMonth_() {
function urlYearMonth() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = vueApp[this.key1];
    vq = vq.split("-").join("");
    return this.key0 + '=' + vq;
  }
  this.toHtml = function(vq){
    vueApp[this.key1] = vq.slice(0,4) + "-" + vq.slice(4,6);
  }
}

// urlTime_() {
// {'timeS': ['timeS', 'timeFull', 'f', 'anomaly', 'a']}
function urlTime() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.toCheck = arg99.slice(2);
  this.fromHtml = function(){
    var vq = $("#"+this.key1).val();
    //vq = vq.replace("-", "");
    vq = vq.split("-").join("");
    //console.log(this.toCheck.length);
    if (this.toCheck.length>1) {
      if ($("#"+this.toCheck[0]).is(":checked")) { 
        vq = vq + "_" + this.toCheck[1];
      }
    }

    if (this.toCheck.length>3) {
      if ($("#"+this.toCheck[2]).is(":checked")) { 
        vq = vq + "_" + this.toCheck[3];
      }
    }

    return vq;
  }

  this.toHtml = function(vq){
    if (vq.length==6) {
      vq = vq.slice(0,4) + "-" + vq.slice(4,6);
    } else {
      vq = vq.slice(0,4) + "-" + vq.slice(4,6) + "-" + vq.slice(6,8);
    }
    $("#"+this.key1).val(vq);
    $("#"+this.key1).change();
  }
}

// urlDate_() {
// {'timeS': ['timeS', 'timeFull', 'f', 'anomaly', 'a']}
function urlDate() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.toCheck = arg99.slice(2);
  this.fromHtml = function(){
    var vq = $("#"+this.key1).val();
    vq = vq.replace("-", "");
    if ($("#"+this.toCheck[0]).is(":checked")) { 
      vq = vq + "_" + this.toCheck[1];
    }
    if ($("#"+this.toCheck[2]).is(":checked")) { 
      vq = vq + "_" + this.toCheck[3];
    }
    return vq;
  }

  this.toHtml = function(vq){
    vq = vq.slice(0,4) + "-" + vq.slice(4,6);
    $("#"+this.key1).val(vq);
    $("#"+this.key1).change();
  }
}

// urlEscape_() {
function urlEscape() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = vueApp[this.key1];
    return this.key0 + '=' + escape(vq);
  }
  this.toHtml = function(vq){
    vq = unescape(vq);
    vueApp[this.key1] = vq;
  }
}

// url2escape_() {
function url2escape() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = vueApp[this.key1];
    return this.key0 + '=' + escape(vq);
  }
  this.toHtml = function(vq){
    vq = unescape(vq);
    vq = unescape(vq);
    vueApp[this.key1] = vq;
  }
}

// urlModel__() {
function urlModel() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = vueApp[this.key1];
    return this.key0 + '=' + vq;
  }
  this.toHtml = function(vq){
    //var vq1 = vq.replace("_", "/"); 
    var vq1 = vq;
    vueApp[this.key1] = vq1;
  }
}


// urlMultiModel__() {
function urlMultiModel() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = vueApp[this.key1];
    var str1 = '';
    for (var ii=0; ii<vq.length; ii++) {
      str1 += vq[ii].replace("/", "_") + ',';
    }
    return str1.slice(0, -1);
  }
  this.toHtml = function(vq){
    var vq1 = vq.split(",");
    for (var ii=0; ii<vq1.length; ii++) {
      vq1[ii] = vq1[ii].replace("_", "/"); 
    }
    vueApp[this.key1] = vq1;
  }
}

// urlRadioTwo_() {
function urlRadioTwo() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.radio1 = arg99[2];
  this.radio2 = arg99[3];
  this.fromHtml = function() {
    if ( document.getElementById(this.radio1).checked ) {
      return "1";
    } else { 
      return "0";
    }
  }
  this.toHtml = function(vq) {
    vq = Number(vq);
    //console.log(this.radio1);
    if (vq == 1) { 
      document.getElementById(this.radio1).checked = true;
      document.getElementById(this.radio2).checked = false;
    } else { 
      document.getElementById(this.radio1).checked = false;
      document.getElementById(this.radio2).checked = true;
    }
  }
}

// urlDataUrl_() {
function urlDataUrl() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    //console.log(document.getElementById("download_data").disabled);
    //if (document.getElementById("download_data").disabled == false) {
    if (includeDataUrl) {
      vq = dataUrl;
    } else {
      vq = "";
    }
    return vq;
  }

  this.toHtml = function(vq){
    vq = unescape(vq);
    $("#"+this.key1).val(vq);
    $("#"+this.key1).change();
  }
}

// urlMonths_() {
function urlMonths() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    vq = getMonthStr('');
    return vq;
  }

  this.toHtml = function(vq){
    select_months_from_str(vq, '');
  }
}

// urlScale1_() {
function urlScale1() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    return scale2num1();
  }

  this.toHtml = function(vq){
    var vq1 = Number(vq);
    num2scale1(vq1);
  }
}

// urlScale1a_() {
function urlScale1a() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    return scale2num1a();
  }

  this.toHtml = function(vq){
    var vq1 = Number(vq);
    num2scale1a(vq1);
  }
}

// urlScale2_() {
function urlScale2() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    return scale2num2();
  }

  this.toHtml = function(vq){
    var vq1 = Number(vq);
    num2scale2(vq1);
  }
}

// urlScale3_() {
function urlScale3() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    return scale2num3();
  }

  this.toHtml = function(vq){
    var vq1 = Number(vq);
    num2scale3(vq1);
  }
}

// urlNumber_() {
function urlNumber() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = $("#"+this.key1).val();
    vq = parseNum(vq);
    return vq;
  }

  this.toHtml = function(vq){
    $("#"+this.key1).val(vq);
    $("#"+this.key1).change();
  }
}

// urlNumberCheck_() {
function urlNumberCheck() {
  var vq;
  this.key0 = key99;
  this.key1 = arg99[0];
  this.check = arg99[2];
  if (arg99.length>3) {
    this.valueDf = arg99[3];
  } else {
    this.valueDf = "-999999";
  } 

  this.fromHtml = function(){
    var vq;
    if ( document.getElementById(this.check).checked ) {
      vq = $("#"+this.key1).val();
      vq = parseNum(vq);
    } else {
      vq = this.valueDf;
    }
    return vq;
  }

  this.toHtml = function(vq){
    $("#"+this.key1).val(vq);
    $("#"+this.key1).change();
  }
}


// urlPres_() {
function urlPres() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var vq = vueApp[this.key1];
    //console.log(vq);
    vq =  parse_pres(vq);
    //console.log(vq);
    return this.key0 + '=' + vq;
  }
  this.toHtml = function(vq){
    if (vq=="-999999") {
      vq = "500";
    }
    vueApp[this.key1] = vq;
  }
}

// urlSubs__
function urlSubs() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var dataset9, var9, dim2, subs2, t1;
    var dim2a, subs2a;
    var subs1 = jQuery.extend({}, subs0);
    for (var i=0; i<vueApp.datasetSelected.length; i++){ 
      dataset9 = vueApp.fileDict[vueApp.datasetSelected[i]];
      var9 = dataset9.varDict[vueApp.varSelected[i]];
      dim2 = var9.dim2;
      subs2 = var9.subs2;
      //console.log(vueApp.datasetSelected[i]);
      //console.log(var9);
      //console.log(dim2);
      //console.log(subs2);

      if (i==0) {
        dim2a = dim2;
        subs2a = subs2;
      }
      //console.log('in toHiml. ' + var9.units);
      //console.log('in toHiml. ' + subs2.lonMethod);
      cumSubs(subs1, dim2, subs2, 'lon', 'lon'); 
      cumSubs(subs1, dim2, subs2, 'lat', 'lat'); 
      cumSubs(subs1, dim2, subs2, 'pres', 'z'); 
      cumSubs(subs1, dim2, subs2, 'time', 'time'); 
    }

    if (vueApp.datasetSelected.length>1) {
      forMethod3(subs1, subs2a, 'lon');
      forMethod3(subs1, subs2a, 'lat');
      forMethod3(subs1, subs2a, 'pres');
      forMethod3(subs1, subs2a, 'time');
    } 

    var t1 = 
          subs2Url(subs1, 'lon')
        + subs2Url(subs1, 'lat')
        + subs2Url(subs1, 'pres')
        + subs2Url(subs1, 'time');
    t1 = t1.slice(0,-1);
    return t1;
  }

  this.toHtml = function(vq){
     
  }
}

// t1 = (dim2.indexOf('time')>-1)? subs2.timeMethod : '0';
// subs1.timeMethod += t1 + ',';
// t1 = (subs2.timeMethod=='1'? subs2.timeS1 : subs2.timeS23;
// subs1.timeS += t1 + ',';
// subs1.timeE += subs2.timeE + ',';
    

// cumSubs__
function cumSubs(subs1, dim2, subs2, ax1, ax2) {
      var t1, tS, tE;
      t1 = (dim2.indexOf(ax2)>-1)? subs2[ax1+'Method'] : '0';
      subs1[ax1+'Method'] += t1 + ',';
      tS = (subs2[ax1+'Method']=='1')? subs2[ax1+'S1'] : subs2[ax1+'S23'];
      tE = subs2[ax1+'E'];
      if (ax1=='pres') {
        tS = Number(tS);
        tE = Number(tE);
      }
      subs1[ax1+'S'] += tS + ',';
      subs1[ax1+'E'] += tE + ',';
}

// forMethod3__
function forMethod3(subs1, subs2a, ax1) {
  var tS, tE;
  if (subs2a[ax1+'Method']=='3') {
    subs1[ax1+'Method'] = ax1 + 'Method=';
    subs1[ax1+'S'] = ax1 + 'S=';
    subs1[ax1+'E'] = ax1 + 'E=';
    for (var i=0; i<vueApp.datasetSelected.length; i++){ 
      subs1[ax1+'Method'] += subs2a[ax1+'Method'] + ',';
      tS = subs2a[ax1+'S23'];
      tE = subs2a[ax1+'E'];
      if (ax1=='pres') {
        tS = Number(tS);
        tE = Number(tE);
      }  
      subs1[ax1+'S'] += tS + ',';
      subs1[ax1+'E'] += tE + ',';
    }
  }
}

// t1 += subs1.lonMethod.slice(0,-1) + '&' 
//      + subs1.lonS.slice(0,-1) + '&'
//      + subs1.lonE.slice(0,-1) + '&';

// subs2Url__
function subs2Url(subs1, ax1) {
  if (vueApp.datasetSelected.length>0){ 
    var t1 = subs1[ax1+'Method'].slice(0,-1) + '&' 
            + subs1[ax1+'S'].slice(0,-1) + '&'
            + subs1[ax1+'E'].slice(0,-1) + '&';
  } else {
    var t1 = subs1[ax1+'Method'] + '&' 
            + subs1[ax1+'S'] + '&'
            + subs1[ax1+'E'] + '&';
  }
  return t1;
}

// urlPlotP__
function urlPlotP() {
  this.fromHtml = function() {
    var plotP1 = jQuery.extend({}, plotP0);
    var plotP2;
    for (var i=0; i<vueApp.service9.nPlot; i++){ 
      //console.log(plotP1.ferretLevel);
      plotP2 = vueApp.plotP9[i]; 
      plotP1.ferretLevel += plotP2.ferretLevel.replace(/,/g,'_C_') + ',';
      plotP1.colorMap += plotP2.colorMap + ',';
      plotP1.plotTitle += plotP2.plotTitle + ',';
    }    
    var t1= plotP1.ferretLevel.slice(0,-1) + '&'
         + plotP1.colorMap.slice(0,-1) + '&'
         + plotP1.plotTitle.slice(0,-1);
     //console.log(t1);
     return t1;
  }
}

// urlTimeMean___
function urlTimeMean() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.key2 = arg99[2];
  this.fromHtml = function(){
    return this.key0 + '=' + vueApp[this.key1];
  }
  this.toHtml = function(vq){
    vueApp[this.key1] = vq;
    if (vq=='y') {
      vueApp.yearMean = true;
      vueApp.quarterMean = false;
    } else if (vq=='q') {
      vueApp.yearMean = false;
      vueApp.quarterMean = true;
    } else {
      vueApp.yearMean = false;
      vueApp.quarterMean = false;
    }
  }
}

// urlAxisMethod__() {
function urlAxisMethod() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.key2 = arg99[2];
  this.fromHtml = function(){
    var temp1 = (vueApp.dim2.indexOf(this.key2)>-1)? vueApp[this.key1] : '0';
    return this.key0 + '=' + temp1;
  }
  this.toHtml = function(vq){
    if (vq=='0') {
      vueApp[this.key1] = '1';
    } else {
      vueApp[this.key1] = vq;
    }
  }
}

// urlDatasets__() {
function urlDatasets() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.key2 = arg99[2];
  this.fromHtml = function(){
    return this.key0 + '=' + vueApp[this.key1];
  }
  this.toHtml = function(vq){
    vueApp.datasets = vq;
    vueApp.datasetFiltered = vq.split(',');
    vueApp.datasetSelected = vq.split(',');
    vueApp.datasetSelected0 = vq.split(',');

    vueApp.changeSearchText();
    //vueApp.changedDatasetSelected();
    //vueApp.changedBeingSubsetted();

    //console.log(which2Subset);
    vueApp.which2Subset0 = '1';
    vueApp.which2Subset = '1';

    for (var ii=0; ii<vueApp.datasetSelected.length; ii++) {
      var temp2 = vueApp.datasetFiltered[ii];
      //console.log(temp2)
      vueApp.datasetFilteredDict[temp2] = {'order':(ii+1).toString(), 'var':vueApp.fileDict[temp2].varList[0]};
      //vueApp.datasetFilteredDict[temp2] = {'order':(ii+1).toString(), 'var':''};
    }
  }
}

// urlVars__() {
function urlVars() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.key2 = arg99[2];
  this.fromHtml = function(){
    return this.key0 + '=' + vueApp[this.key1];
  }
  this.toHtml = function(vq){
    vueApp.vars = vq;
    var vars = vueApp.vars.split(',');
    for (var ii=0; ii<vueApp.datasetSelected.length; ii++) {
			var temp2 = vueApp.datasetSelected[i];
			vueApp.datasetFilteredDict[temp2].var = vars[ii];
    }

    vueApp.changeSearchText();
    //vueApp.changedDatasetSelected();
    //vueApp.changedBeingSubsetted();
    //console.log(which2Subset);
  }
}


// urlCoeff__() {
// urlList__() {
function urlList() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.fromHtml = function(){
    var t1 = "";
//zzzz
    for (var iii=0; iii<vueApp.datasetSelected.length+1; iii++){ 
      t1 += vueApp.coeff[iii]+",";
    }
    t1 = t1.slice(0,-1);
    return this.key0 + '=' + t1;
  } 
  this.toHtml = function(vq){
  }
}

// urlVars__() {
function urlVars() {
  this.key0 = key99;
  this.key1 = arg99[0];
  this.key2 = arg99[2];
  this.fromHtml = function(){
    return this.key0 + '=' + vueApp[this.key1];
  }
  this.toHtml = function(vq){
    vueApp.vars = vq;
    vueApp.varSelected = vq.split(',');
    vueApp.changed2a += 1;
    //vueApp.changed2b += 1;
  }
}
