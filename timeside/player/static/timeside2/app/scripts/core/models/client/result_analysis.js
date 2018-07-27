define([
  'backbone.associations',
  '../qt_basemodel'
],

function (Backbone,BaseModel) {

  'use strict';

  return BaseModel.extend({
    defaults: {
      analysis : '', //URL
      item : '', //URL
      result_url : '', //URL
      url : '', //url
      uuid : '' //U ID
    },

    relations: [],

    //////////////////////////////////////////

  });
});
