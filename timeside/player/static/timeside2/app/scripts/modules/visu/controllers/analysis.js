define([
  '#qt_core/controllers/all',
  'd3'
],

/*
  Ce contrôleur a pour objet de lancer les chargements d'analyse pour l'item en cours et
    de pouvoir ensuite définir lesquels sont disponibles ou non.

    Ici, la création par item_new_view d'une analyse (post choix popup) appellera donc onAskAnalysis
    avec : 
        "{"url":"http://timeside-dev.telemeta.org/timeside/api/analysis/c36a5e2f-9b2a-4034-811b-344b9cb86800/",
            "uuid":"c36a5e2f-9b2a-4034-811b-344b9cb86800",
            "title":"Singings detection",
            "preset":"http://timeside-dev.telemeta.org/timeside/api/presets/cd8d57f2-eaf9-4906-9c51-e7bf7babd19f/",
            "sub_processor":"http://timeside-dev.telemeta.org/timeside/api/subprocessors/irit_singing.segments/"}"

      ==> Appel d'un post sur http://timeside-dev.telemeta.org/timeside/api/analysis_tracks/ qui va créer la track
          en question.


      Pendant ce traitement : 
          A._v.trigCfg('analysis.asked','',this.uniqueIdAnalysis); -> annonce à la vue qu'un item est en cours de création
      puis : 
          A._v.trigCfg('analysis.result','',resultModel); -> traitement est ready



**/

function (A,d3) {
  'use strict';

  var UNIQUE_ID_ANALYSIS = 1;

  var analysisAsked = function(analysis,item) {
    this.analysis = analysis;
    this.item = item.toJSON ? item.toJSON() : item;

    this.launch = function() {


      //this.interval = setInterval(_.bind(this.testIfFinished,this),4000);

      //so view knows we're launching something
      this.uniqueIdAnalysis = UNIQUE_ID_ANALYSIS++;
      A._v.trigCfg('analysis.asked','',this.uniqueIdAnalysis);
      this.testIfExists();
    };

    //1 : test if exists
    this.testIfExists = function() {
      var urlTest = A.getApiUrl()+'/analysis_tracks/';
      var data = {
        analysis : this.analysis.uuid,
        item : this.item.uuid
      };
      var self=this;

      $.ajax({url : urlTest,data : data,
        type : "get",
        headers : {"X-CSRFToken" : A.injector.get(A.injector.cfg.csrfToken)},
        /*headers : {
          "Authorization" : "Token "+A.injector.get('serverToken')
        },*/
        error : function(error) {
          console.error('error on analysis : '+error);
        },
        success : function(a) {
          if (a.length>1)
            console.error('Warning : more than one result on '+urlTest+' & '+JSON.stringify(data));

          if (a.length==0) {
            //we need to create one
            console.log('We need to create a new analysis_track');
            self.interval = setInterval(_.bind(self.testIfFinished,self),4000);
            return (_.bind(self.testIfFinished,self)) ();
          }


            console.log('We have a new analysis_track, lets use it');
          var result = a[0];
          return self.onFinished(result);
        }
      });

      /*$.get(urlTest,data,function(a,b,c) {
        if (b!="success")
          return console.error('error on get analysis_tracks : '+b);

        if (a.length>1)
          console.error('Warning : more than one result on '+urlTest+' & '+JSON.stringify(data));

        if (a.length==0) {
          //we need to create one
          console.log('We need to create a new analysis_track');
          self.interval = setInterval(_.bind(self.testIfFinished,self),4000);
          return (_.bind(self.testIfFinished,self)) ();
        }


          console.log('We have a new analysis_track, lets use it');
        var result = a[0];
        return self.onFinished(result);

      });*/
      //this.testIfFinished();
    };

    //2 : created : wait if finished
    this.testIfFinished = function() {
      console.log('testing if finished my analysis : '+JSON.stringify(this.analysis));
      var data = {
        analysis : this.analysis.url,
        item : this.item.url
      }, self=this;

      $.ajax({url :  A.getApiUrl()+'/analysis_tracks/',data : data,
        type : "post",
        headers : {"X-CSRFToken" : A.injector.get(A.injector.cfg.csrfToken)},
        /*headers : {
          "Authorization" : "Token "+A.injector.get('serverToken')
        },*/
        error : function(error) {
          console.error('error on analysis tyrack : '+error);
        },
        success : function(a) {
          if (a.result_url && a.result_url.indexOf('http://')===0) {
            //alert('success');
            console.log('success');
            self.onFinished(a);
          }
          else
            console.log('Still not finished');
        }
      });



      /*var url = $.post(
          A.getApiUrl()+'/analysis_tracks/'
        ,data,function(a,b,c) {
        //console.log('Ok donc on fait quoi ?');

        if (a.result_url && a.result_url.indexOf('http://')===0) {
          //alert('success');
          console.log('success');
          self.onFinished(a);
        }
        else
          console.log('Still not finished');
      });*/
    };


    //here, result is a js obj following analysis_track object
    this.onFinished = function(result) {
      clearInterval(this.interval);
      var resultModel = new A.models.resultAnalysis(result);
      resultModel.set('uniqueIDForView',this.uniqueIdAnalysis),

      A._v.trigCfg('analysis.result','',resultModel);
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
    //Delete
    deleteAnalysisTrack:function(model,callback) {

      //note : we don't delete anything anymore, asked by TF 08/02/17
      return callback();

      return $.ajax({
          url : /*'http://timeside-dev.telemeta.org/timeside/api/analysis_tracks/'*/
          A.getApiUrl()+'/analysis_tracks/'
            +model.get('uuid'),
          headers : {"X-CSRFToken" : A.injector.get(A.injector.cfg.csrfToken)},
          /*headers : {
              "Authorization" : "Token "+A.injector.get('serverToken')
            },*/
          type : 'DELETE'/*,
          data : data*/,
          success : function(res) {
            return callback();
          }
        });
    },

     //////////////////////////////////////////////////////////////////////////////////////////////
    //Update parameters of analysis

    //1 -- Post on analysis
    updateParametersOnAnalysisTrack:function(parameters,uuid,callback) {




      var dataJsonCall = "{";
      _.each(_.keys(parameters),function(_key,i) {
        dataJsonCall+='"'+_key+'" : '+parameters[_key]+(i==_.keys(parameters).length-1 ? "" : ",");
      });
      dataJsonCall+="}";

      var self=this;
      var _intervalSetParameters = setInterval(function() {
        $.ajax({
          url:A.getApiUrl()+'/analysis_tracks/'+uuid+'/set_parameters/',
          type:"POST",
          data:dataJsonCall,
          headers : {"X-CSRFToken" : A.injector.get(A.injector.cfg.csrfToken)},
           /*headers : {
              "Authorization" : "Token "+A.injector.get('serverToken')
            },*/
          contentType:"application/json; charset=utf-8",
          dataType:"json",
          success: function(res){
            if (res.result_url && res.result_url.indexOf('http')>=0) {
              alert('something happened!');
            }
            console.log('receiving : '+JSON.stringify(res));
          }
        });
      },1000);


      

    },

    //////////////////////////////////////////////////////////////////////////////////////////////
    //
    onAskAnalysis:function(analysis) {

      var scopeAsk = new analysisAsked(analysis,A._i.getOnCfg('currentItem'));
      scopeAsk.launch();

    },


    

  

   

  });
});
