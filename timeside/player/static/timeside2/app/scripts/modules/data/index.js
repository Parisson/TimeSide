define([
  '#qt_core/controllers/all',
  './controllers/data',
  './controllers/true_server',
  './controllers/annotation',


  './commands/commands_processors',
  './commands/commands_items',
  './commands/commands_analysis',

  './commands/get_waveform'
],

function (A,Controller,TrueServerController,AnnotationController,
		ProcessorCommands,ItemCommands,AnalysisCommand,GetWaveformCommand) {
  'use strict';

  return function (options) {
    this.controller = new Controller({
      
    });

    this.trueServerController = new TrueServerController();
    this.annotationController = new AnnotationController();
    
   	A.DataCommandHelper.createCommands(ProcessorCommands);
    A.DataCommandHelper.createCommands(ItemCommands);
    A.DataCommandHelper.createCommands(AnalysisCommand);

   A.injector.get('commando.pool')
      .addCommand(A.Cfg.eventApi(A.Cfg.events.data.items.waveform), GetWaveformCommand);
  };

});
