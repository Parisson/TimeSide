define([
  'backbone.associations',
  '../../qeopa_basemodel',
  '../commande/menu',
  './menuselection_commande',
  '#qt_core/controllers/config'
],

function (Backbone,QeopaBaseModel,MenuModel,MenuSelectionCommandeModel,Cfg) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      menu : null,
      selectionsCommandees : [],

      //dynamic below
      label : '',
      subLabel : '',
      total : 0

    },

    relations: [ {
      type: Backbone.One,
      key: 'menu',
      relatedModel: MenuModel
    },
    {
      type: Backbone.Many,
      key: 'selectionsCommandees',
      relatedModel: MenuSelectionCommandeModel
    }

    ],

    ///////
   

    ///////////////////////////////////////////////////////////
    //update datas

    //when update for recap_commande
    resetForUpdate:function() {
      this.set('selectionsCommandees',new Backbone.Collection([]));
      this.set('label','x');
      this.set('subLabel','xx');
      this.set('total',0);
    },

    updateAttribs:function(log) {
      var _total = this.get('menu') && this.get('menu').get('prixBase') ? this.get('menu').get('prixBase') : 0;
      if (this.get('selectionsCommandees')) {
        
        this.get('selectionsCommandees').each(function(_selectCommandee) {
          if (log) console.log('    In menuCommande '+this.get('id')+' selectionCommandee : '+_selectCommandee.get('id'));
          _selectCommandee.updateAttribs();
          //_total = _total + _platCommande.get('total');
        },this);
      }
      this.updateLabel();
      this.updateSubLabel();
      return this.set('total',_total);
    },

    updateLabel:function() {
      var _label="";
      if (! this.get('menu'))
        return this.set('label',"");

      this.set('label',this.get('menu').getLabelI18N('titre'));
    },

    //todo after updateAttribs in selections -> platsCommandes
    updateSubLabel:function() {
      var _sublabel="";
      console.log(this.attributes.selectionsCommandees.models);
      if (this.get("selectionsCommandees")) {
        this.get('selectionsCommandees').each(function(_selectCommande) {
            _sublabel = _sublabel+', ' +_selectCommande.get('subLabel');
        });
      }

      this.set('subLabel',_sublabel);

    },


  });
});
