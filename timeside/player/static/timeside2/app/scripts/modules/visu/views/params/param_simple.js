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
