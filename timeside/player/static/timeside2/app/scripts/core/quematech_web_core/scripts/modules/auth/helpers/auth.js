define([
  'injector',
  'vent'
],

function (injector, vent) {
  'use strict';

  return {
    isAuth: function () {
      return injector.get('authorized');
    },

    hasAccess: function (trigger) {
      trigger = undefined === trigger ? true : trigger;
      var authorized = injector.get('authorized');

      trigger && !authorized && vent.trigger('access:denied');

      return authorized;
    },

    getCurrentUser:function() {
      return injector.get('user');
    }
  };
});
