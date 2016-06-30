define([
  'marionette',
  '#qt_core/controllers/all',
  './track_waveform',
  'd3'
],

/**
  Inherits from track_waveform, just implements new way of handling data
**/

function (Marionette,A,TrackWaveformView,d3) {
  'use strict';

  /**
    Ruler track
      Simple track for displaying a ruler following the navigator actions
  **/
  return TrackWaveformView.extend({

    setVisibleData:function(data) {
      this.hadFirstData = true;

      var showDebug=false;//hop

      A.log.log('track_waveform2','setVisibleData----------------- on '+data.length);

      this.MAX_VALUE = A._i.getOnCfg('trackInfoController').getMaxValue();

      var height = this.height;
      var width = this.width;
      var barHeight = this.height-this.size.axisHeight;
      var axisHeight = this.size.axisHeight;
      var bar_width = width / data.length;

      //update scales
      this.yScale = d3.scale.linear().range([barHeight, -barHeight]);
      var max_val = this.MAX_VALUE;
      this.yScale.domain([-max_val, max_val]);

      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      //this.xScale = d3.scale.linear().domain([0, 1024]); //TMP
      A.log.log('track_waveform:setVisibleData',' X scale will go from '+data[0].time+'->'+data[data.length-1].time);
      this.xScale = d3.time.scale().domain([data[0].time,data[data.length-1].time]).range([0,width]);

      //go
      var chart = this.d3chart;
      var x=this.xScale,y = this.yScale;

      var newdata =  chart.selectAll("g").data(data,function(d) {return d.time;});



      var self=this;
      //ENTER
      newdata.enter().append("g") // svg "group"
        .attr("transform", function(d, i) {
          var translateX = self.xScale(d.time);
          if (showDebug)
            console.log('     X : '+d.time+' --> '+translateX);
          return "translate(" + translateX /** bar_width*/ + ","+axisHeight+")";
        })
        .append("rect")
        .attr("y", function(d) {
          var yv = barHeight - Math.abs(y(d.value)/2) - barHeight/2 + 2;
          return yv/2;
        })
        .attr("height", function(d) {
          return Math.abs(y(d.value)/2); })
        .attr("width", bar_width );

      //STILL HERE
      chart.selectAll("g")/*.transition(0.75)*/.attr("transform", function(d, i) {
          var translateX = self.xScale(d.time);

          if (showDebug)
            console.log('     X2 : '+d.time+' --> '+translateX);
          return "translate(" + translateX /** bar_width*/ + ","+axisHeight+")";
        }).select('rect')
        .attr("y", function(d) {
          var yv = height - Math.abs(y(d.value)/4) - height/4 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d.value)/2); })
        .attr("width", bar_width );  

      newdata.exit().remove();
        
    }

    
    
   
  });
});
