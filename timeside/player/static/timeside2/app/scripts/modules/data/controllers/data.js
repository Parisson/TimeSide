define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      /*A.vent.on(A.Cfg.events.livraison.transporteur.get,this.onGetTransporteurData,this);*/

      A._v.onCfg('data.items.get','',this.onGetItems,this);
      A._v.onCfg('data.items.getOne','',this.onGetOneItem,this);
    },

    onDestroy : function() {
      /*A.vent.off(A.Cfg.events.livraison.transporteur.get,this.onGetTransporteurData,this);*/


      A._v.offCfg('data.items.get','',this.onGetItems,this);
      A._v.offCfg('data.items.getOne','',this.onGetOneItem,this);
     
    },

    /////////////////////////////////////////////////////////////////////
    // Get Items

    onGetItems:function() {
       A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.items.get),null,null,
        function(result) {
          //alert('oui');
          A._i.setOnCfg('allItems',result);
          return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.data.items.get));
        }, function(error) {
          alert("Non1");
      });
    },

     /////////////////////////////////////////////////////////////////////
    // Get One Item & nivigate to view
    onGetOneItem:function(id,viewid) {

      ///NEW : get item for direct call
       var self=this;
      A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.items.getOne),{id : id},null,
        function(item) {
          A._i.setOnCfg('currentItem',item);

          //NEW 02/17 : we dont call the analysis track objects
          return self.getAllAnotationsTracks(item,function(result) {
              item.set('annotationTracksObjects',result);
              return A._v.trigCfg('navigate.page','',viewid);
            });

          /*return self.getAllAnalysisTracks(item,function(resultAnalysis) {
            item.set('analysisTracksObjects',resultAnalysis);
             //new : get all annotations on item
            return self.getAllAnotationsTracks(item,function(result) {
              item.set('annotationTracksObjects',result);
              return A._v.trigCfg('navigate.page','',viewid);
            });

          })*/
        }, function(error) {
          alert("Non1");
      });
      return;
      
    },

    //get all analysis tracks
    getAllAnalysisTracks:function(item,callback) {
        var indexAnalysis = 0;
        var result = [];

        if ( (!item.get('analysis_tracks')) || item.get('analysis_tracks').length==0 )
          return callback();

        var getNewAnalysis = function() {
          if (indexAnalysis>=12) {
            console.error('tmp debug, 6 analysis track limit')
            return callback(result);
          }

          if (indexAnalysis >= item.get('analysis_tracks').length)
            return callback(result);

          var urlAnnotation = item.get('analysis_tracks')[indexAnalysis];

          $.ajax({
            type : "get",
            url : urlAnnotation,
            headers : {"X-CSRFToken" : A.injector.get(A.injector.cfg.csrfToken)},
            /*headers : {
              "Authorization" : "Token "+A.injector.get('serverToken')
            },*/
            success : function(res) {
              result.push(res);
              indexAnalysis++;
              return getNewAnalysis();
            }
          });

          /*$.get(urlAnnotation,function(res) {
              result.push(res);
              indexAnalysis++;
              return getNewAnalysis();
          });*/
        };

        return getNewAnalysis();  

    },

    //get all annotations tracks
    getAllAnotationsTracks:function(item,callback) {
        var indexCurrentAnnotation = 0;
        var result = [];

        if ( (!item.get('annotation_tracks')) || item.get('annotation_tracks').length==0 )
          return callback();

        var getNewAnnotation = function() {
          if (indexCurrentAnnotation >= item.get('annotation_tracks').length)
            return callback(result);

          var urlAnnotation = item.get('annotation_tracks')[indexCurrentAnnotation];


          $.ajax({
            url : urlAnnotation,
            type : "get",
            headers : {"X-CSRFToken" : A.injector.get(A.injector.cfg.csrfToken)},
            /*headers : {
              "Authorization" : "Token "+A.injector.get('serverToken')
            },*/
            success : function(res) {
              result.push(res);
              indexCurrentAnnotation++;
              return getNewAnnotation();
            }
          });
          /*$.get(urlAnnotation,function(res) {
              result.push(res);
              indexCurrentAnnotation++;
              return getNewAnnotation();
          });*/ 
        };

        return getNewAnnotation();  

    }   


  

   

  });
});
