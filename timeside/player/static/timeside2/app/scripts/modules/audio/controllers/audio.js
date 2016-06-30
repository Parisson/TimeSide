define([
  '#qt_core/controllers/all',
  'buzz'
],

function (A,buzz) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      A._v.onCfg('audio.loadGlobalFile','',this.loadGlobalFile,this);
      A._v.onCfg('audio.loadSpecificFile','',this.loadSpecificFile,this);
      A._v.onCfg('audio.play','',this.playAudio,this);
      A._v.onCfg('audio.pause','',this.pauseAudio,this);
      A._v.onCfg('audio.stop','',this.stopAudio,this);
      A._v.onCfg('audio.setCurrentTime','',this.setCurrentTime,this);

      //vital
      buzz.audioCtx=undefined;

       if (!buzz.isSupported()) {
        console.error(' Error : Buzz : sound not supported');
        return;
      } 
    },

    onDestroy : function() {
      A._v.offCfg('audio.loadGlobalFile','',this.loadGlobalFile,this);
      A._v.offCfg('audio.loadSpecificFile','',this.loadSpecificFile,this);
      A._v.offCfg('audio.play','',this.playAudio,this);
      A._v.offCfg('audio.pause','',this.pauseAudio,this);
      A._v.onCfg('audio.setCurrentTime','',this.setCurrentTime,this);
      A._v.offCfg('audio.stop','',this.stopAudio,this);
    },

     //////////////////////////////////////////////////////////////////////////////
    //Basic buzz functions
    createSound:function(url) {
      if (this.sound) {
        clearInterval(this.updateInterval);
        //this.sound.unbind('timeupdate');
      }
      this.sound = new buzz.sound(url);
      
      //this.sound.bind('timeupdate',_.bind(this.onTimeUpdate,this));
      return this.sound;  

    },

    //////////////////////////////////////////////////////////////////////////////
    //Audio loading -- global

    loadGlobalFile:function(url) {
      //todo : load with buzz remote stuff
      if (this.sound)
        this.sound.stop();

      this.sound = this.createSound(url);

      //temp for test
      //this.playAudio();
    },



    //////////////////////////////////////////////////////////////////////////////
    //Audio loading -- specific segment

    loadSpecificFile:function(url) {

    },


    //////////////////////////////////////////////////////////////////////////////
    //Audio play/pause

    playAudio:function() {
      //todo : load with buzz remote stuff
      if (this.sound) {
        this.sound.play();
        this.updateInterval = setInterval(_.bind(this.testTimeUpdate,this),50);
      }

    },

    stopAudio:function() {
      if (this.sound) {
        this.sound.stop();
        clearInterval(this.updateInterval);
      }
    },
  
    pauseAudio:function() {
      if (this.sound) {
        this.sound.pause();
        clearInterval(this.updateInterval);
      }


      
    },
   

    //////////////////////////////////////////////////////////////////////////////
    //Audio time sync
    //on percent of audio!!!
    setCurrentTime:function(fracTime) {
      var timePercent = fracTime*100;
      if (this.sound)
        this.sound.setPercent(timePercent);
    },


    testTimeUpdate:function() {

      var percent = this.sound.getTime() / this.sound.getDuration();
      A._v.trigCfg('audio.newAudioTime','',percent);
    },

    //DEPRECATED!!!! now pooling above
    onTimeUpdate:function(e) {
      var now = (new Date()).getTime();
      if (this.lastUpdateTime)
        console.log('Delta update time : '+(now - this.lastUpdateTime));

      this.lastUpdateTime = now;


      var percent = this.sound.getTime() / this.sound.getDuration();
      A._v.trigCfg('audio.newAudioTime','',percent);
      //@TODO do something with this percent!
    }    


  });
});
