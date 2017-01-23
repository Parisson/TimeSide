define([
  'injector',
  'vent',
  '#qt_core/controllers/all',
  '#qt_core/controllers/config',
  'core/models/index'
],

/**
  CSRF Test
**/
function (injector, vent,A,Cfg,Models) {
  'use strict';

  var dataLogin;

  var success = function (res) {
    console.log("Success");
    A.vent.trigger(A.Cfg.eventApiOk(A.Cfg.events.init.loginForHeader));
  };

  var error = function (res) {
    console.log("error");
    A.vent.trigger(A.Cfg.eventApiError(A.Cfg.events.init.loginForHeader));
  };

  return function (data) {
    return injector.get('api').loginForHeader()
      .on('success', success)
      .on('error', error);
  };
});
