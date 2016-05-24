define([
  'backbone.associations',
  'injector',
  './camion'
],

/**
  Transporteur class
**/
function (Backbone,injector,CamionModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      nom : '',
      codeSAP : '',
      camions : []

    },

    relations: [
      {
        type: Backbone.Many,
        key: 'camions',
        relatedModel: CamionModel
      }
    ],

    fromServer : function() {
      if (this.get('famillesProduit'))
        this.get('camions').each(function(camion) {camion.fromServer();});

      if (this.get('codeSap'))
        this.set('codeSAP',this.get('codeSap'));
    }

  });
});
