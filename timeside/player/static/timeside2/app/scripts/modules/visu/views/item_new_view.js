define([
   'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3',
  './subs/track_navigator',
  './subs/track_waveform',
  './subs/track_waveform_v2',
  './subs/track_canvas',
  './subs/track_ruler',
  './subs/track_annotations',


  '#audio/views/player'
],

function (Marionette,A,BaseQeopaView,d3,TrackNavigatorView,TrackWaveformView,TrackWaveformViewV2,TrackCanvasView,TrackRulerView,TrackAnnotationsView,
  AudioPlayerView) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['visu/item_new_view'],
    className: 'item_view',

    ui: {
      
      'btnAction' : '[data-action]',
      'containerTrackNavigator' : '.navigation-track',
      'containerRulerView' : '[data-layout="ruler_container"]',
      'containerOtherTracks' : '.other-tracks',


      'containerPlayer' : '[data-layout="player_container"]'
    },
    events: {
      'click @ui.btnAction' : 'onClickAction'
    },
    ////////////////////////////////////////////////////////////////////////////////////
    //SIZES
    updateSize : function() {
      this.size = {
        defaultHeight : 200,  //normal track height
        navHeight     : 60,   // navigation track height
        rulerHeight   : 30,    //height of the ruler above tracks
        width         : this.$el.width()  //all tracks width
      };
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Action manager
    onClickAction:function(ev) {
      var action = ev.currentTarget.dataset.action;
      var mapAction = {"start" : this.onStartLoading, "add" : this.onAddTrackWaveform, "play" : this.onPlayAudio,
        "add_annot" : this.onAddTrackAnnotations,"add_new_waveform" : this.onAddTrackWaveformV2};

      if (mapAction[action])
        (_.bind(mapAction[action],this))();
    },

    onStartLoading:function() {
      this.$el.find('[data-action="start"]').attr("disabled",true).text('loading');
      //alert('start loading');

      A.vent.trigger('audio:loadGlobalFile',this.item.get('audio_url').mp3);

      this.trackNavigatorView.isTrueDataServer = true;

      this.trackNavigatorView.startLoading(this.size.width, this.size.navHeight,_.bind(this.onNavigatorLoaded,this));
    },


    //when navigator is ready
    onNavigatorLoaded:function() {
     this.navigatorReady=true;

     A._i.getOnCfg('dataLoader').isTrueDataServer=true; //IMPORTANT (pas à sa place)

     //tmp
     this.$el.find('[data-action]').attr("disabled",false);

     //let's instanciate ruler
     if (! this.rulerView) {
        this.rulerView = new TrackRulerView();
        this.ui.containerRulerView.empty().append(this.rulerView.render().$el);
        this.rulerView.create(this.size.width, this.size.rulerHeight);
     }

     //@Todo : get container track ruler & instanciate TrackRulerView

    },

    onPlayAudio:function() {
      A.vent.trigger('audio:play',this.item.get('audio_url').mp3);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Add a track
    addTrack:function(trackView,type) {
      this.tracks.push(trackView);
      this.ui.containerOtherTracks.append(trackView.render().$el);
      trackView.defineTrack({type : type, width : this.size.width, height : this.size.defaultHeight});
      trackView.init();
    },

    onAddTrackWaveform:function() {
      if (!this.navigatorReady)
        return;
      return this.addTrack(new TrackWaveformView(),"waveform");
    },

    onAddTrackWaveformV2:function() {
      if (!this.navigatorReady)
        return;
      return this.addTrack(new TrackWaveformViewV2(),"waveform_v2");
    },
    
    onAddTrackAnnotations:function() {
      if (!this.navigatorReady)
        return;


      return this.addTrack(new TrackAnnotationsView(),"annotation");
    },
    

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.item = A._i.getOnCfg('currentItem');
      this.navigatorReady=false;
      this.tracks = [];


      A._i.getOnCfg('trackInfoController').setDuration(this.item.get('audio_duration')*1000);

      A._i.setOnCfg('useFakeData',false);
    },

    onRender:function() {
      
       if (! this.trackNavigatorView) {
          this.trackNavigatorView = new TrackNavigatorView();
          this.ui.containerTrackNavigator.empty().append(this.trackNavigatorView.render().$el);
       }
       if (! this.audioPlayerView) {
          this.audioPlayerView = new AudioPlayerView();
          this.ui.containerPlayer.empty().append(this.audioPlayerView.render().$el);
       }
    },
       

    onDestroy: function () {      
      this.trackNavigatorView.destroy();
      this.audioPlayerView.destroy();
      if (this.rulerView)
        this.rulerView.destroy();

      _.each(this.tracks,function(t) {
        t.destroy();
      });
    },

    onDomRefresh:function() {
      //once it is rendered, set the desired tracks width/height
      this.updateSize();

    },

    serializeData: function () {
      

      return {
        item : this.item.toJSON()
      }
    },


    
    
   
  });
});
