define([
  './controllers/users',
  './commands/commands_user',
  'injector',
  '#qt_core/controllers/config',
  '#qt_core/controllers/all'
],

function (UsersController,UserCommands,injector,Cfg,A) {
  'use strict';

  return function (options) {
    this.controller = new UsersController({
      
    })
    
    A.DataCommandHelper.createCommands(UserCommands);

    /*injector.get('commando.pool')
      .addCommand(Cfg.eventApi(Cfg.events.users.get), commands.getUsers)
      .addCommand(Cfg.eventApi(Cfg.events.users.edit), commands.editUser)
      .addCommand(Cfg.eventApi(Cfg.events.users.create), commands.createUser);*/
  };

});
