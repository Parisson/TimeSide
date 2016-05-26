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
      'items' : '[data-uuid]'
    },
    events: {
      'click @ui.items' : 'onClickItem'
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Func
    onClickItem:function(e) {
      var uuid = e.currentTarget.dataset.uuid;
      var viewid = e.currentTarget.dataset.viewid;

      A._v.trigCfg('data.items.getOne','',uuid,viewid);
    },
    



   
   

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
