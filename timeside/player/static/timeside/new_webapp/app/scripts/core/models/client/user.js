define([
  'backbone.associations',
  'injector',
  './client/zone_commerciale',
  './livraison/depot'
],

function (Backbone,injector,ZoneCommercialeModel,DepotModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      email:'',
      password:'',
      role:null,
      lastConnexion : null,
      enabled : false,

      num : '',
      /*client : null,*/
      zoneCommerciale : null,
      depot : null,
      creationDate : 0,
      telephone : '',
      username : ''

    },

    relations: [
      /*{
        type: Backbone.One,
        key: 'client',
        relatedModel: ClientModel
      },*/
      {
        type: Backbone.One,
        key: 'zoneCommerciale',
        relatedModel: ZoneCommercialeModel
      },
      {
        type: Backbone.One,
        key: 'depot',
        relatedModel: DepotModel
      }
    ],
    //////////////////////////////////////////////////////
    fromServer:function() {
      if (this.get('lastConnect'))
        this.set('lastConnexion',this.get('lastConnect'));

      if (this.get('role'))
        this.set('role',this.roleFromServer(this.get('role')));

      if (this.get('zone')) {
        this.set('zoneCommerciale',this.get('zone'));
        this.get('zoneCommerciale').fromServer();
      }


    },

    roleFromServer:function(_roleIn) {
      if (! _roleIn)
        return console.error('No role for user ? ');
      _roleIn = _roleIn.toUpperCase();
      var mappingFromServer = {
        ROLE_ADMINSI : "ADMIN_SI",
        ROLE_AGENTDEPOT : "AGENT_DEPOT"
      };

      if (mappingFromServer[_roleIn])
        return mappingFromServer[_roleIn];
      else if (_roleIn.indexOf("ROLE_")===0)
        return _roleIn.substr(5);
      else
        return _roleIn;

    },

    //////////////////////////////////////////////////////
    getDetail:function(mainLocale) {
      if (this.get('role')==='ADMIN_SI') {
        return "Administrator"
      }
      if (this.get('role')==='COMMERCIAL') {
        if (! this.get('zoneCommerciale'))
          return "No commercial area";
         if (! this.get('zoneCommerciale').get('nom')[mainLocale])
          return JSON.stringify(this.get('zoneCommerciale').get('nom'));
        return this.get('zoneCommerciale').get('nom')[mainLocale];
      }

      if (this.get('role')==='AGENT_DEPOT') {
         if (! this.get('depot'))
          return "No warehouse";
         if (! this.get('depot').get('designation')[mainLocale])
          return JSON.stringify(this.get('depot').get('designation'));
        return this.get('depot').get('designation')[mainLocale];
      }

      if (this.get('role')==='CLIENT') {
         if (! this.get('client'))
          return "No client";
        return this.get('client').get('nom');
      }
      return "";
    }

  });
});
