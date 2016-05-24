define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  var success = function (data, res) {
    A.vent.trigger(A.Cfg.eventApiOk(A.Cfg.events.init.dataRef),res.body);
  };

  var error = function (res) {
    A.vent.trigger(A.Cfg.eventApiError(A.Cfg.events.init.dataRef),res.body);
  };

  return function (data) {

    return A.injector.get('api').dataref()
      .on('success', function (res) { success(data, res); })
      .on('error', error);
  };
});
