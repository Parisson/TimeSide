define([
  '#qt_core/controllers/all'
],

/**
  Audio web-api controller.
    Now : called by audio.js when a play command is sent && the selected segment is 
      less than X.

    Now actually : test functions
**/

function (A,buzz) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      A._i.setOnCfg('audioWebApiController',this);

      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    },

    onDestroy : function() {
     
    },

     //////////////////////////////////////////////////////////////////////////////
    //Basic functions

    /**
      This will start loading the proper mp3 chunk
        @TODO : load the exact extract url, not the whole url
    **/
    createSound:function(url) {
      //tests loading sound
      var windowStart = A._i.getOnCfg('currentLoopSegment')[0]; //ms
        var windowEnd = A._i.getOnCfg('currentLoopSegment')[1]; //ms
      this.timeStartInSound = windowStart;
      this.timeEndInSound = windowEnd;

      var startSeconds = windowStart/1000;
      var stopSeconds = windowEnd/1000;
      url = url+"?start="+startSeconds+"&stop="+stopSeconds;
      
      this.soundRequest = new XMLHttpRequest();
      this.soundRequest.open('GET', url, true);
      this.soundRequest.responseType = 'arraybuffer';
      this.soundRequest.onload = _.bind(this.onSoundDownloaded,this);
      this.soundRequest.send();
    },

    onSoundDownloaded:function() {
      var audioData = this.soundRequest.response, self=this;

      
     
      this.audioCtx.decodeAudioData(audioData, function(buffer) {
        self.audioBuffer = buffer;//buffer;
        (_.bind(self.testPlay,self))();
      },
        function(e){
          console.error("Error with decoding audio data" + e.err);
      });
    },

    //old : tests de split de buffer. Argn
/*    OLD_onSoundDownloaded:function() {
      var audioData = this.soundRequest.response, self=this;

      
      var sampleRate = 48000; //TMP TOO
      //donc temporaire : ici, buffer est tout le sample
      var startIndexInBuffer = Math.round((this.timeStartInSound/1000)*sampleRate);
      var endIndexInBuffer = Math.round((this.timeEndInSound/1000)*sampleRate);
      //audioData = audioData.slice(startIndexInBuffer,endIndexInBuffer); //NON : THIS IS THE MP3 BINARY FILE!!!

      this.audioCtx.decodeAudioData(audioData, function(buffer) {
        //ici, buffer a duration (sec), length(nb echantillon) & sampleRate (int)
        console.error('WARN-WEBAUDIO @TODO API We load the whole URL and cut in the decodeAudioData temporary (waiting for server func)');
        var newBuffer = self.audioCtx.createBuffer(buffer.numberOfChannels,endIndexInBuffer - startIndexInBuffer, buffer.sampleRate);

        //for (var channel=0; channel < buffer.numberOfChannels; channel++) {
        //    newBuffer.getChannelData(channel).set(buffer.getChannelData(channel), startIndexInBuffer);
        //}

        newBuffer.copyFromChannel(buffer.getChannelData(0),0,startIndexInBuffer);

        self.audioBuffer = newBuffer;//buffer;
        (_.bind(self.testPlay,self))();
      },
        function(e){
          console.error("Error with decoding audio data" + e.err);
      });
    },*/

    testPlay:function() {
      if (!this.audioBuffer)
        return;

      if (this.updateInterval) {
        clearInterval(this.updateInterval);
        this.updateInterval=undefined;
      }

      var isLooping=A._i.getOnCfg('playerIsLooping');//false; //TODO : DYNAMIZE

      this.source = this.audioCtx.createBufferSource();
      this.source.buffer = this.audioBuffer;
      this.source.connect(this.audioCtx.destination);
      this.source.loop = isLooping;
      if (isLooping) {
        this.source.loopStart = this.timeStartInSound/1000;
        this.source.loopEnd = this.timeEndInSound/1000;
        this.source.start(this.audioCtx.currentTime,this.timeStartInSound/1000);
      }
      else {
        this.source.start(this.audioCtx.currentTime,this.timeStartInSound/1000, (this.timeEndInSound - this.timeStartInSound)/1000);
      }

      //this.source.start(this.audioCtx.currentTime,this.timeStartInSound/1000);
      this.startTimeAudioContext = this.audioCtx.currentTime;
      this.updateInterval = setInterval(_.bind(this.testTimeUpdate,this),30);
    },


   

    destroySound:function() {
      
    },

    //////////////////////////////////////////////////////////////////////////////
    //Audio loading 

    loadGlobalFile:function(url) {
     
    },



    //////////////////////////////////////////////////////////////////////////////
    //Audio loading -- specific segment

    loadSpecificFile:function(url) {

    },


    //////////////////////////////////////////////////////////////////////////////
    //Audio play/pause

    playAudio:function() {
      

    },

    stopAudio:function() {
      if (this.source)
        this.source.stop();

      if (this.updateInterval) {
        clearInterval(this.updateInterval);
        this.updateInterval=undefined;
      }
    },
  
    pauseAudio:function() {
      
    },

   

    //////////////////////////////////////////////////////////////////////////////
    //Audio time sync
    //on percent of audio!!!
    setCurrentTime:function(fracTime) {
      /*var timePercent = fracTime*100;
      if (this.sound)
        this.sound.setPercent(timePercent);*/
    },


    testTimeUpdate:function() {
      var timeNow =this.audioCtx.currentTime;
      var origin = this.startTimeAudioContext;
      var delta = (timeNow - origin)*1000;

      var isLooping=A._i.getOnCfg('playerIsLooping');
      if (isLooping) {
        delta = delta % (this.timeEndInSound - this.timeStartInSound);
      }

      var timeInPlay = this.timeStartInSound+delta;
      

      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      var percent = timeInPlay / trackDuration;
      //console.log('playing web-audio : '+timeInPlay+" -> "+percent);
      A._v.trigCfg('audio.newAudioTime','',percent);

      if ((!isLooping) && timeInPlay>=this.timeEndInSound-50) {
        clearInterval(this.updateInterval);
        this.updateInterval=undefined;
      }

    },

  


  });
});
