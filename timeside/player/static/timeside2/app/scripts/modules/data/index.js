define([
  '#qt_core/controllers/all',
  './controllers/data',
  './controllers/true_server',


  './commands/commands_processors',
  './commands/commands_items',

  './commands/get_waveform'
],

function (A,Controller,TrueServerController,
		ProcessorCommands,ItemCommands,GetWaveformCommand) {
  'use strict';

  return function (options) {
    this.controller = new Controller({
      
    });

    this.trueServerController = new TrueServerController();
    
   	A.DataCommandHelper.createCommands(ProcessorCommands);
    A.DataCommandHelper.createCommands(ItemCommands);

   A.injector.get('commando.pool')
      .addCommand(A.Cfg.eventApi(A.Cfg.events.data.items.waveform), GetWaveformCommand);
  };

});
