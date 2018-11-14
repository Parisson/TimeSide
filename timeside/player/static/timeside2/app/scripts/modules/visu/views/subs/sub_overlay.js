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

      Handles a red line for play performance


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

    getTimeFromX:function(x) {
      var time0 =  A._i.getOnCfg('trackInfoController').currentStartTime;
      var time1 =  A._i.getOnCfg('trackInfoController').currentEndTime;
      var width = this.width;


      return time0 + (x/width) * (time1 - time0)
    },

    getXFromTime:function(time) {
      var time0 =  A._i.getOnCfg('trackInfoController').currentStartTime;
      var time1 =  A._i.getOnCfg('trackInfoController').currentEndTime;
      var width = this.width;

      return width * (time-time0)/(time1-time0);
    },


    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('audio.newAudioTime','',this.onNewTime,this);
    },

    onRender:function() {
       if (!this.loopSegmentView) {
          this.loopSegmentView = new LoopSegmentVizualizer();
          this.ui.containerLoopSegment.empty().append(this.loopSegmentView.render().$el);
       }
    },

    onDomRefresh:function() {
      this.loopSegmentView.onDomRefresh();

      if (this.initDone)
        return;

      //creating play cursor

      this.width = this.$el.width();
      this.height = $(document).height();

      var self=this;
      this.node = d3.select(this.$el.find('[data-layout="playcursor_svg_container"]')[0]).append("svg")
        .attr("class","chart")
        .attr('fill','red')
        .attr("width", self.width)
        .attr("height", self.height);

      this.playCursor = this.node.append('g').attr("class", "play-cursor");
      this.playCursor.append('rect').attr('width',1).attr('height',this.height)
        .attr('transform','translate(0,15)');
      this.playCursorTime = this.getTimeFromX(0);
    },

    onResize:function() {
      this.width = this.$el.width();
      this.height = $(document).height();

      this.node.attr('height',this.height);
      this.playCursor.selectAll('rect').attr('height',this.height);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    onNewTime:function(fraction,valueSec) {

      this.playCursorTime = valueSec*1000;
      var X = this.getXFromTime(this.playCursorTime);

      var visible = X >0 && X < this.width;
      this.playCursor.attr('opacity',visible ? 1 : 0);
      var trueX = visible ? X : 0;

      this.playCursor.attr("transform", function() {return "translate("+trueX+",8)";});

    },


    ////////////////////////////////////////////////////////////////////////////////////

    onDestroy: function () {     
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
