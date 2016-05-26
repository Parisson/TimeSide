define([
  'injector',
  'vent'
],

function (injector, vent) {
  'use strict';

  var success = function (data, res) {

  };

  var error = function (res) {
    
  };

  return function (data) {
    
    return injector.get('api').register(createdUserSend)
      .on('success', function (res) { success(data, res); })
      .on('error', error);
  };
});
