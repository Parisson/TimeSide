define([
  'json!#config/events.json',
  'json!#config/views.json',
  '#qt_core/controllers/config'
],

function (eventsConfig,viewsConfig,Cfg) {
  'use strict';

  /**
    * view id names from views.json
    * factory called by navigation controller
    * Ce prototype renvoie les events à émettre et à attendre pour changer de vue, s'il y en a
    **/


  var factory = function () {
    
  };


  factory.prototype = {

    getEventAndBackEvent: function (view) {

      var idView = view.viewid;
      var createBackFromEventObj = function(eventSubObj) {
        return {
            "event" : eventSubObj.ask,
            "ok" : eventSubObj.ok,
            "error" : eventSubObj.error
          };
      };

      //new!
      if (view.baseEvent && view.baseEvent.length>0) {
        return {
          "event" : view.baseEvent,
          "ok" : Cfg.eventOk(view.baseEvent),
          "error" : Cfg.eventError(view.baseEvent)
        };
      }


      switch (idView) {
        /*case viewsConfig.qeopa.home.viewid : 
          return createBackFromEventObj(eventsConfig.data.questions.getlist);
          break; */
       

        default : 
          return undefined;  
      }
    }
  };


  return new factory();
});
