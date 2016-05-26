define([
  '#qt_core/controllers/all',
  './controllers/data',

  './commands/commands_processors',
  './commands/commands_items'
],

function (A,Controller,
		ProcessorCommands,ItemCommands) {
  'use strict';

  return function (options) {
    this.controller = new Controller({
      
    });
    
   	A.DataCommandHelper.createCommands(ProcessorCommands);
    A.DataCommandHelper.createCommands(ItemCommands);
  };

});
