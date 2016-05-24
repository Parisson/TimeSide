define([
  'backbone.associations',
  'injector',
  './zone_commerciale',
  '../referentiel/base_totalref',
  '../user',
  '../livraison/depot'
],

/**
  Client class
**/
function (Backbone,injector,ZoneCommerciale,DataRef,User,Depot) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      user : null,
      type : null, //enum
      isMale : null,
      /*responsable:null, //user responsable & linked to zone commerciale*/
      zoneCommerciale : null, //zone contenant le client
      depotHabituel : null, //depot source habituel pour ce client 
      codeSAP : '',
      nom:'',
      nomContact : '',
      telFixe : '',
      telMobile : '',
      adresse : '',
      localite : null,
      email : '',
      longitude : 0,
      lattitude : 0

    },

    relations: [
      {
        type: Backbone.One,
        key: 'user',
        relatedModel: User
      },
      {
        type: Backbone.One,
        key: 'zoneCommerciale',
        relatedModel: ZoneCommerciale
      },
      {
        type: Backbone.One,
        key: 'localite',
        relatedModel: DataRef
      },
      {
        type: Backbone.One,
        key: 'type',
        relatedModel: DataRef
      },
      {
        type: Backbone.One,
        key: 'depotHabituel',
        relatedModel: Depot
      }
    ],

    //////////////////////
    translate:function(from,to) {
      if (this.get(from))
        this.set(to,this.get(from));
    },

    convertSub:function(attrib) {
      if (this.get(attrib) && this.get(attrib).fromServer)
        this.get(attrib).fromServer();
    },

    fromServer:function() {
      this.translate('male','isMale');
      this.translate('lat','lattitude');
      this.translate('lng','longitude');
      this.translate('typeClient','type');



      this.convertSub('user');
      this.convertSub('zoneCommerciale');
      this.convertSub('localite');
      this.convertSub('type');
    }

  });
});
