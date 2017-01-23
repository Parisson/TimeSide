define([
  'injector',
  'vent'
],

function (injector, vent) {
  'use strict';

  var success = function (res) {
    
  };

  var error = function (res) {
   
  };

  return function (token) {
    return injector.get('api').confirmuser({token: token})
      .on('success', success)
      .on('error', error);
  };
});
