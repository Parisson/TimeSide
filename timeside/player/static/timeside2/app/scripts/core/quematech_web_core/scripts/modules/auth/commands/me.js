define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  var success = function (res) {
    var user = new A.modelsClient.user(res.body);
    user.fromServer();

    if (user.get('role')==='CLIENT') {
      //un client ne se connecte pas au BO....
      return A.vent.trigger(A.Cfg.eventApi(A.Cfg.events.auth.logout));
    }


    A.injector.set(A.injector.cfg.currentUser,user);
    A.vent.trigger(A.Cfg.eventApiOk(A.Cfg.events.users.me));
  };

  var error = function (res) {
    A.vent.trigger(A.Cfg.eventApiError(A.Cfg.events.users.me));
  };

  return function () {
    return A.injector.get('api').me()
      .on('success', success)
      .on('error', error);
  };
});
