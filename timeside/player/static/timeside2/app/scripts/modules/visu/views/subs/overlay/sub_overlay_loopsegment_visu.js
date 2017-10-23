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
      'click [data-layout="click_catcher"]'    : 'onClickCatcher',
      'click [data-layout="reset"]'            : 'onClickReset',
      'click [data-layout="zoom"]'             : 'onClickZoom'
    },

    onClickZoom:function(ev) {
        var zoomIsMore = ev.currentTarget.dataset.zoom =="more";
        A._v.trigCfg('ui_project.zoom','',zoomIsMore ? 0.666 : 1.5 );
    },

    onClickReset:function(ev) {
      this.triangleLeftTime =0;
      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      this.triangleRightTime = trackDuration;

      A._i.setOnCfg('currentLoopSegment',[this.triangleLeftTime,this.triangleRightTime]);
      A._v.trigCfg('ui_project.segmentLoopUpdate');

      return this.onNavigatorNewWindow();

    },

    onClickCatcher:function(ev) {
      var _timeForClick = this.getTimeFromX(ev.pageX);
      console.log('Click : '+ev.pageX+" -> "+_timeForClick);

      


      var distances = [Math.abs(_timeForClick - this.triangleLeftTime), Math.abs(_timeForClick - this.triangleRightTime)];
      var targetIsLeft = distances[0] < distances[1]; //le plus proche

      //if crl key : targetisLeft = true
      if (ev.ctrlKey)
        targetIsLeft = true;
      if (ev.altKey)
        targetIsLeft=false;  

      var newTime = this.getTimeFromX(ev.pageX);

      if (targetIsLeft && newTime < this.triangleRightTime)
        this.triangleLeftTime  = this.getTimeFromX(ev.pageX);
      
      if ((!targetIsLeft) && newTime > this.triangleLeftTime)
        this.triangleRightTime  = this.getTimeFromX(ev.pageX);



      A._i.setOnCfg('currentLoopSegment',[this.triangleLeftTime,this.triangleRightTime]);
      A._v.trigCfg('ui_project.segmentLoopUpdate');

      return this.onNavigatorNewWindow();

      /*var target = targetIsLeft ? this.triangleLeft : this.triangleRight;

      target.attr("transform", function(d, i) {
          var translateX = ev.pageX;
          return "translate(" + translateX + ",0)";
        })*/

     
    },

    /**
        Programmatic update of selected segment
    **/
    setSegment:function(data) {
        this.triangleLeftTime = data.start;
        this.triangleRightTime = data.end;

        A._i.setOnCfg('currentLoopSegment',[this.triangleLeftTime,this.triangleRightTime]);
        A._v.trigCfg('ui_project.segmentLoopUpdate');

        return this.onNavigatorNewWindow();
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
        arrow.attr("transform", function() {return "translate("+trueX+",8)";});
      };
      positionArrow(this.triangleLeft,X0);
      positionArrow(this.triangleRight,X1);


      this.loopSegmentRectangle.attr('x',X0).attr('width',(X1-X0));
    },


    onResize:function() {
      this.width = this.$el.width();
      this.height = $('.tracks').height();

      this.node.attr('height',this.height);
      this.triangleLeft.selectAll('rect').attr('height',this.height);
      this.triangleRight.selectAll('rect').attr('height',this.height);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);
      A._v.onCfg('ui_project.tracksHeightChanged','',this.onResize,this);
      A._v.onCfg('ui_project.setSegment','',this.setSegment,this);
    },

    onRender:function() {
       
    },

    onDomRefresh:function() {
      if (this.initDone)
        return;

      this.width = this.$el.width();
      this.height = $('.other-tracks').height();

      console.log('coucou');

      var self=this;
      this.node = d3.select(this.$el.find('[data-layout="svg_container"]')[0]).append("svg")
        .attr("class","chart")
        .attr("width", self.$el.width())
        .attr("height", self.$el.height());


      //INIT LEFT TRIANGLE
      var triangleLeftPoints = this.generateTriangleLeft(15,true);//'10 0, 15 5, 10 10, 10 0';
      this.triangleLeft = this.node.append('g').attr("class", "time-arrow");
      this.triangleLeft.append('polygon').attr('points',triangleLeftPoints)
      this.triangleLeft.append('rect').attr('width',1).attr('height',this.height)
        .attr('transform','translate(0,15)');
      this.triangleLeftTime = this.getTimeFromX(0);

      //INIT RIGHT TRIANGLE
      var triangleRightPoints = this.generateTriangleLeft(15,false);//'10 0, 15 5, 10 10, 10 0';
      this.triangleRight = this.node.append('g').attr("class", "time-arrow");
      this.triangleRight.append('polygon').attr('points',triangleRightPoints)
      this.triangleRight.append('rect').attr('width',1).attr('height',this.height)
        .attr('transform','translate(-1,15)');
      this.triangleRight.attr("transform","translate(0,8)");

      this.triangleRightTime = this.getTimeFromX(0);

      //INIT SMALL RECT BETWEEN TRIANGLES
      this.loopSegmentRectangle = this.node.insert("rect",":first-child")
        .attr('class',"loop-segment")
        .attr('x',0).attr('y',8)
        .attr('width',0).attr('height',16)
        .attr('opacity',0.6);

      this.initDone=true;
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //generate triange
    generateTriangleLeft(width,isLeft) {
      var positionsLeft = [ [0,0], [Math.round(width/2),Math.round(width/2)], [0,Math.round(width)] ];
      var positionsRight = [ [0,0], [-Math.round(width/2),Math.round(width)/2], [0,Math.round(width)] ];

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
      A._v.offCfg('ui_project.tracksHeightChanged','',this.onResize,this);
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
