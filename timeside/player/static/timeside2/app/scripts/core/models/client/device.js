define([
  'backbone.associations',
  './restaurant'
],

function (Backbone,RestaurantModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({
    defaults: {
      id : 0,
      hardwareId : '',
      idTable : '',
      restaurant : null
    },

    relations: [{
      type: Backbone.One,
      key: 'restaurant',
      relatedModel: RestaurantModel
    }],
    //////////////////////////////////////////
    hasRestaurant : function() {
      return this.get('restaurant')!==null && this.get('restaurant')!==undefined && this.get('restaurant').get('id')
        && this.get('restaurant').get('id')>0;
    },

    hasNumTable : function() {
      return this.get('idTable') && this.get('idTable').length>0;
    }


  });
});
