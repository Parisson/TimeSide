define([
  'backbone.associations',
  '../../qeopa_basemodel'
],

function (Backbone,QeopaBaseModel) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      type : '',
      titre : {},
      deltaPrix : 0
    },

    relations: [],

    //////////////////////////////////////////

  });
});
