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
    //#1 : start init ref : CSRF
    onInitStart:function() {

      //tmp : pas de CSRF
      console.error('Tmp : no CSRF!');
      return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));

      //#1 : loginref for CSRF
      A.ApiEventsHelper.listenOkErrorAndTrigger(
        A.Cfg.eventApi(A.Cfg.events.init.loginForHeader),null,null,this.onCSRFOk,this.onCSRFError,this);
      //vent.trigger(Cfg.eventOk(Cfg.events.init.start));     
    },

    onCSRFError:function() {
      A.ApiEventsHelper.removeOkError(A.Cfg.eventApi(A.Cfg.events.init.loginForHeader),this.onCSRFOk,this.onCSRFError,this);
      alert("CSRF Error");
    },

    onCSRFOk:function() {
      //#2 : test /me
      A.ApiEventsHelper.removeOkError(A.Cfg.eventApi(A.Cfg.events.init.loginForHeader),this.onCSRFOk,this.onCSRFError,this);

       A.ApiEventsHelper.listenOkErrorAndTrigger2(
        A.Cfg.eventApi(A.Cfg.events.users.me),null,null,function(result) {
          //loggued and youpi
          A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));
        },function(error) {
          //not logued and youpi
          A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.init.start));
        },this);


      //en fait non
      return 

    },



   

    

    
  });

  return InitDataController;
});
