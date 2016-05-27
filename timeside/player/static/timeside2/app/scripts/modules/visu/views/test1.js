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

    template: templates['visu/test1'],
    className: 'visu-test1',

    ui: {
      'btnLaunchTest' : 'button[data-layout="test"]',
      'btnRandom' : 'button[data-layout="update"]',
      'btnTestAudio' : 'button[data-layout="audio"]',

      'containerTrackNavigator' : '.navigation-track',
      'containerOtherTracks' : '.other-tracks'
    },
    events: {
      'click @ui.btnLaunchTest' : 'onLaunchTest',
      'click @ui.btnTestAudio' : 'onTestAudio'
    },

     ////////////////////////////////////////////////////////////////////////////////////
    //Ouais
    onTestAudio:function() {
      A.vent.trigger('audio:loadGlobalFile','/data/audio.mp3');
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    onLaunchTest:function() {
      this.trackNavigatorView.startLoading(800,200,_.bind(this.onNavigatorLoaded,this));
    },

    //when navigator is ready
    onNavigatorLoaded:function() {
     
      this.trackWaveformView_1.init();
      this.trackWaveformView_2.init();
      this.trackCanvasView.init();

    },
    
    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      window.home = this;

      A._i.setOnCfg('useFakeData',true);

      A._v.onCfg('fakeserver.getdata','ok',this.onDataReceived,this);
    },

    onRender:function() {
       if (! this.trackNavigatorView) {
          this.trackNavigatorView = new TrackNavigatorView();
          this.ui.containerTrackNavigator.empty().append(this.trackNavigatorView.render().$el);
       }



       if (! this.trackWaveformView_1) {
          this.trackWaveformView_1 = new TrackWaveformView();
          this.ui.containerOtherTracks.empty().append(this.trackWaveformView_1.render().$el);
          this.trackWaveformView_1.defineTrack({type : "waveform", width : 800, height : 200});
       }

       if (! this.trackWaveformView_2) {
          this.trackWaveformView_2 = new TrackWaveformView();
          this.ui.containerOtherTracks.append(this.trackWaveformView_2.render().$el);
          this.trackWaveformView_2.defineTrack({type : "test3", width : 800, height : 200});
       }

       if (! this.trackCanvasView) {
          this.trackCanvasView = new TrackCanvasView();
          this.ui.containerOtherTracks.append(this.trackCanvasView.render().$el);
          this.trackCanvasView.defineTrack({type : "testcanvas", width : 800, height : 200});
       }
    
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
