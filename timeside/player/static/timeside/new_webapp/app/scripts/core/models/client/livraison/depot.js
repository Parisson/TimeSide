define([
  'backbone.associations',
  'injector',
  '../referentiel/base_totalref'
],

/**
  Depot class
**/
function (Backbone,injector,Cfg,RefModel) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    defaults: {
      id:0,
      codeSAP : '',
      designation : {},
      latt : 0,
      longit : 0,
      employeTotal : false


    },

    relations: [
      
    ],

    translate:function(from,to) {
      if (this.get(from))
        this.set(to,this.get(from));
    },

    fromServer:function() {
      this.translate('lat','latt');
      this.translate('lng','longit');
    }

  });
});
