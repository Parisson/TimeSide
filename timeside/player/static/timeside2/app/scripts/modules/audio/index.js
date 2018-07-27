define([
  '#qt_core/controllers/all',
  './controllers/audio',
  './controllers/audio_webapi',
],

function (A,Controller,WebApiController) {
  'use strict';

  return function (options) {
    this.controller = new Controller({
      
    });

    this.webApiController = new WebApiController();
    
   
  };

});
