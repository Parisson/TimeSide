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
      console.log('Click : '+ev.pageX);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {

    },

    onRender:function() {
       
    },

    onDomRefresh:function() {
      if (this.initDone)
        return;
      var self=this;
      this.node = d3.select(this.$el.find('[data-layout="svg_container"]')[0]).append("svg")
        .attr("class","chart")
        .attr("width", self.$el.width())
        .attr("height", self.$el.height());

      var triangleLeftPoints = this.generateTriangleLeft(15,false);//'10 0, 15 5, 10 10, 10 0';
      this.triangleLeft = this.node.append('polyline').attr('points',triangleLeftPoints).style('stroke','blue');


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
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
