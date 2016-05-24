define([
  'backbone.associations',
  'injector',
  '../user'
],

/**
  Type Message class
**/
function (Backbone,injector,User) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      label : '', //nom
      users : [],
      role: '' //SOIT le role soit les users

    },

    relations: [
      {
        type: Backbone.Many,
        key: 'users',
        relatedModel: User
      }
    ],
    fromServer:function() {
      if (this.get('role'))
        this.set('role',this.roleFromServer(this.get('role')));
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

  });
});
