define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  /**
    Overlay loop-segment vizualizer

      has a click Catcher

        @TODO STILL

            -> Avoir l'info pour chaque curseur :  son time

  **/
  return BaseQeopaView.extend({

    template: templates['visu/sub_overlay_loopsegment_visu'],
    className: 'overlay_loopsegment_visu',

    ui: {
    },
    events: {
      'click [data-layout="click_catcher"]' : 'onClickCatcher'
    },

    onClickCatcher:function(ev) {
      var _timeForClick = this.getTimeFromX(ev.pageX);
      console.log('Click : '+ev.pageX+" -> "+_timeForClick);


      var distances = [Math.abs(_timeForClick - this.triangleLeftTime), Math.abs(_timeForClick - this.triangleRightTime)];
      var targetIsLeft = distances[0] < distances[1]; //le plus proche

      if (targetIsLeft)
        this.triangleLeftTime  = this.getTimeFromX(ev.pageX);
      else
        this.triangleRightTime  = this.getTimeFromX(ev.pageX);

      return this.onNavigatorNewWindow();

      var target = targetIsLeft ? this.triangleLeft : this.triangleRight;

      target.attr("transform", function(d, i) {
          var translateX = ev.pageX;
          return "translate(" + translateX + ",0)";
        })
    },

    redrawLoopSegment:function() {

    },

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

    onNavigatorNewWindow:function() {
      var time0 =  A._i.getOnCfg('trackInfoController').currentStartTime;
      var time1 =  A._i.getOnCfg('trackInfoController').currentEndTime;

      var X0 = this.getXFromTime(this.triangleLeftTime),
        X1 = this.getXFromTime(this.triangleRightTime),
        self = this;

      var positionArrow = function(arrow,X)  {
        var visible = X >0 && X < self.width;
        arrow.attr('opacity',visible ? 1 : 0);

        var trueX = visible ? X : 0;
        arrow.attr("transform", function() {return "translate("+trueX+",0)";});
      };
      positionArrow(this.triangleLeft,X0);
      positionArrow(this.triangleRight,X1);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);
    },

    onRender:function() {
       
    },

    onDomRefresh:function() {
      if (this.initDone)
        return;

      this.width = this.$el.width();

      console.log('coucou');

      var self=this;
      this.node = d3.select(this.$el.find('[data-layout="svg_container"]')[0]).append("svg")
        .attr("class","chart")
        .attr("width", self.$el.width())
        .attr("height", self.$el.height());

      var triangleLeftPoints = this.generateTriangleLeft(15,true);//'10 0, 15 5, 10 10, 10 0';
      this.triangleLeft = this.node.append('polyline').attr('points',triangleLeftPoints).style('stroke','black');
      this.triangleLeftTime = this.getTimeFromX(0);

      var triangleRightPoints = this.generateTriangleLeft(15,false);//'10 0, 15 5, 10 10, 10 0';
      this.triangleRight = this.node.append('polyline').attr('points',triangleRightPoints).style('stroke','black')
        .attr("transform","translate(100,0)");
      this.triangleRightTime = this.getTimeFromX(100);


      this.initDone=true;
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //generate triange
    generateTriangleLeft(width,isLeft) {
      var positionsLeft = [ [0,0], [Math.round(width/2),Math.round(width/2)], [0,Math.round(width)] ];
      var positionsRight = [ [Math.round(width/2),0], [Math.round(width/2),Math.round(width)], [0,Math.round(width/2)] ];

      var positions = isLeft ? positionsLeft : positionsRight;

      var result='';
      _.each(positions,function(pos) {
        result=result+pos[0]+" "+pos[1]+","
      });
      result=result+positions[0][0]+" "+positions[0][1];
      return result;

    },


    ////////////////////////////////////////////////////////////////////////////////////

    onDestroy: function () { 
      A._v.offCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);    
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
