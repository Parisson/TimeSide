define([
  'marionette',
  'vent',
  'injector',
  '../helpers/auth'
],

function (Marionette, vent, injector, auth) {
  return Marionette.Controller.extend({
    initialize: function (options) {
      this.region = options.region;
    },

    onDestroy: function () {
     
    },

    ////////////////////////////////////////////////////////////////////////
    // Logout
   
  });
});
