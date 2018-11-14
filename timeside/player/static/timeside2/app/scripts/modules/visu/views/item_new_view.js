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
  './subs/track_waiting',

  './subs/sub_overlay',


  '#audio/views/player'
],

function (Marionette,A,BaseQeopaView,d3,TrackNavigatorView,TrackWaveformView,TrackWaveformViewV2,TrackCanvasView
  ,TrackRulerView,TrackAnnotationsView,TrackWaiting,
  OverlayView,AudioPlayerView) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['visu/item_new_view'],
    className: 'item_view',

    ui: {
      
      'btnAction' : '[data-action]',
      'containerTrackNavigator' : '.navigation-track',
      'containerRulerView' : '[data-layout="ruler_container"]',
      'containerOtherTracks' : '.other-tracks',
      'containerPlayer' : '[data-layout="player_container"]',
      'containerOverlay' : '[data-layout="overlay-container"]'
    },
    events: {
      'click @ui.btnAction' : 'onClickAction',
      'mousemove @ui.containerOtherTracks' : 'onMouseOverContainerTracks',
      'mousedown @ui.containerOtherTracks' : 'onMouseDownContainerTracks',
      'mouseup @ui.containerOtherTracks' : 'onMouseUpContainerTracks',
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
        "add_annot" : this.askNewAnnotationTrack,"add_new_waveform" : this.onAddTrackWaveformV2, "add_anal" : this.onAddNewAnalysis};

      if (mapAction[action])
        (_.bind(mapAction[action],this))();
    },

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Loading

    //Start loading item
    onStartLoading:function() {
      this.$el.find('[data-action="start"]').attr("disabled",true).text('loading');

      A.vent.trigger('audio:loadGlobalFile',this.item.get('audio_url').mp3);

      this.trackNavigatorView.isTrueDataServer = true;

      this.trackNavigatorView.startLoading(this.size.width, this.size.navHeight,_.bind(this.onNavigatorLoaded,this));
    },

    //when navigator is ready
    onNavigatorLoaded:function() {
     this.navigatorReady=true;
     //this.onDomRefresh();

      A._i.getOnCfg('dataLoader').isTrueDataServer=true; //IMPORTANT (pas à sa place)
      A._i.getOnCfg('trackInfoController').currentEndTime = A._i.getOnCfg('trackInfoController').getDuration();

      //tmp
      this.$el.find('[data-action]').attr("disabled",false);

     //let's instanciate ruler
      if (! this.rulerView) {
        this.rulerView = new TrackRulerView();
        this.ui.containerRulerView.empty().append(this.rulerView.render().$el);
        this.rulerView.create(this.size.width, this.size.rulerHeight);
      }

      var item = A._i.getOnCfg('currentItem');
      if (item && item.get('annotationTracksObjects')) {
        var self=this;
        item.get('annotationTracksObjects').each(function(annotationTrack) {
          self.addTrack(new TrackAnnotationsView(),"annotation",annotationTrack);
        });
      }

      this.onAddTrackWaveformV2(); //new : asked by blair


      if (item && item.get('analysisTracksObjects')) {
        var self = this;
        var tracksToCreate = item.get('analysisTracksObjects').models,
          indexTrack = 0;

        var addNewTrack = function() {
          if (indexTrack==tracksToCreate.length) {
            A._v.trigCfg('ui_project.setSegment','',{start : 0,end : A.injector.get('currentItem').get('audio_duration')*1000});
            return console.log('All tracks loaded!');
          }
          var track = tracksToCreate[indexTrack];
          var uniqueId = "FROMSTART_"+indexTrack;

          //1 event for view
          A._v.trigCfg('analysis.asked','',uniqueId);

          setTimeout(function() {
            var resultModel = track;
            resultModel.set('uniqueIDForView',uniqueId),
            A._v.trigCfg('analysis.result','',resultModel); //will update view

            setTimeout(function() {
              indexTrack++;
              return addNewTrack();
            },200);
          },300);
        };

        return addNewTrack();

        /*item.get('analysisTracksObjects').each(function(analysisTrack) {
          console.log('todo : add analysisTrack');
        });*/
      }
      

    },

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Actions on track

    onPlayAudio:function() {
      //no more : triggered by player
      //A.vent.trigger('audio:play',this.item.get('audio_url').mp3);
    },

     //ask for a new analysis
    onAddNewAnalysis:function() {
      var allAnalysis =  _.map(A._i.getOnCfg('allAnalysis'),function(obj) {
        return obj.toJSON()
      }), self=this;
      A._v.trigCfg('ui.popup.show',"",'selectItem', {
        title : 'Nouvelle analyse',
        items : allAnalysis,
        callbackSelect:function(idAnalsysis) {
          var analysis = _.find(allAnalysis,function(_anal) {return _anal.uuid===idAnalsysis});
          
          A._v.trigCfg('analysis.ask','',analysis);
        }
      });


    },

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Delete a track

    /**
        Called by param_simple or parameter item. argument is the trackView.
        Called for visual tracks
    **/
    onDeleteTrackView:function(trackView) {
      if (!trackView)
        return;

      var trackModel = trackView.resultAnalysis;
      var self=this;
      A._i.getOnCfg('analysisController').deleteAnalysisTrack(trackModel,function() {
        self.tracks = self.tracks.filter(function(_tv) {
          return _tv!==trackView;
        });

        trackView.remove(); //@TODO : memory checks
        trackView.destroy();
      });


      
    },

    onDeleteAnnotationTrackView:function(trackModel) {
      var trackViewForModel = _.find(this.tracks,function(_trackView) {
        return _trackView.resultAnalysis===trackModel;
      });
      var self=this;

      A._i.getOnCfg('annotationControlller').deleteTrackAnnotation(trackModel,function() {
        
        if (trackViewForModel) {
          self.tracks = self.tracks.filter(function(_tv) {
          return _tv!==trackViewForModel;
        });

        trackViewForModel.remove(); //@TODO : memory checks
        trackViewForModel.destroy();
        }
      })
    },


    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Resize a track
    onMouseOverContainerTracks:function(ev) {
      /*console.log('overing : '+ev.pageX+":"+ev.pageY);*/

      if (this.isResizing) {
        //make true resize here
        var deltaY = ev.pageY - this.YMouseDownForResize;
        var newHeight = this.initialHeightComponent + deltaY;
        if (this.trackSelected && this.trackSelected.changeHeight)
          this.trackSelected.changeHeight(newHeight);
        return;
      }


      //console.log('=============');  
      var heightZoneCanResize = 30;
      var offsetContainerOtherTracks = this.ui.containerOtherTracks.offset().top;
      var trackSelected;
      var trueYInContainer = ev.pageY - offsetContainerOtherTracks;
      var cummulatedHeight = 0;
      _.each(this.tracks,function(_tv,index) {
        var boundInf = /*_tv.$el.position().top*/ cummulatedHeight+ _tv.$el.height() - heightZoneCanResize;
        var boundSup =  /*_tv.$el.position().top*/ cummulatedHeight+ _tv.$el.height(); 
        /*console.log(index+'Testing : '+trueYInContainer+" || "+_tv.$el.position().top+" ? "+_tv.$el.height()+"\n"
              +"  >? "+(boundInf)+" <? "+( boundSup) );*/

        if (trueYInContainer>boundInf && (trueYInContainer <  boundSup)) {
          trackSelected = _tv;
        }
        cummulatedHeight+=_tv.$el.height();

      },this);

      if (trackSelected) {
        this.ui.containerOtherTracks.css('cursor','row-resize');
      }
      else {
        this.ui.containerOtherTracks.css('cursor','default');
      }

      this.trackSelected = trackSelected;
    },


    onMouseDownContainerTracks:function(ev) {
      if (this.trackSelected) {
        this.YMouseDownForResize = ev.pageY;
        this.initialHeightComponent = this.trackSelected.$el.height();
        this.isResizing=true;
      }
    },

    onMouseUpContainerTracks:function(ev) { 
      if (this.trackSelected) {
        this.trackSelected=undefined;
        this.isResizing=false;
      }

    },


    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Add a track --- Model call


    //--------------------------------ANALYSIS -- TRACK

    //called by analysis controller when it starts loading a track
    //adds a temp track
    onAnalysisAsked:function(uniqueId) {
      if (! this.waitingTracks)
        this.waitingTracks = [];
      var trackView = new TrackWaiting();
      trackView.setUniqueId(uniqueId);
      this.waitingTracks.push(trackView);
      this.ui.containerOtherTracks.append(trackView.render().$el);
      A._v.trigCfg('ui_project.tracksHeightChanged');
    },


    onResultAnalysis:function(resultAnalysis) {
      //find waiting view
      var waiting = _.find(this.waitingTracks,function(_wait) {return _wait.getUniqueId() === resultAnalysis.get('uniqueIDForView')});
      if (!waiting)
        return console.error('no waiting track found for : '+resultAnalysis);

      this.waitingTracks = _.without(this.waitingTracks,waiting);
      waiting.$el.remove();


      //pour l'instant, on part du principe qu'on est sur du canvas toujours pour ces retours
      return this.addTrack(new TrackCanvasView(),"canvas",resultAnalysis);
    },

    //--------------------------------ANNOTATION -- TRACK
    askNewAnnotationTrack:function() {
      var self=this;
      A._i.getOnCfg('annotationControlller').createTrackAnnotation(function(model) {
        return self.addTrack(new TrackAnnotationsView(),"annotation",model);
      }); 
    },

    ////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////
    //Add a track

    addTrack:function(trackView,type,resultAnalysis) {
      this.tracks.push(trackView);
      this.ui.containerOtherTracks.append(trackView.render().$el);
      trackView.defineTrack({type : type, width : this.size.width, height : this.size.defaultHeight, resultAnalysis : resultAnalysis});
      trackView.init();
      A._v.trigCfg('ui_project.tracksHeightChanged');
    },

    //below :  --- DEBUG VERSIONS!!!
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
    
    /*onAddTrackAnnotations:function(model) {
      if (!this.navigatorReady)
        return;


      return this.addTrack(new TrackAnnotationsView(),"annotation");
    },
    */

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.item = A._i.getOnCfg('currentItem');
      this.navigatorReady=false;
      this.tracks = [];


      A._i.getOnCfg('trackInfoController').setDuration(this.item.get('audio_duration')*1000);
      A._v.onCfg('analysis.asked','',this.onAnalysisAsked,this);
      A._v.onCfg('analysis.result','',this.onResultAnalysis,this);
      A._v.onCfg('ui_project.deleteTrack','',this.onDeleteTrackView,this);
      A._v.onCfg('ui_project.deleteAnnotationTrack','',this.onDeleteAnnotationTrackView,this);
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
       if (! this.overlayView) {
        this.overlayView = new OverlayView();
        this.ui.containerOverlay.empty().append(this.overlayView.render().$el);
       }

       //loading start done in onDomRefresh!

       /*if (! this.hasStartedLoading) {
        this.hasStartedLoading=true;
        //this.onStartLoading();
       }*/
    },

   
       

    onDestroy: function () {      
      this.trackNavigatorView.destroy();
      this.audioPlayerView.destroy();
      if (this.rulerView)
        this.rulerView.destroy();
      this.overlayView.destroy();

       A._v.offCfg('analysis.asked','',this.onAnalysisAsked,this);
       A._v.offCfg('analysis.result','',this.onResultAnalysis,this);

      _.each(this.tracks,function(t) {
        t.destroy();
      });
    },

    onDomRefresh:function() {
      this.overlayView.onDomRefresh();
      //once it is rendered, set the desired tracks width/height
      this.updateSize();

      if (! this.hasStartedLoading) {
        this.hasStartedLoading=true;
        this.onStartLoading();
      }

    },

    serializeData: function () {
      

      return {
        item : this.item.toJSON()
      }
    },


    
    
   
  });
});
