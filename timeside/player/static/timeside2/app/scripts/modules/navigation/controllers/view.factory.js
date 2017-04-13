define([
  'underscore',
  'injector',
  'backbone',
  'json!#config/views.json',
  '#navigation_core/baseviews/base_genericlistview',
  '#navigation_core/baseviews/base_genericimportview',
  '#navigation_core/baseviews/base_generic_confirmimport',
  '#auth/views/index',
  '#navigation/views/home',
  '#navigation/views/tests',

  '#visu/views/index',
  '#data/views/index',
  
],

function (_,injector,Backbone,CfgViews,BaseGenericListView,BaseGenericImportView,BaseGenericConfirmImportView,
  AuthViews,HomeView,TestsView,VisuViews,DataViews
  ) {
  'use strict';

  /**
    * view id names from views.json
    * factory called by navigation controller
    **/


  var factory = function () {
    
  };

  factory.prototype = {

    arrayViewIdConstructor : [
      
      {viewid : CfgViews.qeopa.login.viewid, constructor : AuthViews.views.login},
      {viewid : CfgViews.qeopa.home.viewid, constructor : HomeView},
      {viewid : CfgViews.qeopa.item_view.viewid, constructor : VisuViews.views.itemView},
      {viewid : CfgViews.qeopa.item_new_view.viewid, constructor : VisuViews.views.itemNewView},
      {viewid : CfgViews.qeopa.visu_test1.viewid, constructor : VisuViews.views.test1},
      {viewid : CfgViews.qeopa.visu_test2.viewid, constructor : VisuViews.views.test2},
      {viewid : CfgViews.qeopa.list_items.viewid, constructor : DataViews.views.listItems}
      /*{
        viewid : CfgViews.qeopa.list_users.viewid, 
        constructor : BaseGenericListView,
        configList : UsersViews.configList
      },*/
      

    ],

    getView: function (viewId) {

      var obj = _.find(this.arrayViewIdConstructor,function(_obj) {
        return _obj.viewid && _obj.viewid===viewId;
      });
      if (obj && obj.constructor)
        if (obj.configList)
          return new (obj.constructor)({listParameters : obj.configList});
        else if (obj.configImport)
          return new (obj.constructor)({importParameters : obj.configImport});
        else if (obj.configConfirmImport)
          return new (obj.constructor)({confirmParameters : obj.configConfirmImport});
        else
          return new (obj.constructor)();

      return undefined;

      
    }

  };


  return new factory();
});
