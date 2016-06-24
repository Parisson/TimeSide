define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  /**
    Annotations track
      Méthodes à exposer : 
        init(typeData)
          va récupérer les global datas, générer et afficher


      D3 : 
        La data va être mappée en x selon le temps (avec durée)
        et en y, nous allons la mapper de 0 à n, l'index de la data

        En affichage, nous allons juste modifier le scale x pour le temps et le scale y de sorte que
        toute la hauteur soit prise par les barres visibles.


  **/

  var DataProvider = Marionette.Controller.extend({
      init : function() {
        this.data = [];
        for (var i=0; i<5;i++) {
          //toutes les secondes on met un truc de taille variable
          var size = 0.2+Math.random()*0.7;
          this.data.push({start:i*2000, end : i*2000+size*2000, index : i, label : "Annot_"+i});
        }

      }
  });

  return BaseQeopaView.extend({

    template: templates['visu/sub_track_annotations'],
    className: 'track-annotations',

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

      

      this.dataProvider = new DataProvider();
    },

    /**
      Init function : va récupérer les data globales et le specific data
    **/
    init:function() {
      this.dataProvider.init();
      this.createGraphicBase();
      this.generateGraphFromData();
      this.hadFirstData=true;
    },


   
   
    ////////////////////////////////////////////////////////////////////////////////////
    //Generate graph

    /*generate all data from provider data once and for all*/
    generateGraphFromData:function() {
      var data = this.dataProvider.data;
      var newdata =  this.d3chart.selectAll("g").data(data,function(d) {return d.start;});

      var self=this;
      //ENTER
      newdata.enter().append("g")
        .attr("transform", function(d, i) {
          var translateX = self.xScale(d.start);
          var translateY = self.yScale(d.index);
          return "translate(" + translateX + ","+translateY+")";
        })
        .attr('class','annotation')
        .append("rect")
        .attr("height", function(d) {
          return 20; })
        .attr("width", function(d) {
          var duration = d.end - d.start;
          var xScale = self.xScale(d.end - d.start);
          return xScale;
        } );
    },

    /*Base chart creation*/
    createGraphicBase:function() {
      var height = this.height;
      var width = this.width;

      var node = d3.select(this.$el.find('.container_track_annotations > .svg')[0]).append("svg")
        .attr("class","chart")
        .attr("width", width)
        .attr("height", height);

      var chart = node.attr("width", width).attr("height", height);
      this.d3chart = chart;  

      this.yScale = d3.scale.linear().domain([0,this.dataProvider.data.length]).range([0, height]);
      this.xScale = d3.time.scale().domain([0,this.item.get('audio_duration')*1000]).range([0,width]);

      var chart = node.attr("width", width).attr("height", height);
      this.d3chart = chart;

      var xAxis = d3.svg.axis()
          .scale(this.xScale)
          .orient('bottom')
          .ticks(5);

      this.axis = xAxis;

      this.d3chart.call(xAxis);


      /*this.zoom = d3.behavior.zoom()
        .x(this.xScale)
        .y(this.yScale)
        .size([this.width, this.height])
        .scaleExtent([1, 10])
        .center([this.width / 2, this.height / 2])
        .on("zoom", function(a) {console.log('zoom : '+a)});*/

      /*this.d3chart.call(this.zoom);  
      window.zoom = this.zoom;*/

    },





    //////////////////////////////////
    // Render methods

    
    

    /////////////////////////////////////////////////////////////////////////////////////
    //new window navigator

    //here : trackinfo is already updated
    onNavigatorNewWindow:function() {
      //new window selected!
      if (! this.hadFirstData)
        return;
      console.log('onNavigatorNewWindow');
      var time0 =  A._i.getOnCfg('trackInfoController').currentStartTime;
      var time1 =  A._i.getOnCfg('trackInfoController').currentEndTime;

      this.xScale = d3.time.scale().domain([time0,time1]).range([0,this.width]);
      console.log('Duration is : '+(time1-time0));
      //this.zoom.scale()

      this.axis.scale(this.xScale);
      //this.d3chart.call(this.axis);
      var data = this.dataProvider.data;




      var self=this;
      this.d3chart.selectAll("g.annotation").data(data).attr("transform", function(d, i) {
          var translateX = self.xScale(d.start);
          var translateY = self.yScale(d.index);
          if (_.isNaN(translateX))
            console.log('wtf?');
          return "translate(" + translateX + ","+translateY+")";
        })
        .selectAll("rect")
        .attr("height", function(d) {
          return 20; })
        .attr("width", function(d) {
          var duration = d.end - d.start;
          var xScale = (duration*self.width) / (time1-time0);//self.xScale(duration);

          console.log(' * : '+d.index+"/"+duration+" : "+xScale);
          return xScale>0 ? xScale : 0;
        } );


    },

    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);
      this.item = A._i.getOnCfg('currentItem');
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
