define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  

  var success = function (res) {
    
  };

  var error = function (res) {
     
  };

  return function (data) {

    var itemId = data.itemId;delete data.itemId;
    data.format = 'json'; 

    return A.injector.get('api').getWaveform(data,{id : itemId})
      .on('success', success)
      .on('error', error);
  };
});
