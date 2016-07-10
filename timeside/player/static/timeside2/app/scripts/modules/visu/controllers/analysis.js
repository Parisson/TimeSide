define([
  '#qt_core/controllers/all',
  'd3'
],

/*
  Ce contrôleur a pour objet de lancer les chargements d'analyse pour l'item en cours et
    de pouvoir ensuite définir lesquels sont disponibles ou non.



**/

function (A,d3) {
  'use strict';

  var analysisAsked = function(analysis,item) {
    this.analysis = analysis;
    this.item = item;

    this.launch = function() {


      this.interval = setInterval(_.bind(this.testIfFinished,this),3000);
    };

    this.testIfFinished = function() {
      console.log('testing if finished my analysis : '+JSON.stringify(this.analysis));
    };

    this.onFinished = function() {
      clearInterval(this.interval);
    };


  };

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      A._i.setOnCfg('analysisController',this);
      A._v.onCfg('analysis.ask','',this.onAskAnalysis,this);
      
    },

    onDestroy : function() {
       A._v.offCfg('analysis.ask','',this.onAskAnalysis,this);
    },

    //////////////////////////////////////////////////////////////////////////////////////////////
    //
    onAskAnalysis:function(analysis) {

      var scopeAsk = new analysisAsked(analysis,A._i.getOnCfg('currentItem'));
      scopeAsk.launch();

    },


    

  

   

  });
});
