define([
  'backbone.associations',
  'injector',
  '../referentiel/base_totalref'
],

/**
  Position Camion class
**/
function (Backbone,injector,Cfg,RefModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      date : 0,
      long : 0,
      latt : 0
    },

    relations: [
      
    ]

  });
});
