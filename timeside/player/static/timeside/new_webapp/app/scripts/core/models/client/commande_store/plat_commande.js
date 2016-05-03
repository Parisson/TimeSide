define([
  'backbone.associations',
  '../../qeopa_basemodel',
  '../commande/accompagnement',
  '../commande/option',
  '../commande/plat',
  '../commande/prix_plat',
  '#qt_core/controllers/config'
],

function (Backbone,QeopaBaseModel,AccompagnementModel,OptionModel,PlatModel,PrixPlatModel,Cfg) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      plat : null,
      accompagnements : [],
      options : [],
      prix_plat : null,

      //dynamic below
      label : '',
      subLabel : '',
      total : 0

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
      type: Backbone.One,
      key: 'plat',
      relatedModel: PlatModel
    },
    {
      type: Backbone.One,
      key: 'prix_plat',
      relatedModel: PrixPlatModel
    }
    ],

    ///////
   

    ///////////////////////////////////////////////////////////
    //Add stuff like option / accompagnement / prix. Type from const
    addStuff:function(typeStuff,item) {
      if (typeStuff==="PRIX")
        this.set('prix_plat',item);
      if (typeStuff==="ACCOMPAGNEMENT") {
        this.get('accompagnements').add(item);
      }
      if (typeStuff==="OPTION") {
        this.get('options').add(item);
      }
    },

    //from command controller when re-updating a plat
    resetStuffForUpdate:function() {
      this.set('prix_plat',null);
      this.get('accompagnements').reset();
      this.get('options').reset();
    },

    //////Update attribs like total
    updateAttribs:function() {
      this.updateTotal();
      this.updateLabel();
      this.updateSubLabel();
    },

    updateLabel:function() {
      var _label="";
      if (! this.get('plat'))
        return this.set('label',"");

      this.set('label',this.get('plat').getLabelI18N('titre'));
    },

    //used in recap commande
    updateSubLabel:function() {
      var _sublabels=[];
      var addToSubLabel = function(arg) {if (_.isString(arg) && arg.length>0) _sublabels.push(arg);}
      if (this.get('prix_plat')) {
        addToSubLabel(this.get('prix_plat').getLabelI18N('titre'));
        //_sublabel = _sublabel+this.get('prix_plat').getLabelI18N('titre');
      }

      if (this.get('accompagnements')) {
        _//sublabel=_sublabel+", ";
         this.get('accompagnements').each(function(_accomp) {
            addToSubLabel(_accomp.getLabelI18N('titre'));
            /*_sublabel=_sublabel+_accomp.getLabelI18N('titre');*/
        });
      }

      if (this.get('options')) {
        //_sublabel=_sublabel+", "
        this.get('options').each(function(_option) {
          addToSubLabel(_option.getLabelI18N('titre'));
          //_sublabel=_sublabel+_option.getLabelI18N('titre');
        });
      }

      this.set('subLabel',_sublabels);

    },

    updateTotal:function() {
      var _total = 0;
      if (! this.get('plat'))
        return this.set('total',_total);

      var _plat = this.get('plat');
      _total = _plat.get('prixBase');

      if (this.get('prix_plat')) {
        _total = _total+this.get('prix_plat').get('prix');
      }

      if (this.get('options')) {
        this.get('options').each(function(_option) {
          if (_option.get('deltaPrix') && _option.get('deltaPrix')>0)
            _total=_total+_option.get('deltaPrix');
        });
      }

      if (this.get('accompagnements')) {
         this.get('accompagnements').each(function(_accomp) {
          if (_accomp.get('deltaPrix') && _accomp.get('deltaPrix')>0)
            _total=_total+_accomp.get('deltaPrix');
        });
      }

      return this.set('total',_total);
    }





  });
});
