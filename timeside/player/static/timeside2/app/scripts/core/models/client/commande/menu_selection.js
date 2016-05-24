define([
  'backbone.associations',
  '../../qeopa_basemodel',
  './plat'
],

function (Backbone,QeopaBaseModel,PlatModel) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      titre : {},
      plats : [],
      orderInMenu : 0,

      //dynamic
      labelsPlats : []
    },

    relations: [{
      type: Backbone.Many,
      key: 'plats',
      relatedModel: PlatModel
    }],

    //////////////////////////////////////////
    updateAttribs:function() {
      var lbls = [];
      if (this.get('plats')) {
        this.get('plats').each(function(_plat) {
          lbls.push(_plat.getLabelI18N('titre'));
        })
      }
      this.set('labelsPlats',lbls);
    }

  });
});
