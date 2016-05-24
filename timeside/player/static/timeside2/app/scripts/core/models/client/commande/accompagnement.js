define([
  'backbone.associations',
  '../../qeopa_basemodel'
],

function (Backbone,QeopaBaseModel) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      titre : {},
      description : {},//@TODO
      visuel : '',
      deltaPrix : 0
    },

    relations: [],

    //////////////////////////////////////////

    //////////////////////////////////////////
    //update from server

    initFromServer:function() {
      if (this.get('nom')) 
        this.set('titre',this.get('nom')); 
      if (this.get('supplement')) 
        this.set('deltaPrix',this.get('supplement')); 
    }

  });
});
