define([
  '#qt_core/controllers/all',
  'd3',
  './base_dataprovider'
],

/**
  Waveforme data provider
    has typeData and this.view to the view


  !!!!
    les data seront des objets Image() !!!


  Bug inquiry
      cf getSpecificDataOnSegment
**/
function (A,d3,BaseDataProvider) {
  'use strict';

  var debug_id=1;

  return BaseDataProvider.extend({
    initialize: function (options)	 {
      this.base_init();
      this.globalData = [];
      this.specificData = [];

      this.CONST_DELTAZOOM_DONTGETDATA = 0.1;

      this.CONST_WIDTH_BITMAP_GENERATED = 800;
      this.CONST_HEIGHT_BITMAP_GENERATED = 200;

      //Nombre de fois que l'on veut avoir AU MINIMUM le specific data avant et après la fenêtre en cours
      this.CONST_LENGTH_SPECIFICDATA_MIN_CACHE = 1; 

      //Nombre de fois que l'on peut avoir AU MAXIMUM le specific data avant et après la fenêtre en cours
      this.CONST_LENGTH_SPECIFICDATA_MAX_CACHE = 2;    

      this.debugId = debug_id++;   
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

      var callback = _.bind(this.onData,this);

      var useFakeData = A._i.getOnCfg('useFakeData');
      if (useFakeData)
        A._v.trigCfg('fakeserver.getdata','','testcanvas',0,trackDuration,-1,callback);
      else
        A._v.trigCfg('trueserver.getdata','','canvas',0,trackDuration,-1,this.resultAnalysis,_.bind(this.onData,this)); //@@TOD : //voir ce que récupère 
      //true server et faire en sorte qu'il appelle l'url dynamique du resultAnalysis sur cet objet

    },

    onData:function(data) {
      this.globalData = data;
      this.specificData = data;
      this.getUpdatedDataForView();
    },

      /////////////////////////////////////////////////////////////////////////////
    //Internal Canvas caching
    getCanvas:function() {
      var _canvas = A._i.getOnCfg('bitampdataprovider_canvas');
      if (! _canvas) {
        _canvas = document.createElement('canvas');
        A._i.setOnCfg('bitampdataprovider_canvas',_canvas);
      }

      _canvas.getContext('2d').clearRect(0, 0, _canvas.width, _canvas.height);
      return _canvas;
    },

    /////////////////////////////////////////////////////////////////////////////
    //View request for data

    //uses trackInfo to know zoom/positions
    getUpdatedDataForView:function() {

      //@TODO FROM HERE WORKING

      //1 return 'best' available data
      var testData = this.weHaveProperData();
      var availableData = testData.availableData;

      //mmmmm à confirmer
      this.view.hadFirstData = true;  

      //NON, maintenant, on écrit directement depuis ce cointroller
      //this.view.setVisibleData(testData.availableData);
      this.generateViewCanvas(availableData.source,availableData.pixelStart,availableData.pixelEnd);

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

      console.log('loadSpecificData on '+this.debugId);

      //inquiry
      /**
          Ici, on va demander de la nouvelle data sur un segment supérieur à ce qui est sélectionné
              segment available devrait être this.specificDataStartTime && End
              (jamais mis à jour)

          windowStart & windowEnd sont les sélectionnés par user
          timeStart et timeEnd sont eux les plus larges utilisés pour le cache
      **/


      var self=this;
      A._i.getOnCfg('dataLoader').askNewData(this.typeData,timeStart,timeEnd,-1,this.resultAnalysis,
        function(data) {
          console.log(' specific data got on : '+self.debugId);
          self.specificData=data; //is an img

          //test ED bug fix
          self.specificDataStartTime = timeStart;
          self.specificDataEndTime = timeEnd; //so getSpecificDataOnSegment will have a proper ratio

          //NON, écriture depuis le controller
          var _specificDataForView=self.getSpecificDataOnSegment(windowStart,windowEnd);

          //NON : écriture depuis le controller
          //self.view.setVisibleData(_specificDataForView);
          self.generateViewCanvas(_specificDataForView.source,_specificDataForView.pixelStart,_specificDataForView.pixelEnd);
        });
     
    },


    /////////////////////////////////////////////////////////////////////////////
    //Specific data tests

    /*
  NEW : 
    Cette méthode doit renvoyer en canvas
    {
            needsSpecificData : true|false,
            willUpdateViewWithSpecificData : true|false, 
              on peut vouloir du specific data cause on mord sur la fenêtre, mais sans besoin de remettre la vue
              à jour après
            availableData : MODIF : là c'est un objet : 
                {
                  source : global|specific  : OUI
                  pixelStart (source dependant)
                  pixelEnd (source dependant)
                }
          }


    ////////////////////------------------------
      Func test to check if we have proper data available, returns the 'best' data available right now
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
      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();

      //#1 si le zoom est à 1, on voit tout et on renvoie 
      if (zoom===1) {
        return {
          needsSpecificData : false,
          willUpdateViewWithSpecificData : false,
          availableData : this.getGlobalDataOnSegment(0,trackDuration)//this.globalData
        };
      }

      var zoomTrueChange = Math.abs(zoom - this.zoomSpecificData)>this.CONST_DELTAZOOM_DONTGETDATA;

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
      //on devrait pas demander un segment plus long ??

      return (timeStart < this.specificDataStartTime) || (timeEnd > this.specificDataEndTime);
    },

    //renvoie les bornes théoriques du specific data à avoir
    getSpecificDataNeededSegment:function(timeStart,timeEnd) {
      //ce truc devrait etre appeke????

      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      var intervalDuration = timeEnd - timeStart;

      var _start = Math.max(0,timeStart - this.CONST_LENGTH_SPECIFICDATA_MIN_CACHE*intervalDuration);
      var _end = Math.min(trackDuration,timeEnd + this.CONST_LENGTH_SPECIFICDATA_MIN_CACHE*intervalDuration);

      return {start : _start, end : _end};
    },

    //////////////////////////////////////////////////////////////////////////////////////////
    //Get data
    //renvoie les points spécifiques disponibles sur l'intervalle

    //NEW : ne renvoie que un objet avec le segment de pixels à conserver
    //WARN : il va renvoyer un pixel Start et pixelEnd en comparant timeStart/End (voulu) sur this.specificDataStartTime/End
    //Qui lui est tout le temps sur start et end et jamais mis à jour!

    getSpecificDataOnSegment:function(timeStart,timeEnd) {
      var durationSource = this.specificDataEndTime - this.specificDataStartTime;
      var ratioPointStart = (timeStart - this.specificDataStartTime)/durationSource;
      var ratioPointEnd = (timeEnd - this.specificDataStartTime)/durationSource;

      var pixelStart = Math.floor(this.specificData.width*ratioPointStart);
      var pixelEnd = Math.floor(this.specificData.width*ratioPointEnd);

      return {source : "specific", pixelStart : pixelStart, pixelEnd : pixelEnd};

      /*return this.getCuttedData(this.specificData,this.specificDataStartTime,this.specificDataEndTime,
        timeStart,timeEnd);*/

      
    },

    //renvoie les points globaix disponibles sur l'intervalle
    //NEW renvoie juste un objet d'infos
    getGlobalDataOnSegment:function(timeStart,timeEnd) {
      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      var durationSource = trackDuration;
      var ratioPointStart = (timeStart)/durationSource;
      var ratioPointEnd = (timeEnd)/durationSource;

      var pixelStart = Math.floor(this.globalData.width*ratioPointStart);
      var pixelEnd = Math.floor(this.globalData.width*ratioPointEnd);

      return {source : "global", pixelStart : pixelStart, pixelEnd : pixelEnd};


      /*return this.getCuttedData(this.globalData,0,this.trackDuration,
        timeStart,timeEnd);*/
    },


    //////////////////////////////////////////////////////////////////////////////////////////
    //New : Dessin sur le canvas de la vue
    generateViewCanvas:function(source,pixelStart,pixelEnd) {
      var canvas = this.view.canvas;
      var canvasContext = this.view.canvasContext;
      var data = source==="global" ? this.globalData : this.specificData;

      this.lastDrawInfos = {data : data, pixelStart : pixelStart, pixelEnd : pixelEnd};  

      canvasContext.drawImage(data,pixelStart,0,(pixelEnd-pixelStart),data.height,0,0,canvas.width,canvas.height);
    },

    //on resize height, called by view
    redrawSameCanvas:function() {
        if (this.lastDrawInfos) {
            var canvas = this.view.canvas;
            var canvasContext = this.view.canvasContext;

            canvasContext.drawImage(this.lastDrawInfos.data,this.lastDrawInfos.pixelStart,0,
              (this.lastDrawInfos.pixelEnd-this.lastDrawInfos.pixelStart),
              this.lastDrawInfos.data.height,0,0,canvas.width,canvas.height);            
        }
    },


    //////////////////////////////////////////////////////////////////////////////////////////
    //Generic cut data (only if possible)
    //New : deprecated
    getCuttedData:function(sourceData,sourceStart,sourceEnd,timeStart,timeEnd) {

      alert('TODO : il faut que le getCuttedData travailler directement sur le canvas de son track pour y produire directement le scale. Refactoring à réfléchir, donc');


      var durationSource = sourceEnd - sourceStart;
      var ratioPointStart = (timeStart - sourceStart)/durationSource;
      var ratioPointEnd = (timeEnd - sourceStart)/durationSource;

      var pixelStart = Math.floor(sourceData.width*ratioPointStart);
      var pixelEnd = Math.floor(sourceData.width*ratioPointEnd);


      A.log.log('bitmap_dataprovider','getCuttedData : source : ('+sourceStart+','+sourceEnd
        +'), times : ('+timeStart+','+timeEnd+'), sourceDataDims : '+sourceData.width+','+sourceData.height);

      var canvas = this.getCanvas();
      var context = canvas.getContext('2d');


      //ici sourceData est une image qu'il faut donc rescaler!!!
      canvas.width = this.CONST_WIDTH_BITMAP_GENERATED;
      canvas.height = this.CONST_HEIGHT_BITMAP_GENERATED;

      //A.log.log('bitmap_dataprovider','Creating image');

      context.drawImage(sourceData, pixelStart, 0, canvas.width,canvas.height,
        0, 0, (pixelEnd - pixelStart), sourceData.height);


      var croppedData = context.getImageData(0, 0, canvas.width, canvas.height);


      A.log.log('bitmap_dataprovider','Result is : '+croppedData.width+','+croppedData.height);
/*
      context.putImageData(sourceData, 0, 0 );
      var croppedData = context.getImageData(0, 0, (pixelEnd-pixelStart), sourceData.height);
*/
      return croppedData;

    },


   

  });
});

