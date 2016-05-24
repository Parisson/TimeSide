define([
  'backbone.associations',
  'injector'
],

/**
  Client class
**/
function (Backbone,injector) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      nom : {}, //nom
      codeSAP:''

    },

    relations: [
      //depends on server data
    ],
    fromServer : function() {
      
    }

  });
});
