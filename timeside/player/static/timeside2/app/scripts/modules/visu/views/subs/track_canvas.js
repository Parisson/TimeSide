define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  '#visu/controllers/providers/bitmap_dataprovider'
],

function (Marionette,A,BaseQeopaView,BitmapDataProvider) {
  'use strict';

  /**
    Waveform track
      Méthodes à exposer : 
        init(typeData)
          va récupérer les global datas, générer et afficher

  **/
  return BaseQeopaView.extend({

    template: templates['visu/sub_track_canvas'],
    className: 'track-canvas',

    ui: {
     
    },
    events: {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Define
    /*input obj is {type : _type, width : width, height : height}*/
    defineTrack:function(o) {
      this.width = o.width;
      this.height = o.height;

      this.resultAnalysis = o.resultAnalysis;

      this.dataProvider = new BitmapDataProvider();
      this.dataProvider.define(o.type,this,this.resultAnalysis);
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
      Here, data IS AN IMAGE DATA!!!! 
        Supposed to be proper width & height!!!!!
        if not, blame the controller
        or is it??? :)


        DEPRECATED!!! Now called from controller

    **/
    setVisibleData:function(data) {
      this.hadFirstData = true;

      A.log.log('track_canvas','set visible data. Data dims : '+data.width+' : '+data.height);

      /*if (data instanceof HTMLImageElement)*/
        this.canvasContext.drawImage(data, 0, 0, data.width,data.height,
          0, 0, this.canvas.width, this.canvas.height);
      /*else
        this.canvasContext.putImageData(data, 0, 0, 0, 0,
          this.canvas.width, this.canvas.height);*/
/*
       this.canvasContext.putImageData(data, 0, 0, 0, 0,
        this.canvas.width, this.canvas.height);
       */
        
    },
   
    ////////////////////////////////////////////////////////////////////////////////////
    //Generate graph

    /*Base chart creation*/
    createGraphicBase:function() {
      var height = this.height;
      var width = this.width;

      A.log.log('track_canvas','preparing canvas for dimensions : ['+this.width+';'+this.height+']');

      var canvas = this.$el.find('canvas.canvas')[0];
      var ctx = canvas.getContext("2d");
      canvas.width = width;
      canvas.height = height;

      this.canvas = canvas;
      this.canvasContext = ctx;


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
