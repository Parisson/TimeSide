define([
  'marionette',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_qeopaview',
  'd3'
],

function (Marionette,A,BaseQeopaView,d3) {
  'use strict';

  return BaseQeopaView.extend({

    template: templates['data/item_detail'],
    className: 'item-detail',

    ui: {
      
    },
    events: {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    



   
   

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      this.item = A._i.getOnCfg('currentItem');
    },

    onRender:function() {
       
    },

    onDestroy: function () {      
    },

    onDomRefresh:function() {
    },

    serializeData: function () {
      

      return {
       item : this.item.toJSON()
      }
    },


    
    
   
  });
});
