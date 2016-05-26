define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['navigation/home'],
    className: 'home-view',

    ui: {
      'btnNavigate' : 'button[data-viewid]'
    },
    events: {
      'click @ui.btnNavigate' : 'onNavigate'
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    onNavigate:function(ev) {
      var viewid = ev.currentTarget.dataset.viewid;
      A._v.trigCfg('navigate.page','',viewid);


    },



   
   

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      window.home = this;
    },

    onRender:function() {
       
    },

    onDestroy: function () {      
    },

    onDomRefresh:function() {
    },

    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
