define([
  'backbone.associations',
  'injector',
  '../referentiel/base_totalref',
  './contenu_livraison',
  '../client/client'

],

/**
  ArretLivraison class
**/
function (Backbone,injector,RefModel,ContenuModel,ClientModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      statut : '',
      numeroLivraison : '',

      contenu : [], //produit class
      client : null, //client class, not in client-side front object
      localite : null,/*,
      quantite : 0,*/
      ordre : 0,
      heureDepart : 0,
      heureEstimee : 0,
      heureFin : 0


    },

    relations: [
      {
        type: Backbone.One,
        key: 'localite',
        relatedModel: RefModel
      },
      {
        type: Backbone.One,
        key: 'client',
        relatedModel: ClientModel
      },
      {
        type: Backbone.Many,
        key: 'contenu',
        relatedModel: ContenuModel
      }
    ],

    fromServer:function() {
      if (this.get('quantites'))
        this.set('contenu',this.get('quantites'));

      var _fakeid=1;
      this.get('contenu').each(function(_content) {
        _content.set('id','FAKEFROMSERV_'+_fakeid);
        _fakeid++;
      }); 
    }

  });
});
