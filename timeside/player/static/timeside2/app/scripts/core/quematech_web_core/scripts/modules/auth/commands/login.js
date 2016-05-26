define([
  'injector',
  'vent',
  '#qt_core/controllers/config',
  '#qt_core/controllers/all'
],

function (injector, vent,Cfg,A) {
  'use strict';

  var dataLogin;

  var success = function (res) {
    var user = new A.modelsClient.user(res.body);
    user.fromServer();
    injector.set(injector.cfg.currentUser,user);
    vent.trigger(Cfg.eventApiOk(Cfg.events.auth.login));

   
  };

  var error = function (res) {
     vent.trigger(Cfg.events.ui.waiting.stop);
      
     vent.trigger(Cfg.events.ui.notification.show,Cfg.msg.auth.login.error);

     //useful ? no right now.
     vent.trigger(Cfg.eventApiError(Cfg.events.auth.login));
  };

  return function (data) {
   

    return injector.get('api').login(data)
      .on('success', success)
      .on('error', error);
  };
});
