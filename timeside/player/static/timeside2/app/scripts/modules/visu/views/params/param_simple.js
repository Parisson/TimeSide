define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  /**
    Parameter simple window
      
  **/
  return BaseQeopaView.extend({

    template: templates['visu/param_simple'],
    className: 'param-simple',

    ui: {
        
    },
    events: {
        'click [data-layout="delete_track"]' : 'onDeleteTrack'
    },

    setDaddy : function(view) {
        //view = track_waveform or track_canvas
        this.daddy = view;
    },

    ////////////////////////////////////////////////////////////////////////////////////
    onDeleteTrack:function(ev) {
        A._v.trigCfg('ui_project.deleteTrack','',this.daddy);
    },      

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {

    },

    onRender:function() {
       
    },

    onDestroy: function () {     
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
