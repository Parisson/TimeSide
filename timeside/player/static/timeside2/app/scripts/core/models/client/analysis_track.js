define([
  'backbone.associations',
  '../qt_basemodel'
],

function (Backbone,BaseModel) {

  'use strict';

  return BaseModel.extend({
    defaults: {
      analysis : '', //url*
      item : '', 
      url : '',
      result_url : '',
      uuid : ''
    },

    relations: [],

    //////////////////////////////////////////

  });
});
