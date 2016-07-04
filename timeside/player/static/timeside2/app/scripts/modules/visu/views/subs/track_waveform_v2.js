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


    createGraphicBase:function() {
      TrackWaveformView.prototype.createGraphicBase.call(this);
      var self=this;
      this.d3area = d3.svg.area()
        .x(function(d) { 
          
          return self.xScale(d.time); 
        })
        .y0(function(d) {return self.yScale(d.min); })
        .y1(function(d) { return self.yScale(d.max); });

      this.d3AreaSuite = this.d3chart.append('path').datum([]).attr("class","area").attr('d',this.d3area );
    },

    setVisibleData:function(data) {
      this.hadFirstData = true;
      this.lastReceivedData = data;

      var showDebug=false;//hop

      A.log.log('track_waveform2','setVisibleData----------------- on '+data.length);

      this.MAX_VALUE = A._i.getOnCfg('trackInfoController').getMaxValue();

      var height = this.height;
      var width = this.width;
      var barHeight = this.height-this.size.axisHeight;
      var axisHeight = this.size.axisHeight;

      //update scales
      this.yScale.range([barHeight, -barHeight]);
      var max_val = this.MAX_VALUE;
      this.yScale.domain([-max_val, max_val]);

      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      //this.xScale = d3.scale.linear().domain([0, 1024]); //TMP
      A.log.log('track_waveform_V2:setVisibleData',' X scale will go from '+data[0].time+'->'+data[data.length-1].time);
      this.xScale.domain([data[0].time,data[data.length-1].time]).range([0,width]);


      this.d3AreaSuite = this.d3chart.selectAll('path').datum(data).attr("class","area").attr('d',this.d3area );
      return;

      
    },

    /////////////////////////////////////////////////////////////////////////////////////
    //Height change
    changeHeight:function(newHeight) {
      this.height = newHeight;
      this.node.attr('height',newHeight);
      this.d3chart.attr('height',newHeight);
      var barHeight = this.height-this.size.axisHeight;
      var axisHeight = this.size.axisHeight;

      this.yScale.range([barHeight, -barHeight]);
      this.d3AreaSuite = this.d3chart.selectAll('path').datum(this.lastReceivedData).attr("class","area").attr('d',this.d3area );
      
    },

    
    
   
  });
});
