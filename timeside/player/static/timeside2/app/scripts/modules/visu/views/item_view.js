define([
   'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3',
  './subs/track_navigator',
  './subs/track_waveform',
  './subs/track_canvas'
],

function (Marionette,A,BaseQeopaView,d3,TrackNavigatorView,TrackWaveformView,TrackCanvasView) {
  'use strict';

  return BaseQeopaView.extend({

      template: templates['visu/item_view'],
    className: 'item_view',

    ui: {
      
    },
    events: {
      
    },


    

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.item = A._i.getOnCfg('currentItem');
    },

    onRender:function() {
    },
       

    onDestroy: function () {      
    },

    onDomRefresh:function() {
    },

    serializeData: function () {
      

      return {
        item : this.item.toJSON()
      }
    },


    
    
   
  });
});
