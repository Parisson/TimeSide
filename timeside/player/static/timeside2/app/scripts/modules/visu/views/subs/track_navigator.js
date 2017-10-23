define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  /**
    navigation track
    reprend la forme d'onde de base, sur 1024 points
  **/
  return BaseQeopaView.extend({

    template: templates['visu/sub_track_navigator'],
    className: 'nav-track',

    ui: {
     
    },
    events: {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////
    onNewSegmentLoop:function() {
      var timeSegment1 = A._i.getOnCfg('currentLoopSegment')[0];
      var timeSegment2 = A._i.getOnCfg('currentLoopSegment')[1];
      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();

      var x1 = this.xScale(timeSegment1);
      var x2 = this.xScale(timeSegment2);

      this.loopSegmentRectangle.attr('x',x1).attr('width',(x2-x1));
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
     brushed:function(e1,e2,e3) {
      
      var time1 = (this.viewport.extent()[0]).getTime();
      var time2 = (this.viewport.extent()[1]).getTime();
      //console.log('new times : '+time1+','+time2);

      if (time1===time2) {
        return console.log('@TODO : case when time1=time2');
      }

      A._i.getOnCfg('trackInfoController').updateStartEndTimeFromNav(time1,time2);

      //console.log('Brushed : '+time1+","+time2);

      //let's tell the tracks the good news!
      A._v.trigCfg('navigator.newWindow','');


      //this.randomDynamicBloc(this.viewport.extent()[0],this.viewport.extent()[1]);
    },
    
    ////////////////////////////////////////////////////////////////////////////////////
    //Generate graph
    startLoading:function(width,height,callbackLoaded) {
      
      this.width = width;
      this.height = height;
      this.callbackLoaded = callbackLoaded;

      //server to be ready
      this.loadData();
    },


    //1 : load data
    loadData:function() {
      var trackDuration = A._i.getOnCfg('trackInfoController').getDuration();
      var useFakeData = A._i.getOnCfg('useFakeData');

      if (!useFakeData)
        A._v.trigCfg('trueserver.getdata','','waveform',0,trackDuration,1024,null,_.bind(this.onData,this));      
      else
        A._v.trigCfg('fakeserver.getdata','','waveform',0,trackDuration,1024,null,_.bind(this.onData,this));

      
    },

    //2 : keep data & start rendering
    onData:function(data) { 
      console.log('hey im so happy');
      this.data = data;
      this.createBaseChart();
      this.createAxis();
      this.createBrush();
      this.createCursor();
      this.createLoopSegment();

      //pour click curseur // @TODO : CREATE CURSEUR
      this.clickContainer = this.$el.find('.container_track_navigator > .svg');
      this.clickContainer.on('click',_.bind(this.onClick,this));

      A._i.getOnCfg('trackInfoController').setMaxValue(this.max_val);

      if (this.callbackLoaded)
        this.callbackLoaded();
    },

    ////////////////////////////////////////////////////////////////////
    // Click & cursor methods
    onClick:function(evt) {

      var x = evt.pageX - this.clickContainer.offset().left;
      var relativeX = x / this.width;
     //console.log('???? : '+evt.pageX+","+this.clickContainer.offset().left+" ==> "+x+" : "+relativeX);

      A._v.trigCfg('audio.setCurrentTime','',relativeX);
      console.log('CLICK!!!'+relativeX);
    },

    onNewTime:function(fraction) {
      var pixel = Math.round(fraction * this.width);
      if (this.cursorView)
        this.cursorView/*.transition()*/.attr('x',pixel);
    },

    ////////////////////////////////////////////////////////////////////
    // Render methods

    //1
    //creates the chart, kept as this.d3chart
    createBaseChart:function() {
      var height = this.height;
      var barHeight = this.height-this.size.axisHeight;
      var axisHeight = this.size.axisHeight;
      var width = this.width;
      var data = this.data;

      var node = d3.select(this.$el.find('.container_track_navigator > .svg')[0]).append("svg")
        .attr("class","chart")
        .attr("width", width)
        .attr("height", height);

        //append the data background
        node.append("rect")
            .attr("class","chart-background")
            .attr("y", axisHeight)
            .attr("x", 0)
            .attr("width", width)
            .attr("height", height-axisHeight);

        //append the data container
        node.append("g")
            .attr("class","chart-data")
            .attr("width", width)
            .attr("height", height);



      //creating y  
      var y = d3.scale.linear().range([barHeight, -barHeight]);
      var max_val = d3.max(data, function(d) { return d.value; });
      this.max_val = max_val;
      y.domain([-max_val, max_val]);


      //var x = d3.scale.linear().domain([0, data.length]);

      A.log.log('track_navigator:setVisibleData',' scale will go from '+data[0].time+'->'+data[data.length-1].time);
      var x = d3.time.scale().domain([data[0].time,data[data.length-1].time]).range([0,width]);
      this.xScale = x;


      var bar_width = width / data.length;

      var chart = node.attr("width", width).attr("height", height);
      this.d3chart = chart;

      var bar = chart.selectAll(".chart-data").selectAll("g")
        .data(data,function(d) {return d.time;})
        .enter().append("g") // svg "group"
        .attr("transform", function(d, i) {
          return "translate(" + i * bar_width + ","+axisHeight+")";
        })
        .append("rect")
        .attr("y", function(d) {
          var yv = barHeight - Math.abs(y(d.value)/2) - barHeight/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d.value)); })
        .attr("width", bar_width );
    },

    //2
    //Create the axis
    createAxis:function() {
      var height = this.height, width = this.width, data = this.data, chart = this.d3chart,
        max_val=this.max_val;

      var xScale = this.xScale;/*d3.scale.linear()
        .domain([0, data.length])
        .range([0, width]),*/
      
      var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('bottom')
          .ticks(5)
          .tickFormat(function(arg) {
            return A.telem.formatTimeMs(arg.getTime());
          });
          
      chart.append('g')
          .attr('class', 'x axis')
          //.attr('transform', 'translate(0,' + (height-30) + ')')
          .call(xAxis);

      this.xScale = xScale;

      
    },

    //3
    //create the brush
    createBrush:function() {
      var height = this.height, width = this.width, data = this.data, chart = this.d3chart,
        max_val=this.max_val,
        axisHeight = this.size.axisHeight;


      this.viewport = d3.svg.brush()
        .x(this.xScale)
        .on("brush", _.bind(this.brushed,this));

      chart.append("g")
        .attr("class", "viewport")
        .call(this.viewport)
        .selectAll("rect")
        .attr("height", height-axisHeight)
        .attr('transform', 'translate(0,'+axisHeight+')');  
    },

    //4
    //create cursor
    createCursor:function() {
      this.cursorView = this.d3chart.append("rect")
        .attr('class',"cursor")
        .attr('x',0)
        .attr('y',0)
        .attr('width',2)
        .attr('height',this.height);

    },

    //5
    //create segment loop
    createLoopSegment:function() {
      this.loopSegmentRectangle = this.d3chart.insert("rect",":first-child")
        .attr('class',"loop-segment")
        .attr('x',0).attr('y',0)
        .attr('width',2).attr('height',this.height)
        .attr('opacity',0.6);
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Zoom management
    //factor can be <1 (more zoom) or >1 (less zoom)
    onZoomCommand:function(factor) {

      //var deltaTimeMsec = factor<1 ? 50 : -50;

      var time1 = (this.viewport.extent()[0]).getTime();
      var time2 = (this.viewport.extent()[1]).getTime();

      //console.log('before zoom, we have : '+(time2-time1)+" and factor is : "+factor);
      if ((time2 - time1)>0 && (time2-time1)<500 && factor<1)
        return;

      var audioDuration = A._i.getOnCfg('currentItem').get('audio_duration')*1000;
      if ( (time2-time1) >= audioDuration && factor>1)
        return;

      var center = time1 + (time2-time1)/2,
        distanceFromCenter = (time2-time1)/2;
      var newDistanceFromCenter = distanceFromCenter*factor;

      time1 = Math.max(center - newDistanceFromCenter,0);
      time2 = center+newDistanceFromCenter;

      if (time2>audioDuration)
        time2 = audioDuration;
/*
      time1 = Math.max(time1 -deltaTimeMsec, 0);
      time2 = time2+deltaTimeMsec;
*/
      if (time1>=time2)
        time2 = time1+100;

      this.viewport.extent([new Date(time1), new Date(time2)]);
      this.viewport(d3.select('.viewport'));
      this.viewport.event(d3.select('.viewport'));
    },




    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('audio.newAudioTime','',this.onNewTime,this);
      A._v.onCfg('ui_project.segmentLoopUpdate','',this.onNewSegmentLoop,this);
      A._v.onCfg('ui_project.zoom','',this.onZoomCommand,this);      
      //on initialize specify the sizes
      this.updateSize();

      window.debtn = this;
    },

    onRender:function() {
       
    },

    onDestroy: function () {     


      this.$el.find('.container_track_navigator > .svg').off('click'); 

      A._v.offCfg('audio.newAudioTime','',this.onNewTime,this);
      A._v.offCfg('ui_project.segmentLoopUpdate','',this.onNewSegmentLoop,this);
    },


    serializeData: function () {
      

      return {
       
      }
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //SIZES
    updateSize : function() {
      this.size = {
        axisHeight : 15
      };
    }

    
    
   
  });
});
