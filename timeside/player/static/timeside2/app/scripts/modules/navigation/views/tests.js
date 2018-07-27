define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['navigation/tests'],
    className: 'tests-view',

    ui: {
      'btnLaunchTest' : 'button[data-layout="test"]',
      'btnRandom' : 'button[data-layout="update"]'
    },
    events: {
      'click @ui.btnLaunchTest' : 'onLaunchTest',
      'click @ui.btnRandom' : 'randomSvg'
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    onLaunchTest:function() {
      //var wave_json;
      var wave_uri = "./data/geiger.json";
      var max_points = 1024;

      this.width = 880,
      this.height    = 200;
      var self=this;
      d3.json( wave_uri, function(error, json) {

        //calcule la moyenne sur max_points
        var means = [], currentValuesForMean= [];
        var numEltPerMean = Math.floor(json.data.length/max_points);
        _.each(json.data,function(val) {
          if (currentValuesForMean.length>=numEltPerMean) {
            means.push(d3.mean(currentValuesForMean));
            currentValuesForMean=[];
          }
          currentValuesForMean.push(val);
        });


        //self.means = json.data.slice(1, max_points);
        self.wave_json = means;
        self.alldata = json.data;

        _.bind(self.svg_render,self)(self.wave_json,".waveform >  .svg" );
      });


    },



   
    //render le bloc de tout le morceau
    svg_render:function( data, svg ) {

      var height = this.height;
      var width = this.width;

      var node = d3.select(svg).append("svg")
        .attr("class","chart")
        .attr("width", width)
        .attr("height", height);

      var y = d3.scale.linear().range([height, -height]);
      var max_val = d3.max(data, function(d) { return d; });

      this.TOTAL_MAX = max_val; //used for second window (on reste sur un scale Y constant)

      y.domain([-max_val, max_val]);
      var x = d3.scale.linear().domain([0, data.length]);
      var bar_width = width / data.length;

      var chart = node.attr("width", width).attr("height", height);
      this.$chart = chart;

      var bar = chart.selectAll("g")
        .data(data)
        .enter().append("g") // svg "group"
        .attr("transform", function(d, i) {
          return "translate(" + i * bar_width + ",0)";
        })
        .append("rect")
        .attr("y", function(d) {
          var yv = height - Math.abs(y(d)/2) - height/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d)); })
        .attr("width", bar_width );


      var xScale = d3.scale.linear()
        .domain([0, data.length])
        .range([0, width]),
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

      this.viewport = d3.svg.brush()
        .x(xScale)
        .on("brush", _.bind(this.brushed,this));


      chart.append("g")
        .attr("class", "viewport")
        .call(this.viewport)
        .selectAll("rect")
        .attr("height", height);


    },

    brushed:function(e1,e2,e3) {
      console.log('brushed : '+this.viewport.extent());
      this.randomDynamicBloc(this.viewport.extent()[0],this.viewport.extent()[1]);
    },


    //render le bloc dynamique
    randomDynamicBloc:function(indexStart,indexEnd) {
      var max_points = 1024;

      var indexInAllData = Math.floor((indexStart/max_points)*this.alldata.length);//Math.floor(positionPercent*this.alldata.length);
      var indexEndAllData = Math.floor((indexEnd/max_points)*this.alldata.length)//Math.floor((positionPercent+widthPercent)*this.alldata.length);

      var data;

      if ((indexEndAllData-indexInAllData)<max_points) {
        data = this.alldata.slice(indexInAllData,indexEndAllData);
      }
      else {

        //on récupère les valeurs qui nous intéressent
        var means = [], currentValuesForMean= [];
        var numEltPerMean = Math.floor((indexEndAllData-indexInAllData)/max_points);

        for (var i=indexInAllData; i<(Math.min(this.alldata.length,indexEndAllData)); i++) {
          var val = this.alldata[i];
          if (currentValuesForMean.length>=numEltPerMean) {
              means.push(d3.mean(currentValuesForMean));
              currentValuesForMean=[];
            }
            currentValuesForMean.push(val);
        }

        //from here
        data = means;
      }

      //params
      var height = this.height;
      var width = this.width;
      var y = d3.scale.linear().range([height, -height]);
      var max_val = this.TOTAL_MAX;// d3.max(data, function(d) { return d; });


      y.domain([-max_val, max_val]);
      var x = d3.scale.linear().domain([0, data.length]);
      var bar_width = width / data.length;

      //création de la sélection initiale if not exists
      if (! this.chartDynamic) {
        var node = d3.select(".waveform >  .svg2").append("svg")
          .attr("class","chart")
          .attr("width", width)
          .attr("height", height);

        var chart = node.attr("width", width).attr("height", height);
        this.chartDynamic = chart;
      }

      var newdata =  this.chartDynamic.selectAll("g").data(data);

      /*this.chartDynamic.selectAll("g")*/
      newdata
        .enter().append("g") // svg "group"
        .attr("transform", function(d, i) {
          return "translate(" + i * bar_width + ",0)";
        })
        .append("rect")
        .attr("y", function(d) {
          var yv = height - Math.abs(y(d)/2) - height/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d)); })
        .attr("width", bar_width );

       this.chartDynamic.selectAll("g")/*.transition(0.75)*/.attr("transform", function(d, i) {
          return "translate(" + i * bar_width + ",0)";
        }).select('rect')
        .attr("y", function(d) {
          var yv = height - Math.abs(y(d)/2) - height/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d)); })
        .attr("width", bar_width );

      newdata.exit().remove();
    },



    ///test : redo svg different values
    randomSvg:function () {
      var index = Math.floor(Math.random()*(this.alldata.length-2048));
      var newdata = this.alldata.slice(index,index+1024);

      var y = d3.scale.linear().range([this.height, -this.height]);
      var max_val = d3.max(newdata, function(d) { return d; });
      y.domain([-max_val, max_val]);

      var height = this.height;
      var bar_width = this.width / newdata.length;

      var newData = this.$chart.selectAll("g").data(newdata);

     newData.enter().append("g") // svg "group"
        .attr("transform", function(d, i) {
          return "translate(" + i * bar_width + ",0)";
        })
        .append("rect")
        .attr("y", function(d) {
          var yv = height - Math.abs(y(d)/2) - height/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d)); })
        .attr("width", bar_width );

      this.$chart.selectAll("g").transition(0.75).attr("transform", function(d, i) {
          return "translate(" + i * bar_width + ",0)";
        }).select('rect')
        .attr("y", function(d) {
          var yv = height - Math.abs(y(d)/2) - height/2 + 2;
          return yv;
        })
        .attr("height", function(d) {
          return Math.abs(y(d)); })
        .attr("width", bar_width );

      newData.exit().remove();
      return;  

     
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      window.home = this;
    },

    onRender:function() {
       
    },

    onDestroy: function () {      
    },

    onDomRefresh:function() {
    },

    serializeData: function () {
      

      return {
       
      }
    },


    
    
   
  });
});
