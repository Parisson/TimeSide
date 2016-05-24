define([
  'backbone.associations',
  'injector',
  './type_message',
  '../user'
],

/**
  Note de l'application class
**/
function (Backbone,injector,TypeMessageModel,UserModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id : 0,
      type : null,
      date : 0,
      auteur : null,
      destinataire : null,
      titre : '',
      texte : '',
      read : false


    },

    relations: [
     {
        type: Backbone.One,
        key: 'type',
        relatedModel: TypeMessageModel
      },
      {
        type: Backbone.One,
        key: 'auteur',
        relatedModel: UserModel
      },
      {
        type: Backbone.One,
        key: 'destinataire',
        relatedModel: UserModel
      }
    ]

  });
});
