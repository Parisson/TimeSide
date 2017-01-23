define([
  'jquery',
  'marionette',
  'underscore',
  'vent',
  '#behaviors/index',
  '#qt_core/controllers/config'
],
function ($,Marionette, _, vent,behaviors,Cfg) {
  'use strict';

  /****
  Popup behavior
    Looks for button.btn_close to make popup close (wahou)

  ****/
  return Marionette.Behavior.extend({



    events : {
      'click button.btn_close' : 'onClickClose'
    },
   
    initialize: function () {
      
    },

    //////////////////////////////////////////////////////////////////
    onRender:function() {
     
    },

    //destroy hook
    onBeforeDestroy:function() {
    },

    onClickClose:function() {
      vent.trigger('popup:forceclose');
    }



    
  });
});
