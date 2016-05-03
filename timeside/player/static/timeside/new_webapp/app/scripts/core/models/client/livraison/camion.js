define([
  'backbone.associations',
  'injector',
  './depot',
  '../referentiel/base_totalref'
],

/**
  Camion class
**/
function (Backbone,injector,DepotModel,RefModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      codeSAP : '',
      depotAffectation : null,
      famillesProduit : [],
      immatriculation : '',
      capacite : '',
      numBoitier : '',
      transporteur : 0, //TOUJOURS UN ID!!!! (évitons les merdes cycliques)


    },

    relations: [
      {
        type: Backbone.One,
        key: 'depotAffectation',
        relatedModel: DepotModel
      },
      {
        type: Backbone.Many,
        key: 'familleProduit',
        relatedModel: RefModel
      }
    ],

    convertSub:function(attrib) {
      if (this.get(attrib) && this.get(attrib).fromServer)
        this.get(attrib).fromServer();
    },

    fromServer : function() {
      this.convertSub('depotAffectation');

      //@TODO FIXME : là, on a un array d'objet, pas une collection Backbone. Wtf?
      /*if (this.get('famillesProduit')) {
        if (_.isArray(this.get('famillesProduit')))
          _.each(this.get('famillesProduit'),function(famille) {famille.fromServer();});
        else
          this.get('famillesProduit').each(function(famille) {famille.fromServer();});
      }*/
    }

  });
});
