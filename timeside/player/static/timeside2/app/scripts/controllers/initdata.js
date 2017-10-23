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

      


      return A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.analysis.get),null,null,
            function(result) {
              A._i.setOnCfg('allAnalysis',result);

              //avons-nous récupéré un token CSRF ? Si oui, on est content, sinon, on fait l'appel dédié
              if(A.injector.get(A.injector.cfg.csrfToken)) {
                return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));
              }
              else {
                $.ajax({url :  A.getApiUrl()+'/token-csrf/',
                  error : function(error) {
                    console.error('error on get token : '+error);
                  },
                  success : function(a) {
                    if (a && a.csrftoken) {
                      A.injector.set(A.injector.cfg.csrfToken,a.csrftoken);
                      return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));
                    }

                    console.log('error in success function get csrf token');
                    console.dir(a);
                  }
                });
              }
            }, function(error) {
              alert("Non1");
          });

      return; // temp

    }

    
  });

  return InitDataController;
});
