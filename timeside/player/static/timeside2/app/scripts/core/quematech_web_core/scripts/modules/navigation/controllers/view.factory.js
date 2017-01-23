define([
  'underscore',
  'injector',
  'backbone',
  'json!#config/views.json',
  '../baseviews/base_genericlistview',
  '../baseviews/base_genericimportview',
  '../baseviews/base_generic_confirmimport',
  '#auth/views/index',
  '#users/views/index',
  '#livraison/views/index',
  
],

function (_,injector,Backbone,CfgViews,BaseGenericListView,BaseGenericImportView,BaseGenericConfirmImportView,
  AuthViews,UsersViews,
  LivraisonViews) {
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
