define([
  '#qt_core/controllers/all',
  'd3',
  './base_dataprovider'
],

/**
  Waveforme data provider
    has typeData and this.view to the view
**/
function (A,d3,BaseDataProvider) {
  'use strict';

  return BaseDataProvider.extend({
    initialize: function (options)	 {
      this.base_init();
      this.globalData = [];
      this.specificData = [];

      this.CONST_NUMPOINTS = 1024;

      this.CONST_DELTAZOOM_DONTGETDATA = 3; //cette valeur est énorme... A surveiller

      //Nombre de fois que l'on veut avoir AU MINIMUM le specific data avant et après la fenêtre en cours
      this.CONST_LENGTH_SPECIFICDATA_MIN_CACHE = 1; 

      //Nombre de fois que l'on peut avoir AU MAXIMUM le specific data avant et après la fenêtre en cours
      this.CONST_LENGTH_SPECIFICDATA_MAX_CACHE = 2;       
    },

    onDestroy : function() {
      this.base_destroy();
    },


    /////////////////////////////////////////////////////////////////////////////
    //initialization : get global data and keep it
    init:function() {
      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      this.specificDataStartTime = 0; //in base
      this.specificDataEndTime = trackDuration; //in base

      var useFakeData = A._i.getOnCfg('useFakeData');
      if (useFakeData)
        A._v.trigCfg('fakeserver.getdata','','waveform',0,trackDuration,this.CONST_NUMPOINTS,_.bind(this.onData,this));
      else
        A._v.trigCfg('trueserver.getdata','','waveform',0,trackDuration,this.CONST_NUMPOINTS,this.resultAnalysis, _.bind(this.onData,this));
    },

    onData:function(data) {
      this.globalData = data;
      this.specificData = data;
      this.getUpdatedDataForView();
    },

    /////////////////////////////////////////////////////////////////////////////
    //View request for data

    //uses trackInfo to know zoom/positions
    getUpdatedDataForView:function() {

      var nbItemMax = A._i.getOnCfg('trackInfoController').getNbPointVectoMax();
      //1 return 'best' available data
      var testData = this.weHaveProperData();

      this.view.setVisibleData(testData.availableData);

      //2 do we need more proper data ? 
      if (testData.needsSpecificData) {
        this.loadSpecificData();
      }
    },

    /////////////////////////////////////////////////////////////////////////////
    //Specific data loading

    loadSpecificData:function(reloadViewAfter) {
      var zoom = A._i.getOnCfg('trackInfoController').getCurrentZoom();
      var windowStart = A._i.getOnCfg('trackInfoController').getCurrentStartTime();
      var windowEnd = A._i.getOnCfg('trackInfoController').getCurrentEndTime();

      var neededSegment = this.getSpecificDataNeededSegment(windowStart,windowEnd);

      var timeStart = neededSegment.start;
      var timeEnd = neededSegment.end;
      var duration = timeEnd-timeStart;



      var self=this;  
      //Warning : we ask 3 more points because getSpecificDataNeededSegment va multiplier par 3 le segment demandé au serveur
      A._i.getOnCfg('dataLoader').askNewData(this.typeData,timeStart,timeEnd,this.CONST_NUMPOINTS*3,
        this.resultAnalysis,
        function(data) {
          self.specificData=data;
          self.specificDataStartTime = timeStart;
          self.specificDataEndTime = timeEnd;
          console.log('ZOOM IS NOW : '+zoom);
          self.zoomSpecificData = zoom;
          var _specificDataForView=self.getSpecificDataOnSegment(windowStart,windowEnd);
          self.view.setVisibleData(_specificDataForView);
        });
      //A._v.trigCfg('fakeserver.getdata','','waveform',timeStart,timeEnd,this.CONST_NUMPOINTS,_.bind(this.onSpecificData,this));
    },


    /////////////////////////////////////////////////////////////////////////////
    //Specific data tests

    /*Func test to check if we have proper data available, returns the 'best' data available right now
      so from global if that is the case
        returns : 
          {
            needsSpecificData : true|false,
            willUpdateViewWithSpecificData : true|false, 
              on peut vouloir du specific data cause on mord sur la fenêtre, mais sans besoin de remettre la vue
              à jour après
            availableData : [points {time/value}]
          }
      */
    weHaveProperData:function() {
      var zoom = A._i.getOnCfg('trackInfoController').getCurrentZoom();
      var timeStart = A._i.getOnCfg('trackInfoController').getCurrentStartTime();
      var timeEnd = A._i.getOnCfg('trackInfoController').getCurrentEndTime();

      //#1 si le zoom est à 1, on voit tout et on renvoie 
      if (zoom===1) {
        return {
          needsSpecificData : false,
          willUpdateViewWithSpecificData : false,
          availableData : this.globalData
        };
      }

      var zoomTrueChange = Math.abs(zoom - this.zoomSpecificData)>this.CONST_DELTAZOOM_DONTGETDATA;
      console.log("Zoom {"+zoomTrueChange+"? "+zoom+","+this.zoomSpecificData
        +"}, INTS : wanted : ("+timeStart+"--"+timeEnd+") spec avail : ("+this.specificDataStartTime+"--"+this.specificDataEndTime+")");

      //#2 si le zoom n'a pas ASSEZ changé, a-t-on la data en specific disponible ??? 
      if (! zoomTrueChange) {

        if (timeStart>=this.specificDataStartTime && timeEnd<=this.specificDataEndTime) {
          //ici, on a la donnée specifique disponible
          var intersectedData = this.getSpecificDataOnSegment(timeStart,timeEnd);
          var needNewData = this.needNewSpecificData();
          return {
            needsSpecificData : needNewData,
            willUpdateViewWithSpecificData : false,
            availableData : intersectedData
          };
        }
        //ici, nous n'avons pas la donnée spécifique disponible
        var globalIntersectedData = this.getGlobalDataOnSegment(timeStart,timeEnd);
        return {
            needsSpecificData : true,
            willUpdateViewWithSpecificData : true,
            availableData : globalIntersectedData
          };
      }

      //#3 zoom très différent
      var globalIntersectedData = this.getGlobalDataOnSegment(timeStart,timeEnd);
      return {
          needsSpecificData : true,
          willUpdateViewWithSpecificData : true,
          availableData : globalIntersectedData
        };

    },

    //////////////////////////////////////////////////////////////////////////////////////////
    //Tests

    //needNewSpecificData ? (respecte-t-on la fenêtre minimale ? )
    needNewSpecificData:function(timeStart,timeEnd) {
      var segment = this.getSpecificDataNeededSegment();

      if (timeStart < segment._start)
        return true;
      if (timeEnd > segment._end)
        return true;
      return false;
    },

    //renvoie les bornes théoriques du specific data à avoir
    getSpecificDataNeededSegment:function(timeStart,timeEnd) {
      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      var intervalDuration = timeEnd - timeStart;

      var _start = Math.max(0,timeStart - this.CONST_LENGTH_SPECIFICDATA_MIN_CACHE*intervalDuration);
      var _end = Math.min(trackDuration,timeEnd + this.CONST_LENGTH_SPECIFICDATA_MIN_CACHE*intervalDuration);

      return {start : _start, end : _end};
    },

    //////////////////////////////////////////////////////////////////////////////////////////
    //Get data
    //renvoie les points spécifiques disponibles sur l'intervalle
    getSpecificDataOnSegment:function(timeStart,timeEnd) {
      var result = [];
      _.each(this.specificData,function(_data) {
        if (_data.time>=timeStart && _data.time <=timeEnd)
          result.push(_data);
      });

      A.log.log('WaveformDataProvider','getSpecificDataOnSegment from : '+this.specificData.length+"pts -> "+result.length+"pts");

      return result;
    },

    //renvoie les points globaix disponibles sur l'intervalle
    getGlobalDataOnSegment:function(timeStart,timeEnd) {
      var result = [];
      _.each(this.globalData,function(_data) {
        if (_data.time>=timeStart && _data.time <=timeEnd)
          result.push(_data);
      });

      return result;
    },



   

  });
});

