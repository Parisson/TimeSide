define([
  'backbone.associations',
  '../qt_basemodel'
],

function (Backbone,BaseModel) {

  'use strict';

  return BaseModel.extend({
    defaults: {
      annotations : [],
      author : '',
      description : '',
      is_public : true,
      item : '', 
      overlapping : false,
      title : '',
      url : '',
      uuid : ''
    },

    relations: [],

    //////////////////////////////////////////

  });
});
