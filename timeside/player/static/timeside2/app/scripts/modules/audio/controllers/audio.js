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
      /*console.error('TMP!!!!!!! replacing mp3 url');
      url = "/data/mp3chelou.mp3";*/

      if (this.sound) {
        this.destroySound();
      }
      this.sound = new buzz.sound(url);
      this.sound.bind('ended',_.bind(this.onSoundEnded,this));


      this.sound.bind('canplay',function(err) {console.log('====Can Play')});
      this.sound.bind('canplaythrough',function(err) {console.log('====Can Play Through')});
      this.sound.bind('error',function(err) {console.error('error on audio : '+err);console.dir(err);});
      this.sound.bind('sourceerror',function(err) {console.error('sourceerror on audio : '+err)});

      window.debsound = this.sound;
      this.sound.load();
      //this.sound.bind('timeupdate',_.bind(this.onTimeUpdate,this));
      return this.sound;  

    },

    destroySound:function() {
      if (this.updateInterval) {      
        console.log('clearing : '+this.updateInterval);
        clearInterval(this.updateInterval); 
        this.updateInterval=undefined;
      }
      this.sound.unbind('ended');
      this.sound.unbind('error');
      this.sound.unbind('sourceerror');
      this.sound.unbind('canplay');
      this.sound.unbind('canplaythrough');
      this.sound=undefined;
    },

    //////////////////////////////////////////////////////////////////////////////
    //Audio loading -- global

    loadGlobalFile:function(url) {
      //todo : load with buzz remote stuff
      if (this.sound)
        this.sound.stop();

      this.soundUrl = url; //temp

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

      if (this.updateInterval) {
        clearInterval(this.updateInterval);
        this.updateInterval=undefined;
      }

      this.isPlayingOnWebAudioApi=false;
      //TEST : if duration less than 5 secondes, web-api goes on!
      if (A._i.getOnCfg('currentLoopSegment') && A._i.getOnCfg('currentLoopSegment').length===2) {
        var windowStart = A._i.getOnCfg('currentLoopSegment')[0]; //ms
        var windowEnd = A._i.getOnCfg('currentLoopSegment')[1]; //ms
        if (Math.abs(windowEnd - windowStart)<5000) {
          //alert('goto webapi');
          this.isPlayingOnWebAudioApi=true;
          return A._i.getOnCfg('audioWebApiController').createSound(this.soundUrl); //done from loading
        }
      }


      //todo : load with buzz remote stuff
      if (this.sound) {
        this.sound.play();
        this.updateInterval = setInterval(_.bind(this.testTimeUpdate,this),30);
        console.log('*** Created interval : '+this.updateInterval);
      }

    },

    stopAudio:function() {
      if (this.isPlayingOnWebAudioApi) {
         return A._i.getOnCfg('audioWebApiController').stopAudio();
      }

      if (this.sound) {
        this.sound.stop();
      }
      if (this.updateInterval) {
        clearInterval(this.updateInterval);
        this.updateInterval=undefined;
      }

      this.testTimeUpdate();
    },
  
    pauseAudio:function() {
      if (this.isPlayingOnWebAudioApi) {
         return A._i.getOnCfg('audioWebApiController').stopAudio();
       }
      
      if (this.sound) {
        this.sound.pause();
      }
      if (this.updateInterval) {
        clearInterval(this.updateInterval);
        this.updateInterval=undefined;
      }
    },

    onSoundEnded:function() {
      if (this.updateInterval) {
        clearInterval(this.updateInterval);
        this.updateInterval=undefined;
      }
    },
   

    //////////////////////////////////////////////////////////////////////////////
    //Audio time sync
    //on percent of audio!!!
    setCurrentTime:function(fracTime) {
      var timePercent = fracTime*100;
      //console.log('setPercent on : '+fracTime+"=>"+timePercent);
      if (this.sound)
        this.sound.setPercent(timePercent);
    },


    testTimeUpdate:function() {
      var timeSound = this.sound.getTime() ;
      var percent =timeSound / this.sound.getDuration();

      A._v.trigCfg('audio.newAudioTime','',percent,timeSound);
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
