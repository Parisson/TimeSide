define([
  'injector',
  'vent',
  '#qt_core/controllers/all'
],

function (injector, vent, A) {
  'use strict';

  var success = function (res) {
    A.vent.trigger('popup:forceclose');
    A.vent.trigger(A.Cfg.events.ui.notification.show,{type : 'info', text : "La demande a été prise en compte. Vous recevrez un email à l'adresse liée à ce compte utilisateur dans les prochains instants"});
  };

  var error = function (res) {
    
  };

  return function (data) {
    return injector.get('api').askReset({username: data.username})
      .on('success', success)
      .on('error', error);
  };
});
