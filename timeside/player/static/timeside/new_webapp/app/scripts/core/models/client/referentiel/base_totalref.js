define([
  'backbone.associations',
  'injector'
],

/**
  Base class for total referentiel model
  type can change and can be : TypeClient, Localite, Devise, FamilleProduit, UniteProduit
**/
function (Backbone,injector) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      nom:{},
      detail:{},
      type : ''
    },

    relations: [
    
    ]

  });
});
