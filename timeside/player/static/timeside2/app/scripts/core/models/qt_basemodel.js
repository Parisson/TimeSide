define([
  'backbone.associations',
  'injector'
],

function (Backbone,injector) {

  'use strict';

  return Backbone.AssociatedModel.extend({

    //conversion server->client. Arg is obj {attrib : value} where attrib -> value
    //for fromServer // toServer functions
    applyConvert:function(obj) {
      _.each(obj,function(value,nameAttrib) {
        if (this.get(nameAttrib))
          this.set(value,this.get(nameAttrib));
      });
    },

    getLabelI18N:function(attrib) {
      var _obj = this.get(attrib);
      var _currentLocale = injector.get(injector.cfg.currentLocale);
      var _defaultLocale = 'fr';
      if (! _currentLocale)
        _currentLocale=_defaultLocale;

      if (_obj && _obj[_currentLocale])
        return _obj[_currentLocale];

      if (_obj && _obj[_defaultLocale])
        return _obj[_defaultLocale];

      return undefined;
    },


    //For fake data, generating traduction from _attrib
    genereTranslateFake:function(arrayAttribsSrc,arrayAttribsTarget) {

      for (var i=0; i<arrayAttribsSrc.length; i++) {
        var attribSrc = arrayAttribsSrc[i], attribTarget = arrayAttribsTarget[i];
        var self=this;
        var traductedObj = {};
        _.each(['fr','en','es'],function(locale) {
          /*if (!self.get(attribSrc))
            console.log('wtf?');*/
          traductedObj[locale] = self.get(attribSrc)+'_'+locale;
        })
        this.set(attribTarget,traductedObj);
      }
    }

    //////////////////////////////////////////


    //////////////////////////////////////////

  });
});
