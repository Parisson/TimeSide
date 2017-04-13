define([
  './controllers/navigation',
  './controllers/popup',
  './commands/index',
  '#qt_core/controllers/all',
  'injector'
],

function (NavigationController,PopupController,commands,A,injector) {
  'use strict';

  return function (options) {
    this.controller = new NavigationController({
      application: options ? options.application : undefined
    });

    this.popupController = new PopupController({
      application: options ? options.application : undefined
    });

    A._i.setOnCfg('navigationController',this.controller);


    injector.get('commando.pool');

  };

});
