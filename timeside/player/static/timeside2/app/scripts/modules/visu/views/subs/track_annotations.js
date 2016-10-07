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
      init : function(annotationTrackObject) {

        this.data = [];
        if (annotationTrackObject) {
          console.error('TODO on annotation track object');
          return;
        }  

        this.data = [];
        var numItem = 50;
        var stepPerItem = 200;
        for (var i=0; i<numItem;i++) {
          //toutes les secondes on met un truc de taille variable
          var size = 0.2+Math.random()*0.7;
          this.data.push({
            start:i*stepPerItem, 
            end : i*stepPerItem+size*stepPerItem, 
            index : i, label : "Annot_"+i, 
            clicked : (i%3==0 ? true : false),
            color :"#cf8e2a"
          });
        }

      }
  });

  return BaseQeopaView.extend({

    template: templates['visu/sub_track_annotations'],
    className: 'track-annotations',

    ui: {
      btnCreateNewAnnotation : '[data-layout="create_new_annotation"]',
      confirmAnnotationCreationForm : '[data-layout="create_annotation_form"]',
      lblConfirmAnnotationCreation : '[data-layout="create_annotation_label"]',
      inputContentAnnotation : '[data-layout="annotation_content"]'
    },
    events: {
      'click @ui.btnCreateNewAnnotation' : 'onClickCreateNewAnnotation',
      'click [data-layout="confirm_annotation_creation"]' : 'onClickConfirmCreateAnnotation'
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

      this.resultAnalysis = o.resultAnalysis; //will be the annotation track object


      this.dataProvider = new DataProvider();
    },

    /**
      Init function : va récupérer les data globales et le specific data
    **/
    init:function() {
      this.dataProvider.init(this.resultAnalysis);
      this.createGraphicBase();
      this.createBrush();
      this.onNavigatorNewWindow();
      //this.generateGraphFromData();
      this.hadFirstData=true;
    },

     ////////////////////////////////////////////////////////////////////////////////////
    //Brush listener

    brushed:function(e1,e2,e3) {
      
      //console.log('new times : '+time1+','+time2);

      //var a = this.xScale.
      if (!this.isModeCreation)
        return;


      var a = (this.viewport.extent()[0]);
      var b = (this.viewport.extent()[1]);
      this.lastBrushData = this.viewport.extent();
      this.ui.lblConfirmAnnotationCreation.empty().append('From '+a.getTime()+" to "+b.getTime());
      this.selectedDatesForAnnotation = [a.getTime(),b.getTime()]
      console.log('brushed annot track : '+JSON.stringify(a)+" -> "+JSON.stringify(b));

    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Button to toggle creation mode
    onClickCreateNewAnnotation:function() {
      var newModeIsCreation = ! this.isModeCreation;
      var brush = this.$el.find('rect.extent');
      if (newModeIsCreation) {
        this.ui.btnCreateNewAnnotation.addClass('active');
        brush.attr('class','extent creation-mode');
        this.$el.find('.viewport').css('display','auto');
        this.ui.confirmAnnotationCreationForm.removeClass('hidden');
      }
      else {
        this.ui.btnCreateNewAnnotation.removeClass('active'); 
        brush.attr('class','extent');
        this.$el.find('.viewport').css('display','none');
        this.ui.confirmAnnotationCreationForm.addClass('hidden');
      }
      this.isModeCreation = newModeIsCreation;
    },


    onClickConfirmCreateAnnotation:function() {
        if (!this.selectedDatesForAnnotation || this.selectedDatesForAnnotation.length!=2)
          return;
        var txt = this.ui.inputContentAnnotation.val(),
            timeStart = this.selectedDatesForAnnotation[0],
            timeEnd = this.selectedDatesForAnnotation[1];

        if (txt.length<1)
            return;
        A._i.getOnCfg('annotationControlller').postAnnotation(this.resultAnalysis,timeStart,timeEnd,
          txt,function() {
            alert('impact view from success')
          });      

        alert('go!');
    },
    

    ////////////////////////////////////////////////////////////////////////////////////
    //Click listener

    
    onClickElement:function(d,i) {
      console.log('click ELEMENT!');
      d.clicked = !d.clicked;
      this.onNavigatorNewWindow();
    },

      ////////////////////////////////////////////////////////////////////////////////////
    //Function to check the data clicked and compute heights / y
    computeHeightElementsOnData:function(data) {
      if(!data)
        data = this.dataProvider.data;
      var numTotalData = data.length;
      var numClickedData = 0;
      _.each(data,function(_data) {if (_data.clicked) numClickedData++});
      //Clicked  elements weight twice more than non clicked
      var numDivision = numClickedData*2 + (numTotalData-numClickedData );

      var heightPerDivision = Math.floor(this.height/numDivision);

      var currentY = 0;
      _.each(data,function(_data) {
        _data.computed_height = _data.clicked ? 2*heightPerDivision : heightPerDivision;
        _data.computed_y = currentY;
        currentY+=_data.computed_height;

      });
      console.log(numClickedData, numTotalData,numDivision,data);
      return data;
    },
   
   
    ////////////////////////////////////////////////////////////////////////////////////
    //Generate graph
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

      /*var xAxis = d3.svg.axis()
          .scale(this.xScale)
          .orient('bottom')
          .ticks(5);

      this.axis = xAxis;

      this.d3chart.call(xAxis);*/
    },

    createBrush:function() {
      var height = this.height, width = this.width, chart = this.d3chart;


      this.viewport = d3.svg.brush()
        .x(this.xScale)
        /*.y(this.yScale)*/
        .on("brush", _.bind(this.brushed,this));

      chart.append("g")
        .attr("class", "viewport")
        .call(this.viewport)
        .selectAll("rect")
        .attr("height", this.height-50)
        .attr('transform', 'translate(0,'+25+')');  

      //we do not start in creation mode
      this.$el.find('.viewport').css('display','none');
    },



    /////////////////////////////////////////////////////////////////////////////////////
    //new window navigator

    //here : trackinfo is already updated
    onNavigatorNewWindow:function() {
      //new window selected!
      //if (! this.hadFirstData)
      //  return;

      //UPDATE BRUSH
      /**
          brush.extent([new Date(2000),new Date(3000)]); &&
          chart.call(brush);
              font quelque chose mais wtf? 
      **/


      console.log('onNavigatorNewWindow');
      var time0 =  A._i.getOnCfg('trackInfoController').currentStartTime;
      var time1 =  A._i.getOnCfg('trackInfoController').currentEndTime;


      this.xScale = d3.time.scale().domain([time0,time1]).range([0,this.width]);
      this.viewport.x(this.xScale);

      //update brush scale
      if (this.lastBrushData) {
        this.viewport.extent(this.lastBrushData);
        this.d3chart.call(this.viewport);
      }  

      //console.log('Duration is : '+(time1-time0));
      //this.zoom.scale()

      //this.axis.scale(this.xScale);
      //this.d3chart.call(this.axis);
      var data = this.dataProvider.data;
      //B : REMOVING
      
      
      //1 8 FILTER DATA TO HAVE THOSE IN THE TIME RAHGE
      var filtered = data.filter(function(d){
        if(
          (d.start <= time0 && d.end>=time0)    // end of annotation is inside
          || (d.start >= time0 && d.end<=time1) // all anotation inside
          || (d.start < time1 && d.end>=time1)  // start of annotation is inside
        ) {
          return true;
        }
        return false;
      });

      //2 MAGIC HEIGHT FROM ERIC
      filtered = this.computeHeightElementsOnData(filtered);
      
      //BIND DATA TO ELEMENTS
      var self=this;
      var g = this.d3chart.selectAll("g.annotation").data(filtered, function(d) { return d.start; });
      //REMOVE OUT OF SCOPE
      g.exit().remove();
      //ADD NEW
      var newG = g.enter()
        .append("g")
        .attr('class','annotation')
        .attr("style", function(d) {
           return "clip-path: url(#"+("mettre-id-unique-ici"+d.start)+");";
        })
        .on('click',_.bind(self.onClickElement,self));
      
      //Add the clip path on this annotation
      newG.append("defs").append("clipPath")
        .attr("id", function(d) {
          return "mettre-id-unique-ici"+d.start;
        }).append("rect");
      
      //the visible rectangle
      newG.append('rect')
        .attr("fill", function(d){
          return d.color;
        });
      
      //and the text
      newG.append('text')
        .attr('x',10)
        .text(function(d) {return d.label;})
      
      /*
        .attr("height", function(d) {
          return d.computed_height; 
        })
        .attr("width", function(d) {
          var duration = d.end - d.start;
          var xScale = self.xScale(d.end) - self.xScale(d.start);
          return xScale;
        } );*/
      
      //UPDATE ALL REMAINING
      g.attr("class", function(d, i) {
          if(d.clicked) {
            return "annotation active";
          }
          return "annotation";
          
        })
        .attr("transform", function(d, i) {
          var translateX = self.xScale(d.start);
          var translateY = d.computed_y;// self.yScale(d.index);
          return "translate(" + translateX + ","+translateY+")";
        })
        .selectAll("rect")
         .attr("height", function(d) {
            console.log(d);
            return d.computed_height; 
          })
          .attr("width", function(d) {
            var duration = d.end - d.start;
            var xScale = self.xScale(d.end) - self.xScale(d.start);
            return xScale;
          } );
          g.selectAll("text")
            .attr('y',function(d){
              return d.computed_height/2;
            })
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
      var title = this.resultAnalysis ? this.resultAnalysis.get('title') : 'New Annotation track'

      return {
          title : title       
      }
    }
  });
});
