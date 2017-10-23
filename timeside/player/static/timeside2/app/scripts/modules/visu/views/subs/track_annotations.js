define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3',
  'moment'
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

    intern vars
      isModeCreation : false/true 
      selectedElement : null / object
  **/

  var DataProvider = Marionette.Controller.extend({
      init : function(annotationTrackObject) {
        /*if (!this.data)
          this.data = [];*/
        this.data=[];



        /**
          D3.js objects lifecycle can be a pain in the ass (if we bluntly replace the data with another one, 
            we'll have to rework the drawing main function). So we do update only if edit, or add if create
        **/
        if (annotationTrackObject) {
          _.each(annotationTrackObject.get('annotations'),function(annotation,index) {
              var dataOk = {
                start : annotation.start_time,
                end : annotation.stop_time,
                index : index,
                uuid : annotation.uuid,
                label : annotation.description,
                clicked : false,
                color :"#cf8e2a"
              }

              var alreadyThere = _.find(this.data,function(oldDataObj) {return oldDataObj.uuid==dataOk.uuid;});
              if (alreadyThere) {
                alreadyThere.start = dataOk.start;
                alreadyThere.end = dataOk.end;
                alreadyThere.label = dataOk.label;
                alreadyThere.clicked=false;
              }
              else {
                this.data.push(dataOk);
              }

              this.lastIndex = index;
          },this);  

          //console.error('TODO on annotation track object');
          return;
        }  

       /* this.data = [];
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
        }*/
      },

      //after create/edit/delete
      updateFromServer:function(view,model) {
        var self=this;
        A._i.getOnCfg('annotationControlller').udpateTrackDataFromServer(model,function(modelUpdated) {
          view.resultAnalysis = modelUpdated;
          self.init(modelUpdated);
          (_.bind(view.onNavigatorNewWindow,view))();
        });
      },

  });

  return BaseQeopaView.extend({

    template: templates['visu/sub_track_annotations'],
    className: 'track-annotations',

    ui: {
      btnCreateNewAnnotation : '[data-layout="create_new_annotation"]',
      confirmAnnotationCreationForm : '[data-layout="create_annotation_form"]',
      lblConfirmAnnotationCreation : '[data-layout="create_annotation_label"]',
      inputContentAnnotation : '[data-layout="annotation_content"]',
      lblEditAnnotationMode : '[data-layout="edit_annotation_mode"]',
      btnDeleteAnnotation : '[data-layout="delete_annotation"]',

      container : '.container_track_annotations'
    },
    events: {
      'click @ui.btnCreateNewAnnotation' : 'onClickCreateNewAnnotation',
      'click @ui.btnDeleteAnnotation' : 'onClickDeleteAnnotation',
      'click [data-layout="confirm_annotation_creation"]' : 'onClickConfirmCreateAnnotation',
      'mousemove .container_track_annotations' : 'onMouseMove',
       'mousedown .container_track_annotations' : 'onMouseDown',
      'mouseup .container_track_annotations' : 'onMouseUp',
      'click [data-layout="show_parameters"]' : 'onClickShowParameters',

      'click [data-layout="delete_annotation_track"]' : 'onClickDeleteAnnotationTrack',
      'click [data-layout="close_edit"]'      : 'onClickCloseEditWindow'
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
    //Delete button. just pass the word to the main view!
    onClickDeleteAnnotationTrack:function() {
      A._v.trigCfg('ui_project.deleteAnnotationTrack','',this.resultAnalysis);
    },



     ////////////////////////////////////////////////////////////////////////////////////
    //Brush listener

    brushed:function(e1,e2,e3) {
      
      console.log('brushed ');

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
    //Click listener
    //Start selection of annotation
    onClickElement:function(d,i) {
      console.log('click ELEMENT!');

      if (this.selectedElement && this.selectedElement.uuid == d.uuid) {
        console.log(' already selected');
        return false;
      }

      _.each(this.dataProvider.data,function(obj) {obj.clicked=false});

      d.clicked = true;//!d.clicked;
      this.selectedElement = d;
      this.updateViewEditAnnotation();
      this.onNavigatorNewWindow();
    },

    onClickShowParameters:function() {
      this.$el.toggleClass('parameters-visible');
    },

    
    ////////////////////////////////////////////////////////////////////////////////////
    //Listen for mouse over - always on, but used only when we have a selected element
    //--- EDIT ANNOTATION DRAG && DROP left & right
    onMouseMove:function(ev) {
      //console.log('Mouse over...'+ev.pageX);
      var timeForMouse = this.xScale.invert(ev.pageX);
      if (!this.selectedElement)
        return;

      if (this.isMouseDownForResizingAnnotation) {
        //resizing an annotation actual code
        var newTime = this.xScale.invert(ev.pageX);
        if (this.isResizingLowerBound)
          this.selectedElement.start = newTime.getTime();
        else
          this.selectedElement.end = newTime.getTime();

        console.log(' new time while selecting : '+newTime.getTime());
        this.ui.lblConfirmAnnotationCreation.empty().append('From '+
          A.telem.formatTimeMs(this.selectedElement.start)+" to "+A.telem.formatTimeMs(this.selectedElement.end));

        this.onNavigatorNewWindow();
        return;
      }

      var lowerBound = this.selectedElement.start+0.1*(this.selectedElement.end - this.selectedElement.start);
      var upperBound = this.selectedElement.end - 0.1*(this.selectedElement.end - this.selectedElement.start);
      var inBounds=false, isMovingLowerBound = false;
      if (timeForMouse<lowerBound && timeForMouse > this.selectedElement.start) {
        inBounds=true;isMovingLowerBound=true;
        this.ui.container.css('cursor','row-resize');
      }
      else if (timeForMouse>upperBound && timeForMouse < this.selectedElement.end) {
        inBounds=true;isMovingLowerBound=false;
        this.ui.container.css('cursor','row-resize');
      }
      else {
        this.ui.container.css('cursor','default');
      }

      //console.log('   comps : ['+this.selectedElement.start+","+lowerBound+" -> "+upperBound+","+this.selectedElement.end);

      this.canResizeAnnotation = inBounds;
      this.isResizingLowerBound = isMovingLowerBound;

    },

    onMouseDown:function(ev) {
      if (!this.selectedElement)
        return;
      if (!this.canResizeAnnotation)
        return;

      this.timeBaseForResize = this.xScale.invert(ev.pageX);
      this.isMouseDownForResizingAnnotation=true;
    },

    onMouseUp:function(ev) {
      this.isMouseDownForResizingAnnotation=false;
    },



    ////////////////////////////////////////////////////////////////////////////////////
    //Mode to edit an annotation
    updateViewEditAnnotation:function() {
      /*if (this.isModeCreation) {
        this.updateViewOnNewModeCreation(false);
      }*/
      var newModeIsCreation = false;//! this.isModeCreation;
      this.updateViewOnNewModeCreation(newModeIsCreation);
      var element = this.selectedElement;
      if (!element) {
        return console.error('ERROR : no selected element on updateViewEditAnnotation')
      }
      this.ui.lblEditAnnotationMode.empty()
      this.ui.lblEditAnnotationMode.append('Edit '+element.uuid);
      this.ui.confirmAnnotationCreationForm.removeClass('hidden');
      this.ui.lblConfirmAnnotationCreation.empty().append('Edition from '+A.telem.formatTimeMs(element.start)
            +" to "+A.telem.formatTimeMs(element.end));
      this.ui.inputContentAnnotation.val(element.label);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Button to toggle creation mode
    onClickCreateNewAnnotation:function() {
      var newModeIsCreation = ! this.isModeCreation;
      this.updateViewOnNewModeCreation(newModeIsCreation);
      if (newModeIsCreation)
        _.each(this.dataProvider.data,function(obj) {obj.clicked=false});
      this.selectedElement=null;
    },

    updateViewOnNewModeCreation:function(newModeIsCreation) {
      if (newModeIsCreation)
        this.selectedElement = null;

      this.ui.lblEditAnnotationMode.empty().val('Creating new annotation....');

      var brush = this.$el.find('rect.extent');
      if (newModeIsCreation) {
        this.$el.addClass("creating-new-annotation");
        //this.ui.btnCreateNewAnnotation.addClass('active');
        brush.attr('class','extent creation-mode');
        this.$el.find('.viewport').css('display','auto');


        this.$el.find('[data-layout="confirm_annotation_creation"] span').text('Create');
        this.$el.find('[data-layout="create_annotation_form"] h3').text('New annotation');
        this.ui.btnDeleteAnnotation.addClass("hidden");
        //this.ui.confirmAnnotationCreationForm.removeClass('hidden');
      }
      else {
        
        //this.$el.removeClass("creating-new-annotation");
        this.$el.addClass("creating-new-annotation"); //even in edit mode
        brush.attr('class','extent creation-mode');
        this.$el.find('.viewport').css('display','none');
        this.$el.find('[data-layout="confirm_annotation_creation"] span').text('Edit');
        this.$el.find('[data-layout="create_annotation_form"] h3').text('Update annotation');
        this.ui.btnDeleteAnnotation.removeClass("hidden");
        //this.ui.confirmAnnotationCreationForm.addClass('hidden');
      }
      this.isModeCreation = newModeIsCreation;
    },

    onClickCloseEditWindow:function() {
      var brush = this.$el.find('rect.extent');
      this.$el.removeClass("creating-new-annotation");
      brush.attr('class','extent');
    },


    ///USED FOR CREATION && EDITION DEPENDING OF CONTEXT
    onClickConfirmCreateAnnotation:function() {
        var self=this,
          txt = this.ui.inputContentAnnotation.val();
        //-------MODE EDITION
        if (this.selectedElement) {
          var timeStart = this.selectedElement.start,
            timeEnd = this.selectedElement.end;


          return A._i.getOnCfg('annotationControlller').updateAnnotation(this.resultAnalysis,timeStart,timeEnd,
            txt,this.selectedElement.uuid,function() {
              self.dataProvider.updateFromServer(self,self.resultAnalysis);
              (_.bind(self.onClickCloseEditWindow,self))();
              //(_.bind(self.updateViewOnNewModeCreation,self))();
            });      
        }

        //-------MODE CREATION
        if (!this.selectedDatesForAnnotation || this.selectedDatesForAnnotation.length!=2)
          return;

        var timeStart = this.selectedDatesForAnnotation[0],
            timeEnd = this.selectedDatesForAnnotation[1];

        if (txt.length<1)
            return;
        if (this.isModeCreation) {  
          A._i.getOnCfg('annotationControlller').postAnnotation(this.resultAnalysis,timeStart,timeEnd,
            txt,function() {
              self.dataProvider.updateFromServer(self,self.resultAnalysis);
              (_.bind(self.onClickCloseEditWindow,self))();
              //(_.bind(self.updateViewOnNewModeCreation,self))();
            });      
        }

    },

    /**
        Annotation deletion
    **/
    onClickDeleteAnnotation:function() {
      var self=this;
        return A._i.getOnCfg('annotationControlller').deleteAnnotation(this.resultAnalysis,this.selectedElement.uuid,function() {
              self.dataProvider.updateFromServer(self,self.resultAnalysis);
              (_.bind(self.onClickCloseEditWindow,self))();
              //(_.bind(self.updateViewOnNewModeCreation,self))();
            });      
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
      //console.log(numClickedData, numTotalData,numDivision,data);
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
      this.d3Node = node;

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

      window.debviewport = this.viewport;

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
        .on('mousedown',_.bind(self.onClickElement,self));
      
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
      
      g.selectAll('text')
        .text(function(d) {return d.label;})
      
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
            //console.log(d);
            return d.computed_height; 
          })
          .attr("width", function(d) {
            var duration = d.end - d.start;
            var xScale = self.xScale(d.end) - self.xScale(d.start);
            console.log('---> '+d.start+","+d.end+" -> "+duration+","+xScale);
            return xScale;
          } );
          g.selectAll("text")
            .attr('y',function(d){
              return d.computed_height/2;
            })
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Resize
    changeHeight:function(newHeight) {
      this.height = newHeight;
      this.d3Node.attr("height", newHeight);this.d3chart.attr('height',newHeight);
      this.yScale = d3.scale.linear().domain([0,this.dataProvider.data.length]).range([0, newHeight]);

      this.onNavigatorNewWindow();
    },


    ////////////////////////////////////////////////////////////////////////////////////
    initialize: function () {
      A._v.onCfg('navigator.newWindow','',this.onNavigatorNewWindow,this);
      this.item = A._i.getOnCfg('currentItem');
      window.debt = this;
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
