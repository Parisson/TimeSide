define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3',
  '#visu/controllers/providers/waveform_dataprovider',
  '#behaviors/index',
  '../params/param_simple'
],

function (Marionette,A,BaseQeopaView,d3,WaveformDataProvider,behaviors,ParamSimpleView) {
  'use strict';

  /**
    Waveform track
      Méthodes à exposer : 
        init(typeData)
          va récupérer les global datas, générer et afficher

  **/
  return BaseQeopaView.extend({

    behaviors: function () {
      return {
        Parameter : {
          behaviorClass : behaviors.viewParameterTrack
        }
      };
    },

    /*parametersConfig : {
      getParameterView:function() {
        return new ParamSimpleView();
      }
    },*/

    template: templates['visu/sub_track_waveform'],
    className: 'track-waveform',

    ui: {
     
    },
    events: {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Definition //un peu con car sur les autres tracks, c'est au niveau du loader qu'on décide ça.
    isTrueDataServer : false,

    ////////////////////////////////////////////////////////////////////////////////////
    //Define
    /*input obj is {type : _type, width : width, height : height, trueData : true/false}*/
    defineTrack:function(o) {
      this.width = o.width;
      this.height = o.height;
      this.isTrueDataServer = o.trueData!==undefined ? o.trueData : false;
      this.type = o.type;
      

      this.dataProvider = new WaveformDataProvider();
      this.dataProvider.define(o.type,this);
    },

    /**
      Init function : va récupérer les data globales et le specific data
    **/
    init:function() {
      this.createGraphicBase();
      this.dataProvider.init();
    },


    /**
      From dataprovider
    **/
    setVisibleData:function(data) {
      this.hadFirstData = true;
      this.lastReceivedData = data;

      var showDebug=false;//hop

      A.log.log('track_waveform','setVisibleData----------------- on '+data.length);

      this.MAX_VALUE = A._i.getOnCfg('trackInfoController').getMaxValue();

      var height = this.height;
      var width = this.width;
      var barHeight = this.height-this.size.axisHeight;
      var axisHeight = this.size.axisHeight;
      var bar_width = width / data.length;

      //update scales
      this.yScale.range([barHeight, -barHeight]);
      var max_val = this.MAX_VALUE;
      this.yScale.domain([-max_val, max_val]);

      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      //this.xScale = d3.scale.linear().domain([0, 1024]); //TMP
      A.log.log('track_waveform:setVisibleData',' X scale will go from '+data[0].time+'->'+data[data.length-1].time);
      this.xScale.domain([data[0].time,data[data.length-1].time]).range([0,width]);

      //go
      var chart = this.d3chart;
      var x=this.xScale,y = this.yScale;

      var newdata =  chart.selectAll("g").data(data,function(d) {return d.time;});



      var self=this;
      //ENTER
      newdata.enter().append("g") // svg "group"
        .attr("transform", function(d, i) {
          var translateX = self.xScale(d.time);
          /*if (showDebug)
            console.log('     X : '+d.time+' --> '+translateX);*/
          return "translate(" + translateX + ","+axisHeight+")";
        })
        .append("rect")
        .attr("y", function(d) {
          var yv = barHeight - Math.abs(y(d.value)/2) - barHeight/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d.value)); })
        .attr("width", bar_width );

      //STILL HERE
      //@Todo : optim : don't do width/height/y here
      chart.selectAll("g").attr("transform", function(d, i) {
          var translateX = self.xScale(d.time);
/*
          if (showDebug)
            console.log('     X2 : '+d.time+' --> '+translateX);*/
          return "translate(" + translateX + ","+axisHeight+")";
        });  

      newdata.exit().remove();
        
    },
   
    ////////////////////////////////////////////////////////////////////////////////////
    //Generate graph

    /*Base chart creation*/
    createGraphicBase:function() {
      var height = this.height;
      var width = this.width;
      var barHeight = this.height-this.size.axisHeight;
      var axisHeight = this.size.axisHeight;

      this.node = d3.select(this.$el.find('.container_track_waveform > .svg')[0]).append("svg")
        .attr("class","chart")
        .attr("width", width)
        .attr("height", height);

      var chart = this.node.attr("width", width).attr("height", height);

      //append the data background
      /*this.node.append("rect")
          .attr("class","chart-background")
          .attr("y", axisHeight)
          .attr("x", 0)
          .attr("width", width)
          .attr("height", height-axisHeight);*/

      //append the data container
      this.node.append("g")
          .attr("class","chart-data")
          .attr("width", width)
          .attr("height", height);


      this.d3chart = chart.selectAll(".chart-data"); 

      this.yScale = d3.scale.linear();
      this.xScale = d3.time.scale(); 
    },


    /////////////////////////////////////////////////////////////////////////////////////
    //Height change
    changeHeight:function(newHeight) {
      this.height = newHeight;
      this.node.attr('height',newHeight);
      this.d3chart.attr('height',newHeight);


      var barHeight = this.height-this.size.axisHeight;
      var axisHeight = this.size.axisHeight;
      var bar_width = this.width / this.lastReceivedData.length;

      //update scales
      this.yScale.range([barHeight, -barHeight]);
      var self=this;
      var x=this.xScale,y = this.yScale;

      this.d3chart.selectAll('g').attr("transform", function(d, i) {
          var translateX = self.xScale(d.time);
          return "translate(" + translateX + ","+axisHeight+")";
        })
        .selectAll("rect")
        .attr("y", function(d) {
          var yv = barHeight - Math.abs(y(d.value)/2) - barHeight/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d.value)); })
        .attr("width", bar_width );
      //this.
    },


    /////////////////////////////////////////////////////////////////////////////////////
    //new window navigator

    //here : trackinfo is already updated
    onNavigatorNewWindow:function() {
      //new window selected!
      if (! this.hadFirstData)
        return;
      this.dataProvider.getUpdatedDataForView();


    },

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);

      //on initialize specify the sizes
      this.updateSize();
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
    ////////////////////////////////////////////////////////////////////////////////////
    //SIZES
    updateSize : function() {
      this.size = {
        axisHeight : 0
      };
    }

    
    
   
  });
});
