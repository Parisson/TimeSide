define([
  'backbone.associations',
  'injector',
  './produit'
],

/**
  Camion class
**/
function (Backbone,injector,ProduitModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      produit : null,
      quantite : 0


    },

    relations: [
      {
        type: Backbone.One,
        key: 'produit',
        relatedModel: ProduitModel
      }
    ]

  });
});
