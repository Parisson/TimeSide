define([
  'backbone',
  'marionette',
  'vent',
  'injector',
  '#qt_core/controllers/config',
  '#qt_core/controllers/helpers/apievents_helper'
],

function (Backbone, Marionette, vent,injector,Cfg,ApiEventsHelper) {
  'use strict';

  var NavController = Marionette.Controller.extend({
    initialize: function (options) {
      this.region = options.region;

    },

    onClose: function () {
    },

    ///////////////////////////////////////////////////////////////////
    //help
    userLoggued:function() {
      
      var _user = injector.get(injector.cfg.currentUser);
      return (_user!==undefined)
    },

    getOnIdAndTrigger:function(array,id,viewId,injectorCfg,defaultUrl,dataNavigate) {
      var _id=parseInt(id);
      var _item = _.find(array,function(_item) {
        return _item.get('id')===_id;
      });

      if (_item) {
        injector.set(injectorCfg,_item);
        vent.trigger(Cfg.events.navigate.page,viewId,dataNavigate);
      }
      else {

        vent.trigger(Cfg.events.ui.notification.show, Cfg.msg.no_data_for_page);
        window.location.href=defaultUrl;
      }
    },

    ///////////////////////////////////////////////////////////////////
    //base routes

    home: function () {

      return vent.trigger('navigate:page',Cfg.views.qeopa.home.viewid);

    },

    temp_home : function() {
      vent.trigger('navigate:page',Cfg.views.qeopa.home.viewid);
    },

    item_view : function(uuid) {
      vent.trigger('data:items:getOne',uuid,'item_new_view');
    },

    ///////////////////////////////////////////////////////////////////
    // auth specific routes
    auth_forgetpassword:function() {
      vent.trigger(Cfg.events.ui.popup.show,Cfg.views.popups.auth_forgetpassword.popupid);
    },

    auth_newpassword:function(token) {
      injector.set(injector.cfg.auth_token_newpassword,token);
      vent.trigger(Cfg.events.ui.popup.show,Cfg.views.popups.auth_newpassword.popupid);
    },

    logout:function() {
      vent.trigger(Cfg.eventApi(Cfg.events.auth.logout));
    },


    ///////////////////////////////////////////////////////////////////
    // user management list
    /*list_users:function() {
      if (! this.userLoggued())
        return window.location='/#';
      vent.trigger('navigate:page',Cfg.views.qeopa.list_users.viewid);
    },

    edit_user:function(id) {
      if (! this.userLoggued())
        return window.location='/#';
      this.getOnIdAndTrigger(injector.get(injector.cfg.currentListData),id,
        Cfg.views.qeopa.edit_user.viewid,injector.cfg.currentEditData,'/#users/list',{isCreate : false});

    },

    edit_myprofile:function() {
      if (! this.userLoggued())
        return window.location='/#';
      injector.set(injector.cfg.currentEditData,injector.get(injector.cfg.currentUser));
      vent.trigger(Cfg.events.navigate.page,Cfg.views.qeopa.edit_my_profile.viewid,{isCreate : false});
    },

    new_user:function() {
      if (! this.userLoggued())
        return window.location='/#';
      vent.trigger(Cfg.events.navigate.page,Cfg.views.qeopa.new_user.viewid,{isCreate : true});
    },*/

    

    _resetUrl: function () {
      // clear displayed url
      Backbone.history.navigate('');
    }
  });

  return NavController;
});
