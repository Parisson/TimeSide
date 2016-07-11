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

  var UNIQUE_ID_ANALYSIS = 1;

  var analysisAsked = function(analysis,item) {
    this.analysis = analysis;
    this.item = item.toJSON ? item.toJSON() : item;

    this.launch = function() {


      this.interval = setInterval(_.bind(this.testIfFinished,this),4000);

      //so view knows we're launching something
      this.uniqueIdAnalysis = UNIQUE_ID_ANALYSIS++;
      A._v.trigCfg('analysis.asked','',this.uniqueIdAnalysis);
      this.testIfFinished();
    };

    this.testIfFinished = function() {
      console.log('testing if finished my analysis : '+JSON.stringify(this.analysis));
      var data = {
        analysis : this.analysis.url,
        item : this.item.url
      }, self=this;
      var url = $.post('http://149.202.199.160:8000/timeside/api/analysis_track/',data,function(a,b,c) {
        console.log('Ok donc on fait quoi ?');

        if (a.result_url && a.result_url.indexOf('http://')===0) {
          //alert('success');
          console.log('success');
          self.onFinished(a);
        }
        else
          console.log('Still not finished');
      });
    };

    this.onFinished = function(result) {
      clearInterval(this.interval);
      var resultModel = new A.models.resultAnalysis(result);
      resultModel.set('uniqueIDForView',this.uniqueIdAnalysis),

      A._v.trigCfg('analysis.result','',resultModel);
      //@TODO
      //@TODO

      // créer un model de result_analysis
      // côté vue : 
      // quand le controleur lance un loading, ikl doit lancer un event analysis_started avec un token unique 
      // comme ça un segment se met en place visuellement en mode waiting
      // quand ok, il doit mettre sur le currentItem l'analyse et ensuite remplacer le analysis started par le bon resultat
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
