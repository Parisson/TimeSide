define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  /**
    Ruler track
      Simple track for displaying a ruler following the navigator actions
  **/
  return BaseQeopaView.extend({

    template: templates['visu/sub_track_ruler'],
    className: 'ruler-track',

    ui: {
     
    },
    events: {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////


    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    
    onNavigatorNewWindow:function() {
      var time0 =  A._i.getOnCfg('trackInfoController').currentStartTime;
      var time1 =  A._i.getOnCfg('trackInfoController').currentEndTime;
      this.xScale.domain([time0,time1]);
      this.axis.scale(this.xScale);
      this.d3chart.call(this.axis);

    },
    
    ////////////////////////////////////////////////////////////////////////////////////
    //Generate graph
    
    create:function(width,height) { 
      this.width = width;this.height=height;
      this.createBase();
      this.createAxis();
    },

   
    //////////////////////////////////
    // Render methods

    //1
    //creates the chart, kept as this.d3chart
    createBase:function() {
      var height = this.height;
      var width = this.width;

      var node = d3.select(this.$el.find('.container_track_ruler > .svg')[0]).append("svg")
        .attr("class","chart")
        .attr("width", width)
        .attr("height", height);


      var time0=0, time1 = this.item.get('audio_duration')*1000;  
      var x = d3.time.scale().domain([time0,time1]).range([0,width]);
      this.xScale = x;

      var chart = node.attr("width", width).attr("height", height);
      this.d3chart = chart;

    },

    //2
    //Create the axis
    createAxis:function() {
      var height = this.height, width = this.width, data = this.data, chart = this.d3chart,
        max_val=this.max_val;

      var xScale = this.xScale;
      
      var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('top')
          .ticks(6)
          .tickFormat(function(arg) {
            return A.telem.formatTimeMs(arg.getTime());
          });

      this.axis = xAxis;

      this.d3chart = chart.append('g')
          .attr('class', 'x axis')
          .attr('transform', 'translate(0,' + (height) + ')');

      this.d3chart.call(xAxis);

      this.xScale = xScale;
    },

    




    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {

      this.item = A._i.getOnCfg('currentItem');
      A._v.onCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);
    },

    onRender:function() {
       
    },

    onDestroy: function () {     
      A._v.offCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
