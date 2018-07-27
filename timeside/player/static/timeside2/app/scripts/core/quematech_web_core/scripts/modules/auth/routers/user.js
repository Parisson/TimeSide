define([
  'marionette',
  './user.anonymous',
  './user.auth'
],

function (Marionette, AnonRouter, AuthRouter) {
  'use strict';

  return Marionette.AppRouter.extend({
    bindAnonRoutes: function (controller) {
      this.processAppRoutes(controller, AnonRouter.prototype.appRoutes);
    },

    unbindAnonRoutes: function () {
      console.log(AnonRouter.prototype.appRoutes);
    },

    bindAuthRoutes: function (controller) {
      console.log(AuthRouter.prototype.appRoutes);
      this.processAppRoutes(controller, AuthRouter.prototype.appRoutes);
    },

    unbindAuthRoutes: function () {
      console.log(AuthRouter.prototype.appRoutes);
    },
  });
})
