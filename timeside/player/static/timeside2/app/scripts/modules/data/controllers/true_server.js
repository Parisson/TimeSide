define([
  '#qt_core/controllers/all',
  'd3'
],

function (A,d3) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      //this.ready=false;
      A._v.onCfg('trueserver.getdata','',this.onGetData,this);
    },

    onDestroy : function() {
       A._v.offCfg('trueserver.getdata','',this.onGetData,this);
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
      //this.ready=true;
    },

     /////////////////////////////////////////////////////////////////////////////
    //Global get data
    onGetData:function(type,startTime,endTime,nbItem,callback) {
      if (type==="waveform")
        return this._onGetWaveformData(startTime,endTime,nbItem,callback);
      /*else if (type==="testcanvas")
        return this._onGetBitmapData(startTime,endTime,callback);*/
    },

    /////////////////////////////////////////////////////////////////////////////
    //Get data picture
    //times are in MS
    _onGetBitmapData:function(startTime,endTime,callback,inputData) {

      /*var startPx = Math.floor(this.imgPicture.width * (startTime/this.dataDuration));
      var endPx = Math.floor(this.imgPicture.width * (endTime/this.dataDuration));

      A.log.log('fake_server','Calling bitmap for : '+startTime+','+endTime+' => '+startPx+','+endPx)

      var canvas = this.getCanvas();// document.createElement('canvas');
      var context = canvas.getContext('2d');

      canvas.width = (endPx-startPx);
      canvas.height = this.imgPicture.height;
      
      context.drawImage(this.imgPicture, startPx, 0 ,(endPx-startPx),this.imgPicture.height);

      var imageBack = new Image();
      imageBack.onload = function() {
        A.log.log('fake_server','returning bitmap ('+imageBack.width+','+imageBack.height+')');
        callback(imageBack);
      }
      imageBack.src = canvas.toDataURL();*/

    },

    /////////////////////////////////////////////////////////////////////////////
    //Get data waveform
    //times are in MS
    _onGetWaveformData:function(startTime,endTime,nbItem,callback) {
      var currentItem = A._i.getOnCfg('currentItem');
      var result = [];
      var data = {
        start : startTime,
        end : endTime,
        nb_pixels : nbItem,
        itemId : currentItem.get('uuid')
      };

      A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.items.waveform),data,null,
        function(result) {
          alert('so?');
        }, function(error) {
          alert("Non6");
      });


/*
      callback(result);*/


    }

  

   

  });
});
