define([
  'injector',
  'backbone.associations',
  '../../qeopa_basemodel',
  './plat_commande',
  './menu_commande',
  '../paiement/paiement',
  '#qt_core/controllers/config',
],

function (injector,Backbone,QeopaBaseModel,PlatCommandeModel,MenuCommandeModel,PaiementModel,Cfg) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      statutCommande : '',
      statutPaiement : '',
      platsCommandes : [],
      menusCommandes : [],
      total : 0,
      paiements : []

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
    },
    {
      type: Backbone.Many,
      key: 'paiements',
      relatedModel: PaiementModel
    }
    ],

    ////////////////////////////////////////////////////////
    //gestion pour paiement

    /**
      Renvoie les éléments non payés de type PlatCommandeModel ou MenuCommandeModel
      dans un obj {platCommandes : plats, menuCommandes : menus}
    **/
    getNotPaidElements:function() {
      //tmp : return copy of all
      //@TODO!!! comparer aux contenus des paiements!!

      var _allPlatsCommandes = new Backbone.Collection(this.get('platsCommandes') ? this.get('platsCommandes').models : []);
      var _allMenusCommandes = new Backbone.Collection(this.get('menusCommandes') ? this.get('menusCommandes').models : []);

      var _platsCommandes = new Backbone.Collection();
      var _menusCommandes = new Backbone.Collection();

      if ( (! this.get('paiements')) || this.get('paiements').models.length===0) {
        return {platCommandes : _allPlatsCommandes, menuCommandes : _allMenusCommandes};
      }
      else {
        var self=this;
        _allMenusCommandes.each(function(_menuCommande) {
          var _isPaid = false;
          self.get('paiements').each(function(_paiement) {
            if (_paiement.hasMenuCommande(_menuCommande))
              _isPaid=true;
          });
          if (! _isPaid)
            _menusCommandes.add(_menuCommande);
        });

        _allPlatsCommandes.each(function(_platCommande) {
          var _isPaid = false;
          self.get('paiements').each(function(_paiement) {
            if (_paiement.hasPlatCommande(_platCommande))
              _isPaid=true;
          });
          if (! _isPaid)
            _platsCommandes.add(_platCommande);
        }); 
      }

      return {platCommandes : _platsCommandes, menuCommandes : _menusCommandes};

      
      
    },

    /**
    Renvoie la somme non payée en comparant avec le contenu des paiements
    **/
    getNotPaidAmount:function() {
      var _total = this.get('total');
      var _paid = 0;
      if (this.get('paiements')) {
        this.get('paiements').each(function(_paiement) {
          _paid = _paid+_paiement.get('sommePaiement');
        });
      }

      return (_total -_paid);

    },


    ////////////////////////////////////////////////////////

    //getter, with  type const ("PLAT" | "MENU") and id
    //WARN : id is id of PlatCommande or MenuCommande, not Plat or Menu!
    //returns {collection : BackboneCollection concernée (this menusCommandes ou this platsCommandes), item : item}
    getItemAndCollectionInCommande:function(type,item_id) {

      var _result = {collection : undefined, item : undefined};
      var _commande = this;
      
      if (_commande && _commande.get('platsCommandes') && type==="PLAT") {
        var _itemInCommande = _commande.get('platsCommandes').find(function(_platCommande) {
          return _platCommande.get('id')===item_id;
        });
        if (_itemInCommande)
          return {collection : _commande.get('platsCommandes'), item : _itemInCommande};
      }

      if (_commande && _commande.get('menusCommandes') && type==="MENU") {
        var _itemInCommande = _commande.get('menusCommandes').find(function(_menuCommande) {
          return _menuCommande.get('id')===item_id;
        });
        if (_itemInCommande)
          return {collection : _commande.get('menusCommandes'), item : _itemInCommande};
      }

      return undefined;
    },

    removeItemInCommande:function(type,item_id) {
      var data = this.getItemAndCollectionInCommande(type,item_id);
      if (data && data.collection && data.item) {
        data.collection.remove(data.item);
      }
    },

    duplicateItemInCommande:function(type,item_id) {
      var data = this.getItemAndCollectionInCommande(type,item_id);
      var models = injector.get(injector.cfg.clientModels);
      if (data && data.collection && data.item) {
        var _newItem = models.cloneObjModel(data.item);
        data.collection.add(_newItem);
      }
    },
   

    ///////////////////////////////////////////////////////////
    //update datas
    updateAttribs:function(log) {
      var _total = 0;
      if (this.get('platsCommandes')) {
        this.get('platsCommandes').each(function(_platCommande) {
          _platCommande.updateAttribs();
          _total = _total + _platCommande.get('total');
        });
      }
      if (this.get('menusCommandes')) {
        if (log) console.log('---Menus Commandes');
        this.get('menusCommandes').each(function(_menuCommande) {

          if (log) console.log('   ---MenuCommande  : '+_menuCommande.get('id'));

          _menuCommande.updateAttribs(log);
          _total = _total + _menuCommande.get('total');

          //used for mapping in recap_commande : plats must know MenuCommandeId
          if (_menuCommande.get('selectionsCommandees')) {
            _menuCommande.get('selectionsCommandees').each(function(_selectionCommandee) {
              _selectionCommandee.set('$dyn_menucommandeid',_menuCommande.get('id'));
            });
          }
        });
      }
      return this.set('total',_total);
    },

    isEmpty:function() {
      var _empty = true;
      if (this.get('platsCommandes') && this.get('platsCommandes').models.length>0)
        _empty=false;
      if (this.get('menusCommandes') && this.get('menusCommandes').models.length>0)
        _empty=false;
      return _empty;
    },


  });
});
