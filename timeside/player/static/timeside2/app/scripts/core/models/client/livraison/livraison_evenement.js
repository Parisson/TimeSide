define([
  'backbone.associations',
  'injector',
  '../referentiel/base_totalref'
],

/**
  Livraison Evenement class
**/
function (Backbone,injector,Cfg,RefModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      date : 0,
      type : '', //enum
      detail : ''
    },

    relations: [
      
    ]

  });
});
