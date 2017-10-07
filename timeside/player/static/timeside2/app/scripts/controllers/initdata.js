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

      var data = {
        username : "quematech",
        password : "quimitich"
      }, self=this;


      var url = $.post(/*'http://timeside-dev.telemeta.org/timeside/api/analysis_tracks/'*/
          A.getApiUrl()+'/token-auth/'
        ,data,function(a,b,c) {

        if (a.token) {

          var apiController = A.injector.get(A.injector.cfg.apiController);
          apiController.removeHeader("X-CSRFToken");
          apiController.addHeader("X-CSRFToken",a.token);
          apiController.addHeader("Authorization","Token "+a.token);

          A.injector.set(A.injector.cfg.serverToken,a.token);

           A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.analysis.get),null,null,
            function(result) {
              A._i.setOnCfg('allAnalysis',result);
              return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));
            }, function(error) {
              alert("Non1");
          });

        }
      });


      return; // temp
      



    }

    
  });

  return InitDataController;
});
