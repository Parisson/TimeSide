define([
  'marionette',
  'templates',
  '#qt_core/controllers/all',
  '#navigation_core/baseviews/base_popupview'
],

/**
    Select an item for creation as admin
**/
function (Marionette, templates,A,BasePopupView) {
  'use strict';

  return BasePopupView.extend({

    
    ////////////////////////////////////////////////////////////////////////////////////
    // View definition
    template: templates['visu/popup_select_item'],
    className: 'popup-admin-select',

    events: {
      'click [data-layout="item"]' : 'onClickItem'
    },

    ui : {
      
    },



    ////////////////////////////////////////////////////////////////////////////////////
    // Ammount changes..
   
    onClickItem:function(ev) {
      A._v.trigCfg('ui.popup.forceclose');
      this.callbackSelect(ev.currentTarget.dataset.id);
      return false;
      
    },

    


    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle
    initialize: function () {

    },

    onDestroy: function () {
      
    },

    onRender:function() {
    },

    serializeData: function () {
      return {
        items : this.items,
        title : this.title
      }
    },

   

    ////////////////////////////////////////////////////////////////////////////////////
    // Popup specific
    historyBackOnClose:function() {return false;},


    //data en entrée doit être une liste de plats}      
    setData:function(data) {
        if (data.callbackSelect)
          this.callbackSelect = data.callbackSelect;
        if (data.items)
          this.items = data.items;
        if (data.title)
          this.title = data.title;
    },

    ////////////////////////////////////////////////////////////////////////////////////
    // 
    

    

  });
});
