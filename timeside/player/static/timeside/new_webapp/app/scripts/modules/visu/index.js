define([
  '#qt_core/controllers/all',
  './controllers/fake_server',
  './controllers/track_info',
  './controllers/loader'
],

function (A,Controller,TrackInfoController,LoaderController) {
  'use strict';

  return function (options) {
    this.controller = new Controller({
      
    });

    this.trackInfoController = new TrackInfoController();
    this.loaderController = new LoaderController();
    
   
  };

});
