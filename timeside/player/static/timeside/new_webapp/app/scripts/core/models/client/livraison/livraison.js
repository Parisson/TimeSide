define([
  'backbone.associations',
  'injector',
  './camion',
  './arret_livraison',
  './position_camion',
  './livraison_evenement',
  '../referentiel/base_totalref',
  './depot'
],

/**
  Livraison class
**/
function (Backbone,injector,CamionModel,ArretLivraisonModel,PositionCamionModel,LivraisonEvenementModel,RefModel,DepotModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      statut : '', //enum
      numeroTransport : '',
      datePrevue : 0, //date d'importation / création
      departDepart : 0, //date de départ
      dateFin : 0, //date de fin de livraison
      camion : null,
      depot : null,
      arretLivraisonClient : null, //specific client-side object

      arretsLivraison : [], //not in front client side object
      positions : [], //not in front client side object
      events : [], //not in front client side object
      fiabilite : 0, //not in front client side object


    },

    relations: [
      {
        type: Backbone.One,
        key: 'camion',
        relatedModel: CamionModel
      },
      {
        type: Backbone.One,
        key: 'depot',
        relatedModel: DepotModel
      },
      {
        type: Backbone.One,
        key: 'arretLivraisonClient',
        relatedModel: ArretLivraisonModel
      },
      {
        type: Backbone.Many,
        key: 'arretsLivraison',
        relatedModel: ArretLivraisonModel
      },
      {
        type: Backbone.Many,
        key: 'positions',
        relatedModel: PositionCamionModel
      },
      {
        type: Backbone.Many,
        key: 'events',
        relatedModel: LivraisonEvenementModel
      }
    ],

    fromServer:function() {
      if (this.get('arrets')) {
        this.set('arretsLivraison',this.get('arrets'));
        var _fakeid=1;
        this.get('arretsLivraison').each(function(_arretLivraison) {
          _arretLivraison.set('id','FAKEFROMSERV_'+_fakeid);
          _fakeid++;
          _arretLivraison.fromServer();
        });
      }
    },

    getDisplayStartDate:function() {
      if (this.get('dateDepart') && this.get('dateDepart')>0)
        return this.get('dateDepart');
      return 0;
    },

    getDisplayDepartHeure:function() {
      return this.get('arretLivraisonClient') ? this.get('arretLivraisonClient').get('heureDepart') : 0;
    },

    getDisplayArriveeHeure:function() {
      if (['IMPORTEE','CREEE','EDITEE'].indexOf(this.statut)>0)
        return '';
      if (this.get('arretLivraisonClient') && this.get('arretLivraisonClient').get('statut')==="FINIE")
        return this.get('arretLivraisonClient').get('heureFin');

      return this.get('arretLivraisonClient').get('heureEstimee');
    },

  });
});
