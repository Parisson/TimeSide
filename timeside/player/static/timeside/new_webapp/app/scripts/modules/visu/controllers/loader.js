define([
  '#qt_core/controllers/all',
  'd3'
],

function (A,d3) {
  'use strict';

  /**
  Controller centralisant les demandes aux serveur
    //will use _.debounce to assure we don't override loadings
        
  **/
  return Marionette.Controller.extend({
    initialize: function (options)	 {
      A._i.setOnCfg('dataLoader',this);


      this.mapFuncByType = {}; //contient pour chaque type la méthode _.debounce
    },

    onDestroy : function() {
       
    },

    /////////////////////////////////////////////////////////////////////////////
    //Gestion de la map de demande
    getDataFunction:function(type) {
      if (! this.mapFuncByType[type]) {
        this.mapFuncByType[type] = _.debounce(this.askDataFunc,200);
      }
      return this.mapFuncByType[type]
    },

    /////////////////////////////////////////////////////////////////////////////
    //Demande de la part d'un provider
    askNewData:function(type,timeStart,timeEnd,nbItem,callback) {
      ( this.getDataFunction(type) )(type,timeStart,timeEnd,nbItem,callback);
    },

    //ok
    askDataFunc:function(type,timeStart,timeEnd,nbItem,callback) {
      A.log.log('loader','launching data ask for : '+type+','+timeStart+','+timeEnd+' : '+nbItem);

      A._v.trigCfg('fakeserver.getdata','',type,timeStart,timeEnd,nbItem,function(data) {
        callback(data);
      });

    },


   

  });
});
