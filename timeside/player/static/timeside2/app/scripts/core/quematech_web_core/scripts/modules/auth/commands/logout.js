define([
  'injector',
  'vent'
],

function (injector, vent) {
  'use strict';

  var success = function (res) {
    window.location = '/';
  };

  var error = function (res) {
    console.log('error - logout');
    window.location = '/';
  };

  return function (token) {
    return injector.get('api').logout()
      .on('success', success)
      .on('error', error);
  };
});
