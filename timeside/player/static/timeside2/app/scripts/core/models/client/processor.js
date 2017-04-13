define([
  'backbone.associations',
  '../qt_basemodel'
],

function (Backbone,BaseModel) {

  'use strict';

  return BaseModel.extend({
    defaults: {
      pid : '',
      version : '',
      url : ''
    },

    relations: [],

    //////////////////////////////////////////

  });
});
