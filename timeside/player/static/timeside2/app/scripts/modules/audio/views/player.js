define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview'
],

function (Marionette,A,BaseQeopaView) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['audio/player'],
    className: 'audio-player',

    ui: {
      
    },
    events: {
      'click [data-layout="action"]' : 'onClickAction'
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    onClickAction:function(ev) {
      var action = ev.currentTarget.dataset.action;
      var map = {
        'play' : _.bind(this.play,this), 
        'stop' : _.bind(this.stop,this)
        };
      if (map[action])
        map[action]();
    },


    play:function() {
      A.vent.trigger('audio:play',this.item.get('audio_url').mp3);
    },

    stop:function() {
      A.vent.trigger('audio:stop',this.item.get('audio_url').mp3);
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
      
    },


    
    
   
  });
});
