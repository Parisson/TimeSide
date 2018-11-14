define([
  '#qt_core/controllers/all',
  'd3'
],

/**
  Asked by TF : https://taiga.ircam.fr/project/yomguy-diadems/issue/77
    -> Deactivating

  You may want one day to use this fake data controller to make some basic tests, so its only commented in initialize

**/
function (A,d3) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      return; 

      /*var wave_uri = "./data/geiger.json";
      d3.json( wave_uri,_.bind(this.onJSONLoaded,this));   

      this.ready=false;

      A._v.onCfg('fakeserver.getdata','',this.onGetData,this);*/
    },

    onDestroy : function() {
       A._v.offCfg('fakeserver.getdata','',this.onGetData,this);
    },

    onJSONLoaded:function(error,json) {
      this.dataDuration = 25093;//ms (calculé en console, le json donne de la merde)
      var time = 0;
      this.alldata = _.map(json.data,function(_value) {
        var result = {value : _value, time : time}
        time+=(this.dataDuration/json.data.length);
        return result;
      },this);


      this.alldata2 = _.map(this.alldata,function(_obj) {
        return {time : _obj.time, value : _obj.value/2};
      },this)

      this.alldata3 = _.map(this.alldata,function(_obj) {
        return {time : _obj.time, value : _obj.value/4};
      },this)


      var urlPicture = '/data/picture.jpg';
      this.imgPicture = new Image();
      this.imgPicture.onload = _.bind(this.onPictureLoaded,this);
      this.imgPicture.src = urlPicture;
    },

      /////////////////////////////////////////////////////////////////////////////
    //Canvas caching
    getCanvas:function() {
      var _canvas = A._i.getOnCfg('fakeserver_canvas');
      if (! _canvas) {
        _canvas = document.createElement('canvas');
        A._i.setOnCfg('fakeserver_canvas',_canvas);
      }

      _canvas.getContext('2d').clearRect(0, 0, _canvas.width, _canvas.height);
      return _canvas;
    },

      /////////////////////////////////////////////////////////////////////////////
    //Picture loading
    onPictureLoaded:function() {
      this.ready=true;
    },

     /////////////////////////////////////////////////////////////////////////////
    //Global get data
    onGetData:function(type,startTime,endTime,nbItem,callback) {
      if (type==="waveform")
        return this._onGetData(startTime,endTime,nbItem,callback,this.alldata);
      else if (type==="test2")
        return this._onGetData(startTime,endTime,nbItem,callback,this.alldata2);
      else if (type==="test3")
        return this._onGetData(startTime,endTime,nbItem,callback,this.alldata3);
      else if (type==="testcanvas")
        return this._onGetBitmapData(startTime,endTime,callback);
    },

    /////////////////////////////////////////////////////////////////////////////
    //Get data picture
    //times are in MS
    _onGetBitmapData:function(startTime,endTime,callback,inputData) {

      var startPx = Math.floor(this.imgPicture.width * (startTime/this.dataDuration));
      var endPx = Math.floor(this.imgPicture.width * (endTime/this.dataDuration));

      A.log.log('fake_server','Calling bitmap for : '+startTime+','+endTime+' => '+startPx+','+endPx)

      var canvas = this.getCanvas();// document.createElement('canvas');
      var context = canvas.getContext('2d');

      canvas.width = (endPx-startPx);
      canvas.height = this.imgPicture.height;
      
      context.drawImage(this.imgPicture, startPx, 0 ,(endPx-startPx),this.imgPicture.height);
      //var croppedData = context.getImageData(0, 0, (endPx-startPx), this.imgPicture.height);

      var imageBack = new Image();
      imageBack.onload = function() {
        A.log.log('fake_server','returning bitmap ('+imageBack.width+','+imageBack.height+')');
        callback(imageBack);
      }
      imageBack.src = canvas.toDataURL();


      //callback(croppedData);
    },

    /////////////////////////////////////////////////////////////////////////////
    //Get data waveform
    //times are in MS
    _onGetData:function(startTime,endTime,nbItem,callback,inputData) {
      if (! this.ready)
        return console.error('leave me some time!');

      var result = [];

      //on convertit les temps en indexs dans alldata
      //on ne s'emmerde pas à checker les temps car on est linéaire à la création, mais attention!
      var indexStartInAllData = Math.floor(inputData.length * (startTime / this.dataDuration));
      var indexEndInAllData = Math.floor(inputData.length * (endTime / this.dataDuration));

      //@Todo : renvoyer soit que les valeurs disponibles s'il y en a, soit les valeurs moyennées
      //MAIS TIMESTAMPEES!!! C'est vraiment important

      //@Todo : prévoir qu'on peut avoir moins de valeurs de l'autre côté
      var nbIndexInAllData = indexEndInAllData - indexStartInAllData;
      if (nbIndexInAllData<nbItem) {
         result = inputData.slice(indexStartInAllData,indexEndInAllData);
      }
      else {
        //on récupère les valeurs qui nous intéressent
        var means = [], currentValuesForMean= [];
        var numEltPerMean = Math.floor((indexEndInAllData-indexStartInAllData)/nbItem);

        for (var i=indexStartInAllData; i<(Math.min(inputData.length,indexEndInAllData)); i++) {
          var val = inputData[i];
          if (currentValuesForMean.length>=numEltPerMean) {


              var values = [];
              var times = [];
              _.each(currentValuesForMean,function(_obj) {
                values.push(_obj.value);
                times.push(_obj.time);
              });

              means.push({value : d3.mean(values), time : d3.mean(times)});
              currentValuesForMean=[];
            }
            currentValuesForMean.push(val);
        }

        //from here
        result = means;
        if (result.length> nbItem)
          result = result.slice(0,nbItem);  
      }

      callback(result);


    }

  

   

  });
});
