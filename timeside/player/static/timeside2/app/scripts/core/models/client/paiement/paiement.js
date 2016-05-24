define([
  'injector',
  'backbone.associations',
  '../../qeopa_basemodel',
  '../commande_store/plat_commande',
  '../commande_store/menu_commande',
  '#qt_core/controllers/config',
],

function (injector,Backbone,QeopaBaseModel,PlatCommandeModel,MenuCommandeModel,Cfg) {

  'use strict';

  /**
    * Représente un paiement unitaire avec pourboire
  **/
  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      typePaiement : '', //DIVISION|PLAT
      platsCommandes : [],
      menusCommandes : [],
      sommePaiement: 0,
      sommePourboire : 0

    },

    relations: [ {
      type: Backbone.Many,
      key: 'platsCommandes',
      relatedModel: PlatCommandeModel
    },
    {
      type: Backbone.Many,
      key: 'menusCommandes',
      relatedModel: MenuCommandeModel
    }
    ],

    ////////////////////////////////////////////////////////
    //gestion pour paiement

    getTotal:function() {
      return this.get('sommePaiement')+this.get('sommePourboire');
    },

    hasMenuCommande:function(_menuCommande) {
      if (this.get('menusCommandes')) {
        var _ok = false;
        this.get('menusCommandes').each(function(_menuTest) {
          if (_menuTest.get('id')===_menuCommande.get('id'))
            _ok=true;
        });
        return _ok;
      }
      return false;
    },

    hasPlatCommande:function(_platCommande) {
      if (this.get('platsCommandes')) {
        var _ok = false;
        this.get('platsCommandes').each(function(_platTest) {
          if (_platTest.get('id')===_platCommande.get('id'))
            _ok=true;
        });
        return _ok;
      }
      return false;
    },
    ///////////////////////////////////////////////////////////
    //update datas
    updateAttribs:function() {
      var _total = 0;
      if (this.get('platsCommandes')) {
        this.get('platsCommandes').each(function(_platCommande) {
          _platCommande.updateAttribs();
          _total = _total + _platCommande.get('total');
        });
      }
      if (this.get('menusCommandes')) {
        this.get('menusCommandes').each(function(_menuCommande) {
          _menuCommande.updateAttribs();
          _total = _total + _menuCommande.get('total');
        });
      }
      return this.set('sommePaiement',_total);
    }


  });
});
