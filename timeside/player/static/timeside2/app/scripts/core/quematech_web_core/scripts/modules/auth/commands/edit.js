define([
  'injector',
  'vent',
  'underscore'
],

function (injector, vent, _,messages,UserModel) {
  'use strict';

  var success = function (data, res) {
    
  };

  var error = function (res) {
    
  };

  return function (data) {
    
    return injector.get('api').edituser(data)
      .on('success', function (res) { success(data, res); })
      .on('error', error);
  };
});
