define([
  '#qt_core/controllers/all'
],

function (A) {
  return Marionette.Controller.extend({
    initialize: function () {
      A.vent.on(A.Cfg.events.auth.login,this.onStartLogin,this);

      
    },

    onClose: function () {
      A.vent.off(A.Cfg.events.auth.login,this.onStartLogin,this);
      

      
    },

    ////////////////////////////////////////////////////////////////////////////////
    // Login
    onStartLogin:function(data) {
      A.ApiEventsHelper.listenOkErrorAndTrigger2(
          A.Cfg.eventApi(A.Cfg.events.auth.login),data,null,function(result) {
            A.vent.trigger('navigate:page',A.Cfg.views.qeopa.home.viewid);
        },function(error) {
            console.log('unknown error');
        },this);
    },


    ////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////
    // USER-CREATON-----------------------------------------------------------------


   
  });
});

