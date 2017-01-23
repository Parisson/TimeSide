define([
  '../base_qeopaview',
  '#qt_core/controllers/all'
],


/**
  This is the array of genericlistview
**/
function (BaseQeopaView,A) {
  'use strict';

  return BaseQeopaView.extend({


    ////////////////////////////////////////////////////////////////////////////////////
    //View definition

    template: templates['navigation/sub_base_genericlist_array'],
    className: 'genericèlist_array',

    initialize: function (options) { 
        
    },


    onRender:function() {
    },


    onDestroy: function () {
      //alert('argl');
    },

    ui : {
        btnDelete : '.btn_delete_item'
    },  

    events : {
        'click @ui.btnDelete' : 'onDeleteItem'
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //From daddy
    setData:function(headers,data) {
      this.data = data;
      this.headers = headers;
      this.render();
    },
    setDaddy:function(daddy) {
      this.daddy=daddy;
    },
    

    ////////////////////////////////////////////////////////////////////////////////////
    //Intern logic
    onDeleteItem:function(ev) {
      var _id = parseInt(ev.currentTarget.dataset.id);
      this.daddy.deleteItem(_id);
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Managing data
    serializeData: function () {
     
      return {
       
        items : this.data ? this.data : [],
        headers : this.headers ? this.headers : []
      }
    },

    
   
  });
});
