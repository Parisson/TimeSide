define([
  'backbone.associations',
  'injector'
],

/**
  Note de l'application class
**/
function (Backbone,injector) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      login:'',
      password : ''

    },

    relations: [
     
    ]

  });
});
