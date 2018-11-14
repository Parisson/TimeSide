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
      timeLabel : '[data-layout="time-indicator"]',

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
        'stop' : _.bind(this.stop,this),
        'loop' : _.bind(this.loop,this)
        };
      if (map[action])
        map[action]();
    },
    loop:function() {
      this.isLooping = !this.isLooping; //undefined -> true -> false
      A._i.setOnCfg('playerIsLooping',this.isLooping);
      if(this.isLooping)
        this.$el.find('[data-action="loop"]').addClass("active");
      else
        this.$el.find('[data-action="loop"]').removeClass("active");

    },

    play:function() {
      if (this.isPlaying) {
        this.isPlaying=false;
        this.$el.find('[data-action="play"]').removeClass("active");
        console.log("this.isPlaying is false, launching pause");
        return A.vent.trigger('audio:pause');
      }
      this.isPlaying=true;
      console.log("this.isPlaying is true, launching play");
      A.vent.trigger('audio:play',this.item.get('audio_url').mp3);
      this.$el.find('[data-action="play"]').addClass("active");
    },

    stop:function() {
      A.vent.trigger('audio:stop',this.item.get('audio_url').mp3);
      this.isPlaying=false;
      console.log("this.stop is true");
      this.$el.find('[data-action="play"]').removeClass("active");
    },



    onAudioTime:function(percent,valueSec) {
      
      var value = A.telem.formatTimeMs(valueSec*1000);
      //console.log('time : '+valueSec+" : "+value);
        this.ui.timeLabel.empty().append(value);
    },
   
   

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.item = A._i.getOnCfg('currentItem');
      A._v.onCfg('audio.newAudioTime','',this.onAudioTime,this);
    },

    onRender:function() {
       
    },

    onDestroy: function () {   

      A._v.offCfg('audio.newAudioTime','',this.onAudioTime,this);   
    },

    onDomRefresh:function() {
    },

    serializeData: function () {
      
    },


    
    
   
  });
});
