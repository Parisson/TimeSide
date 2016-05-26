define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['data/liste_items'],
    className: 'list-items',

    ui: {
      
    },
    events: {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    



   
   

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.items = A._i.getOnCfg('allItems');
    },

    onRender:function() {
       
    },

    onDestroy: function () {      
    },

    onDomRefresh:function() {
    },

    serializeData: function () {
      

      return {
       items : _.map(this.items,function(obj) {return obj.toJSON();})
      }
    },


    
    
   
  });
});
