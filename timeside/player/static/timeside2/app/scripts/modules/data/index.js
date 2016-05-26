define([
  '#qt_core/controllers/all',
  './controllers/data',

  './commands/commands_processors'
],

function (A,Controller,
		ProcessorCommands) {
  'use strict';

  return function (options) {
    this.controller = new Controller({
      
    });
    
   	A.DataCommandHelper.createCommands(ProcessorCommands);
  };

});
