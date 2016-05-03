define([
  'backbone.associations',
  'underscore',
  '../../qeopa_basemodel',
  './plat',
  './menu'
],

function (Backbone,_,QeopaBaseModel,PlatModel,MenuModel) {

  'use strict';

 return  QeopaBaseModel.extend({
    defaults: {
      intern_type : 'categorie',
      id : 0,
      titre : {},

      plats : [],
      categories : [],
      menus : [],
      photo : null,
      order : 0
    },

    relations: [ {
      type: Backbone.Many,
      key: 'categories',
      relatedModel: Backbone.Self
    },
    {
      type: Backbone.Many,
      key: 'plats',
      relatedModel: PlatModel
    },
    {
      type: Backbone.Many,
      key: 'menus',
      relatedModel: MenuModel
    }
    ],

    //////////////////////////////////////////
    //update from server

    initFromServer:function() {
      if (this.get('nom')) 
        this.set('titre',this.get('nom'));

      if (this.get('ordre'))
        this.set('order',this.get('ordre'));

      if (this.get('visuel'))
        this.set('photo',this.get('visuel'));

      if (this.get('childs')) 
        this.set('categories',this.get('childs'));

      var self=this;
      if (this.get('categories'))
        this.get('categories').each(function(categorie) {
          categorie.initFromServer()
          categorie.set('parent_id',self.get('id'));
        });
    
    },

    //////////////////////////////////////////

    //get a category or a subcategory based on input id
    getThisOrChildOnId:function(id) {
      var _id = parseInt(id);

      if (this.get('id')===_id)
        return this;

      var ok;
      if (this.get('categories')) { 
        this.get('categories').each(function(_subcat) {
          if (_subcat.get('id')===_id)
            ok=_subcat;
        });
      }
      return ok;
    },

    getMenuOnThisOrChildId:function(id) {
      var _id = parseInt(id);
      if (this.get('menus')) {
        var _menuIn = this.get('menus').find(function(_menu) {
          return _menu.get('id')===_id;
        })
        if (_menuIn)
          return _menuIn;
      }
      if (this.get('categories')) {
        var _menuInSub = this.get('categories').find(function(_subcat) {
          var testOnSub = _subcat.getMenuOnThisOrChildId(_id);
          if (testOnSub)
            return testOnSub;
        });
        if (_menuInSub)
          return _menuInSub;
      }
      return undefined
    },

    getPlatOnThisOrChildId:function(id) {
      var _id = parseInt(id);
      if (this.get('plats')) {
        var _menuIn = this.get('plats').find(function(_menu) {
          return _menu.get('id')===_id;
        })
        if (_menuIn)
          return _menuIn;
      }
      if (this.get('categories')) {
        var _menuInSub = this.get('categories').find(function(_subcat) {
          var testOnSub = _subcat.getPlatOnThisOrChildId(_id);
          if (testOnSub)
            return testOnSub;
        });
        if (_menuInSub)
          return _menuInSub;
      }
      return undefined
    },



    getTypeContent:function() {
      if (this.get('categories') && this.get('categories').length>0)
        return "CATEGORIE";
      else if (this.get('plats') && this.get('plats').length>0)
        return "PLATS"
      else if (this.get('menus') && this.get('menus').length>0)
        return "MENUS"
      return "VIDE";
    },

    updateFakeTrads:function() {
      this.genereTranslateFake(['_titre'],['titre']);
      this.get('plats').each(function(plat) {
        plat.updateFakeTrads();
      });
      this.get('categories').each(function(categorie) {
        categorie.updateFakeTrads();
      });
      this.get('menus').each(function(menu) {
        menu.updateFakeTrads();//genereTranslateFake(['_titre'],['titre']);
      });
    }

  });
});
