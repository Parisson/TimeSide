define([
  'injector',
  'vent',
  '#qt_core/controllers/all'
],

function (injector, vent, A) {
  'use strict';

  var success = function (res) {
    A.vent.trigger('popup:forceclose');
    A.vent.trigger(A.Cfg.events.ui.notification.show,{type : 'info', text : "Votre mot de passe a été modifié. Merci de vous reconnecter"});
  };

  var error = function (res) {
    
  };

  return function (data) {
    data['token'] = A.injector.get(A.injector.cfg.auth_token_newpassword);
    data['confirmPassword'] = data['confirm_password'];
    delete data['confirm_password'];
    
    return injector.get('api').changePassword(data)
      .on('success', success)
      .on('error', error);
  };
});
