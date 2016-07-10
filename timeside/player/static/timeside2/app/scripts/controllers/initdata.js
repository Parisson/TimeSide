define([
  'backbone',
  'marionette',
  '#qt_core/controllers/all',
  'json!#config/fake/fakedata_bo.json'
],

function (Backbone, Marionette, A,FakeData) {
  'use strict';

  var InitDataController = Marionette.Controller.extend({
    initialize: function (options) {
      A.vent.on(A.Cfg.events.init.start,this.onInitStart,this);
      this.initDataDone = false;
    },

    onClose: function () {
     vent.off(A.Cfg.events.init.start,this.onInitStart,this);
    },


    ////////////////////////////////////////////////////////////
    //#1 : start init ref : Pas de CSRF
    onInitStart:function() {

      
      //console.error('Tmp : no CSRF!');
       //return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));

      //#1 Load all processors
     /* A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.processors.get),null,null,
        function(result) {
          A._i.setOnCfg('allProcessors',result);
          return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));
        }, function(error) {
          alert("Non1");
      });*/


       A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.analysis.get),null,null,
        function(result) {
          A._i.setOnCfg('allAnalysis',result);
          return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));
        }, function(error) {
          alert("Non1");
      });



    }

    
  });

  return InitDataController;
});
