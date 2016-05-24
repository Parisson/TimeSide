define([
  'backbone.associations',
  'injector',
  '../referentiel/base_totalref'
],

/**
  Produit class
**/
function (Backbone,injector,RefModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      label : {},
      codeSAP : '',
      familleProduit : null,
      unite : null


    },

    relations: [  {
      type: Backbone.One,
      key: 'familleProduit',
      relatedModel: RefModel
    },
    {
      type: Backbone.One,
      key: 'unite',
      relatedModel: RefModel
    }
      
    ],

    fromServer:function() {
      if (this.get('famille'))
        this.set('familleProduit',this.get('famille'));
    }

  });
});
