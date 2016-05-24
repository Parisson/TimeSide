define([
  'backbone.associations',
  '../../qeopa_basemodel',
  '../commande/menu_selection',
  './plat_commande',
  '#qt_core/controllers/config'
],

function (Backbone,QeopaBaseModel,MenuSelectionModel,PlatCommandeModel,Cfg) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      selection : null,
      platCommande : null,
      total : 0,

      //dynamic
      subLabel : ''
    },

    relations: [ {
      type: Backbone.One,
      key: 'platCommande',
      relatedModel: PlatCommandeModel
    },
    {
      type: Backbone.One,
      key: 'selection',
      relatedModel: MenuSelectionModel
    }

    ],

    ///////
   

    ///////////////////////////////////////////////////////////
    //update datas
    updateAttribs:function() {
      var _total = 0;
      var _sublabel="";
      if (this.get('platCommande')) {
        this.get('platCommande').updateAttribs();
        _sublabel = this.get('platCommande').get('label');
      }
      this.set('subLabel',_sublabel);
      return this.set('total',_total);
    }


  });
});
