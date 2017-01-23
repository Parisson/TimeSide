define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3',
  './overlay/sub_overlay_loopsegment_visu'
],

function (Marionette,A,BaseQeopaView,d3,LoopSegmentVizualizer) {
  'use strict';

  /**
    MAIN OVERLAY PANEL ON OTHER TRACKS
      Can accumulate annotations & stuff like that easily
      
      The main container is pointer-events : none; children can override this css property to become mouse-interactive

      Component will be composed of : 
        the loop-segment vizualizer/controller : 
          upper zone is click responsive
          the whole zone is used to draw the two bars.

        a lower bigger zone (fill) which will contain the annotations

  **/
  return BaseQeopaView.extend({

    template: templates['visu/sub_overlay'],
    className: 'overlay',

    ui: {
     containerLoopSegment : '[data-layout="loopsegment_container"]'
    },
    events: {
      
    },


    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {

    },

    onRender:function() {
       if (!this.loopSegmentView) {
          this.loopSegmentView = new LoopSegmentVizualizer();
          this.ui.containerLoopSegment.empty().append(this.loopSegmentView.render().$el);
       }
    },

    onDomRefresh:function() {
      this.loopSegmentView.onDomRefresh();
    },

    onDestroy: function () {     
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
