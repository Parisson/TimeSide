define([
  'marionette',
  './controllers/session',
  './controllers/user.auth',
  './routers/user.auth',
  './controllers/user.anonymous',
  './routers/user.anonymous',
  'injector',
  './commands/index',
  '#qt_core/controllers/config'
],

function (Marionette, SessionController, AuthUserController, AuthUserRouter, AnonUserController, AnonUserRouter, 
  injector, commands,Cfg) {
  return function (options) {
    this.authRouter = new AuthUserRouter({
      controller: new AuthUserController()
    });

    this.anonRouter = new AnonUserRouter({
      controller: new AnonUserController()
    });

    injector.get('commando.pool')
      .addCommand(Cfg.eventApi(Cfg.events.auth.login), commands.login)
      .addCommand(Cfg.eventApi(Cfg.events.auth.logout), commands.logout)
      .addCommand(Cfg.eventApi(Cfg.events.init.loginForHeader), commands.loginForHeader)
      .addCommand(Cfg.eventApi(Cfg.events.users.me),commands.me)
      .addCommand(Cfg.eventApi(Cfg.events.auth.ask_resetPassword), commands.askResetPassword)
      .addCommand(Cfg.eventApi(Cfg.events.auth.changePassword),commands.changePassword);
      

      /*.addCommand('user:api:session', commands.me)
      
      .addCommand('auth:api:logout', commands.logout)
      .addCommand('user:api:register', commands.register)
      .addCommand('auth:api:confirm', commands.confirm)
      .addCommand('auth:api:resetpassword', commands.resetPassword)
      .addCommand('auth:api:askresetpassword', commands.askResetPassword)
      .addCommand('user:api:edit', commands.edit)
      .addCommand('auth:api:checkemail',commands.checkEmail)
      .addCommand('auth:api:askreset',commands.askResetPassword)
      .addCommand('user:api:getinfo',commands.getUserInfo);*/

    // session controller must be initialized after commands setup
    this.session = new SessionController();
  };
});
