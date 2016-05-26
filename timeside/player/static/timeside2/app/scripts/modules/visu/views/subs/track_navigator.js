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
    //Definition
    isTrueDataServer : false,


    ////////////////////////////////////////////////////////////////////////////////////
    //Func
     brushed:function(e1,e2,e3) {
      
      var time1 = (this.viewport.extent()[0]).getTime();
      var time2 = (this.viewport.extent()[1]).getTime();
      console.log('new times : '+time1+','+time2);

      if (time1===time2) {
        return console.log('@TODO : case when time1=time2');
      }

      A._i.getOnCfg('trackInfoController').updateStartEndTimeFromNav(time1,time2);

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
      if (this.isTrueDataServer)
        A._v.trigCfg('trueserver.getdata','','waveform',0,trackDuration,1024,_.bind(this.onData,this));      
      else
        A._v.trigCfg('fakeserver.getdata','','waveform',0,trackDuration,1024,_.bind(this.onData,this));

      
    },

    //2 : keep data & start rendering
    onData:function(data) { 
      console.log('hey im so happy');
      this.data = data;
      this.createBaseChart();
      this.createAxis();
      this.createBrush();
      this.createCursor();

      //pour click curseur // @TODO : CREATE CURSEUR
      this.clickContainer = this.$el.find('.container_track_navigator > .svg');
      this.clickContainer.on('click',_.bind(this.onClick,this));

      A._i.getOnCfg('trackInfoController').setMaxValue(this.max_val);

      if (this.callbackLoaded)
        this.callbackLoaded();
    },

    //////////////////////////////////
    // Click & cursor methods
    onClick:function(evt) {

      var x = evt.pageX - this.clickContainer.offset().left;
      var relativeX = x / this.width;
      A._v.trigCfg('audio.setCurrentTime','',relativeX);
      console.log('CLICK!!!'+relativeX);
    },

    onNewTime:function(fraction) {
      var pixel = Math.round(fraction * this.width);
      if (this.cursorView)
        this.cursorView.transition().attr('x',pixel);
    },

    //////////////////////////////////
    // Render methods

    //1
    //creates the chart, kept as this.d3chart
    createBaseChart:function() {
      var height = this.height;
      var width = this.width;
      var data = this.data;

      var node = d3.select(this.$el.find('.container_track_navigator > .svg')[0]).append("svg")
        .attr("class","chart")
        .attr("width", width)
        .attr("height", height);


      //creating y  
      var y = d3.scale.linear().range([height, -height]);
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

      var bar = chart.selectAll("g")
        .data(data,function(d) {return d.time;})
        .enter().append("g") // svg "group"
        .attr("transform", function(d, i) {
          return "translate(" + i * bar_width + ",0)";
        })
        .append("rect")
        .attr("y", function(d) {
          var yv = height - Math.abs(y(d.value)/2) - height/2 + 2;
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

      var xScale = this.xScale,/*d3.scale.linear()
        .domain([0, data.length])
        .range([0, width]),*/
      yScale = d3.scale.linear()
        .domain([-max_val, max_val]).nice()
        .range([height, 0]); 
      
      var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('bottom')
          .ticks(5),
          yAxis = d3.svg.axis()
          .scale(yScale)
          .orient('left');

      chart.append('g')
          .attr('class', 'x axis')
          .attr('transform', 'translate(0,' + (height-30) + ')')
          .call(xAxis);

      chart.append('g')
          .attr('class', 'y axis')
          .attr('transform', 'translate(40,0)')
          .call(yAxis);  

      this.xScale = xScale;
      this.yScale=yScale;
    },

    //3
    //create the brush
    createBrush:function() {
      var height = this.height, width = this.width, data = this.data, chart = this.d3chart,
        max_val=this.max_val;

      this.viewport = d3.svg.brush()
        .x(this.xScale)
        .on("brush", _.bind(this.brushed,this));


      chart.append("g")
        .attr("class", "viewport")
        .call(this.viewport)
        .selectAll("rect")
        .attr("height", height);  
    },

    //4
    //create cursor
    createCursor:function() {
      this.cursorView = this.d3chart.append("rect")
        .attr('x',200)
        .attr('y',0)
        .attr('width',2)
        .attr('height',this.height);

    },




    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('audio.newAudioTime','',this.onNewTime,this);
    },

    onRender:function() {
       
    },

    onDestroy: function () {     


      this.$el.find('.container_track_navigator > .svg').off('click'); 

      A._v.offCfg('audio.newAudioTime','',this.onNewTime,this);
    },


    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
