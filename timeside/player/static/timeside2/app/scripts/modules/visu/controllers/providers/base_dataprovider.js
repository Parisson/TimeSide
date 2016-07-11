define([
  '#qt_core/controllers/all',
  'd3'
],

/**
  Base data provider
**/
function (A,d3) {
  'use strict';

  return Marionette.Controller.extend({

    //will be overrided
    initialize: function (options)	 {
      
    },

    //will be overrided
    onDestroy : function() {
      
    },

    base_init:function() {
      /*this.globalData = [];
      this.specificData = [];*/
      this.zoomSpecificData = 1; //on voit tout

      this.specificDataStartTime = 0;
      this.specificDataEndTime = NaN;


    },

    base_destroy:function() {
      this.view=undefined;
    },

    //////////////////////////////////////////////////////////


    define:function(typeData,view,resultAnalysis) {
      this.typeData = typeData;
      this.view = view;
      this.resultAnalysis = resultAnalysis;
    },

   

   

  });
});
