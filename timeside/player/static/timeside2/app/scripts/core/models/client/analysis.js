define([
  'backbone.associations',
  '../qt_basemodel'
],

function (Backbone,BaseModel) {

  'use strict';

  return BaseModel.extend({
    defaults: {
      url : '',
      uuid : '',
      title : '',
      preset : '', //url du preset
      sub_processor : '', //url du subprocessor
      parameters_schema : '' //schema des paramètres  
    },

    relations: [],

    //////////////////////////////////////////

  });
});
