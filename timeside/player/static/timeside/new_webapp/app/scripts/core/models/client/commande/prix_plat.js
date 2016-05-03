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
      prix : 0
    },

    relations: [],

    //////////////////////////////////////////
    initFromServer:function() {
      if (this.get('label')) 
        this.set('titre',this.get('label'));
    }

  });
});
