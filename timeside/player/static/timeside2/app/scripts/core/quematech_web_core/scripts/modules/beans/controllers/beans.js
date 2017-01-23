define([
  'marionette',
  'injector'
],

function (Marionette, injector) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options) {
      injector.set(injector.config.beanController,this);

      //  vent.on('initdata:end',this.onDataInitOk,this);
    },

    onClose: function () {
      //vent.off('initdata:end',this.onDataInitOk,this);
    },


   

  });
});
