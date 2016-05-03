define([
  'backbone.associations',
  '../../qeopa_basemodel',
  './accompagnement',
  './option',
  './categorie',
  './prix_plat',
  '#qt_core/controllers/config'
],

function (Backbone,QeopaBaseModel,AccompagnementModel,OptionModel,CategorieModel,PrixPlatModel,Cfg) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      intern_type : 'plat',
      id : 0,
      titre : {},
      description : {},
      bigvisuel : '',
      smallvisuel : '',

      prixBase : 0,
      prix : [],
      tarifs : [], //doublon prix

      ////
      options : [],
      accompagnements : [],
      categories : [],

      ///only in menu, dynamic
      supplement : 0
    },

    relations: [ {
      type: Backbone.Many,
      key: 'options',
      relatedModel: OptionModel
    },
    {
      type: Backbone.Many,
      key: 'accompagnements',
      relatedModel: AccompagnementModel
    },
    {
      type: Backbone.Many,
      key: 'categories',
      relatedModel: function(){return require(["#models/client/commande/categorie"])}
    },
    {
      type: Backbone.Many,
      key: 'prix',
      relatedModel: PrixPlatModel
    },
    {
      type: Backbone.Many,
      key: 'tarifs',
      relatedModel: PrixPlatModel
    }
    ],

    ///////


     initFromServer:function() {
      if (this.get('nom')) 
        this.set('titre',this.get('nom'));

      if (this.get('visuel'))
        this.set('bigvisuel',this.get('visuel'));

      if (this.get('visuel'))
        this.set('smallvisuel',this.get('visuel'));

      //Non : fait dans la commande de récupération!
      /*if (this.get('prix'))
        this.set('prixBase',this.get('prix'));*/

      
      if (this.get('tarifs')) {
        this.get('tarifs').each(function(_tarif) {
          _tarif.initFromServer();
        });
        this.set('prix',this.get('tarifs'));
      }




    
    },


    //fake _titre translations
    updateFakeTrads:function() {
      this.genereTranslateFake(['_titre'],['titre']);
      this.genereTranslateFake(['_description'],['description']);
      this.get('options').each(function(_option) {
        _option.genereTranslateFake(['_titre'],['titre']);
      });
      this.get('accompagnements').each(function(_acc) {
        _acc.genereTranslateFake(['_titre'],['titre']);
      });

      this.get('prix').each(function(_prix) {
        _prix.genereTranslateFake(['_titre'],['titre']);
      });
    },

    ///////////////////////////////////////////////////////////
    //Special getters

    getDisplayPrix:function() {
      if (this.get('displayPrix'))
        return this.get('displayPrix');

      var _displayPrix = 0;
      if (this.get('prixBase') && this.get('prixBase')>0)
        _displayPrix = this.get('prixBase');
      else if (this.get('prix')){
        this.get('prix').each(function(_price) {
          if (_displayPrix===0)
            _displayPrix = _price.get('prix')
          else
            _displayPrix = Math.min(_displayPrix,_price.get('prix'));
        });
      }
      this.set('displayPrix',_displayPrix);
      return _displayPrix;
    },

    getAdminDiplayPrix:function() {
      if (this.get('adminDisplayPrix'))
        return this.get('adminDisplayPrix');

      var _displayPrix = '';
      if (this.get('prixBase') && this.get('prixBase')>0)
        _displayPrix = ''+this.get('prixBase');
      else if (this.get('prix')){
        _displayPrix='[';
        this.get('prix').each(function(_price) {
          _displayPrix=_displayPrix+_price.get('prix')+',';
        });
        _displayPrix=_displayPrix+']';
      }
      this.set('adminDisplayPrix',_displayPrix);
      return _displayPrix;
    },

    //typedetail from consts
    hasDetail:function(typeDetail) {
      if (typeDetail==="PRIX") 
        return this.get('prix') && this.get('prix').length>0;
      
      if (typeDetail==="ACCOMPAGNEMENT")
        return this.get('accompagnements') && this.get('accompagnements').length>0;

      if (typeDetail==="OPTION")
        return this.get('options') && this.get('options').length>0;
    },

    getDetail:function(typeDetail) {
       if (typeDetail==="PRIX") 
        return this.get('prix');
      
      if (typeDetail==="ACCOMPAGNEMENT")
        return this.get('accompagnements');

      if (typeDetail==="OPTION")
        return this.get('options');
    }


  });
});
