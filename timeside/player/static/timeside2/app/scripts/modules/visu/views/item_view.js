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
      var mapAction = {"start" : this.onStartLoading};

      if (mapAction[action])
        (_.bind(mapAction[action],this))();
    },

    onStartLoading:function() {
      this.$el.find('[data-action="start"]').attr("disabled",true).text('loading');
      alert('start loading');

      this.trackNavigatorView.isTrueDataServer = true;

      this.trackNavigatorView.startLoading(800,200,_.bind(this.onNavigatorLoaded,this));
    },


    //when navigator is ready
    onNavigatorLoaded:function() {
     
     /* this.trackWaveformView_1.init();
      this.trackWaveformView_2.init();
      this.trackCanvasView.init();*/

    },
    
    

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.item = A._i.getOnCfg('currentItem');
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
