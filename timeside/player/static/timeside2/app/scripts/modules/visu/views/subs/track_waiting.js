define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  /**
    Waiting track : to show we asked for an analysis
     has an unique id from analysis controller
  **/
  return BaseQeopaView.extend({

    template: templates['visu/sub_track_waiting'],
    className: 'waiting-track',

    ui: {
     
    },
    events: {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////


    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    setUniqueId:function(uniqueId) {
      this.uniqueId = uniqueId;
    },

    getUniqueId:function() {
      return this.uniqueId;
    },
   
   
    
    ////////////////////////////////////////////////////////////////////////////////////
    //Generate graph
    

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {

      this.item = A._i.getOnCfg('currentItem');
     
    },

    onRender:function() {
       
    },

    onDestroy: function () {     
     
    },


    serializeData: function () {
      


      return {
        uniqueId : this.uniqueId 
      }
    },


    
    
   
  });
});
