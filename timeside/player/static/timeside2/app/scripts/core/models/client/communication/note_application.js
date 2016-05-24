define([
  'backbone.associations',
  'injector',
  '../user'
],

/**
  Note de l'application class
**/
function (Backbone,injector,User) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      date : 0,
      note : 0, //int in [0,5]
      user : null,
      detail: ''

    },

    relations: [
      {
        type: Backbone.One,
        key: 'users',
        relatedModel: User
      }
    ]

  });
});
