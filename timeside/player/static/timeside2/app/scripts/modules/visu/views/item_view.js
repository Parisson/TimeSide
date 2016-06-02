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
      
      'btnAction' : '[data-action]',
      'containerTrackNavigator' : '.navigation-track',
      'containerOtherTracks' : '.other-tracks'
    },
    events: {
      'click @ui.btnAction' : 'onClickAction'
    },

     ////////////////////////////////////////////////////////////////////////////////////
    //Action manager
    onClickAction:function(ev) {
      var action = ev.currentTarget.dataset.action;
      var mapAction = {"start" : this.onStartLoading, "add" : this.onAddTrackWaveform, "play" : this.onPlayAudio};

      if (mapAction[action])
        (_.bind(mapAction[action],this))();
    },

    onStartLoading:function() {
      this.$el.find('[data-action="start"]').attr("disabled",true).text('loading');
      alert('start loading');

      A.vent.trigger('audio:loadGlobalFile',this.item.get('audio_url').mp3);

      this.trackNavigatorView.isTrueDataServer = true;

      this.trackNavigatorView.startLoading(800,200,_.bind(this.onNavigatorLoaded,this));
    },


    //when navigator is ready
    onNavigatorLoaded:function() {
     this.navigatorReady=true;

     A._i.getOnCfg('dataLoader').isTrueDataServer=true; //IMPORTANT (pas à sa place)

     this.$el.find('[data-action]').attr("disabled",false);
     /* this.trackWaveformView_1.init();
      this.trackWaveformView_2.init();
      this.trackCanvasView.init();*/

    },

    onPlayAudio:function() {
      A.vent.trigger('audio:play',this.item.get('audio_url').mp3);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Add a track
    onAddTrackWaveform:function() {
      if (!this.navigatorReady)
        return;

      this.trackWaveformView_1 = new TrackWaveformView();
      this.ui.containerOtherTracks.empty().append(this.trackWaveformView_1.render().$el);
      this.trackWaveformView_1.defineTrack({type : "waveform", width : 800, height : 200});

      this.trackWaveformView_1.init();
    },
    
    

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.item = A._i.getOnCfg('currentItem');
      this.navigatorReady=false;



      A._i.getOnCfg('trackInfoController').setDuration(this.item.get('audio_duration')*1000);

      A._i.setOnCfg('useFakeData',false);
    },

    onRender:function() {
       if (! this.trackNavigatorView) {
          this.trackNavigatorView = new TrackNavigatorView();
          this.ui.containerTrackNavigator.empty().append(this.trackNavigatorView.render().$el);
       }
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
