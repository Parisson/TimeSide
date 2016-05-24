define([
  'backbone.associations'
],

function (Backbone) {

  'use strict';

  return Backbone.AssociatedModel.extend({
    defaults: {
      id : 0,
      nom : '',
      bigvisuel : null,
      smallvisuel : null,
      logo : '',
      mainLocale : '',
      subLocales : [],
      description : {},
      codeCouleur1 : '',
      codeCouleur2 : ''
    },

    relations: [],

    //////////////////////////////////////////
    //update from server

    initFromServer:function() {
      if (this.get('principale')) 
        this.set('mainLocale',this.get('principale'));
      if (this.get('secondaires'))
        this.set('subLocales',this.get('secondaires'));

      if (this.get('visuelIntro'))
        this.set('smallvisuel',this.get('visuelIntro'));

      if (this.get('visuelHome'))
        this.set('bigvisuel',this.get('visuelHome'));      
    }

  });
});
