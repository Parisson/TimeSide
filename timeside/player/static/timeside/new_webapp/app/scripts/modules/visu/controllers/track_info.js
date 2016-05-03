define([
  '#qt_core/controllers/all',
  'd3'
],

function (A,d3) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      A._i.setOnCfg('trackInfoController',this);

      this.trackDuration = 25093;
      this.currentZoom=1; //means all visible
      this.currentStartTime = 0;
      this.currentEndTime = 25093;

      this.max_value=6000;
    },

    onDestroy : function() {
       
    },

    //////////////////////////////////////////////////////////////////////////////////////////////
    //Update
    updateStartEndTimeFromNav:function(startTime,endTime) {
      this.currentStartTime = startTime;
      this.currentEndTime = endTime;
      this.currentZoom = this.trackDuration / (this.currentEndTime - this.currentStartTime);

      
    },

    //////////////////////////////////////////////////////////////////////////////////////////////
    //get set simple
    getDuration:function() {
      return this.trackDuration;
    },

    getNbPointVectoMax:function() {
      return 1024;
    },

    getCurrentZoom:function() {
      return this.currentZoom;
    },

    getCurrentStartTime:function() {
      return this.currentStartTime;
    },
    getCurrentEndTime:function() {
      return this.currentEndTime;
    },

    setMaxValue:function(arg) {
      this.max_value = arg;
    },
    getMaxValue:function() {return this.max_value;}


    

  

   

  });
});
