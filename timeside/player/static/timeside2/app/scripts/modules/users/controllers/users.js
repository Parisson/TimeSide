define([
  'underscore',
  'marionette',
  'injector',
  'vent',
  '#qt_core/controllers/all',
  '#qt_core/controllers/config',
  '#qt_core/controllers/helpers/apievents_helper'

],

function (_,Marionette, injector, vent,A,Cfg,ApiHelper) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options) {
      vent.on(Cfg.events.users.get,this.onGetUsers,this);

      vent.on(Cfg.events.users.create,this.onCreateOrEditUser,this);
      vent.on(Cfg.events.users.edit,this.onCreateOrEditUser,this);


      vent.on(Cfg.events.users.edit_mine,this.onEditMyProfile,this);
    },

    onDestroy : function() {
      vent.off(Cfg.events.users.get,this.onGetUsers,this);

      vent.off(Cfg.events.users.create,this.onCreateOrEditUser,this);
      vent.off(Cfg.events.users.edit,this.onCreateOrEditUser,this);


      vent.off(Cfg.events.users.edit_mine,this.onEditMyProfile,this);
    },

    ////////////////////////////////////////////////////////////////////
    //Edit my profile
    onEditMyProfile:function(data) {
      //let's call API
      var self=this;
      A.ApiEventsHelper.listenOkErrorAndTrigger2(
            A.Cfg.eventApi(A.Cfg.events.users.edit_mine),data,null,function(result) {
              //if ok, t
              self.onEditMyProfileOK();
      },function(error) {
            console.log('onEditMyProfile - unknown error #2');
      },this);

    },

    onEditMyProfileOK:function() {
      //edit profile ok : launch /me
       A.ApiEventsHelper.listenOkErrorAndTrigger2(
        A.Cfg.eventApi(A.Cfg.events.users.me),null,null,function(result) {
          //youpi, reload edit my profile with notification OK
           A.vent.trigger(A.Cfg.events.ui.notification.show,{type : 'info', text : "Votre compte a été modifié"});
          injector.set(injector.cfg.currentEditData,injector.get(injector.cfg.currentUser));
          vent.trigger(Cfg.events.navigate.page,Cfg.views.qeopa.edit_my_profile.viewid,{isCreate : false});
        },function(error) {
          //not logued and youpi
           A.vent.trigger(A.Cfg.events.ui.notification.show,{type : 'error', text : "Erreur serveur"});
        },this);
    },

    ////////////////////////////////////////////////////////////////////
    //Getting user data
    /**
    * data inside can be undefined or type {page : int, term : String}
    **/
    onGetUsers:function(data) {
      ApiHelper.listenOkErrorAndTrigger(Cfg.eventApi(Cfg.events.users.get),data,null,this.onGetUsersOk,this.onGetUsersError,this);

    },

    onGetUsersOk:function(result) {
      ApiHelper.removeOkError(Cfg.eventApi(Cfg.events.users.get),this.onGetUsersOk,this.onGetUsersError,this);
      injector.set(injector.cfg.currentListData,result);
      vent.trigger(Cfg.eventOk(Cfg.events.users.get));
    },

    onGetUsersError:function() {
      ApiHelper.removeOkError(Cfg.eventApi(Cfg.events.users.get),this.onGetUsersOk,this.onGetUsersError,this);
    },

    ////////////////////////////////////////////////////////////////////
    //Creating or editing user data
    onCreateOrEditUser:function(data) {
      var _isCreate = data.isCreate;
      //get zones commerciales && depots
     
      A.ApiEventsHelper.listenOkErrorAndTrigger2(
        A.Cfg.eventApi(A.Cfg.events.clients.zone_commerciale.get),null,null,function(result) {
          A.injector.set(A.injector.cfg.allZonesCommerciales,result);

          //get depots
          A.ApiEventsHelper.listenOkErrorAndTrigger2(
            A.Cfg.eventApi(A.Cfg.events.clients.depot.get),null,null,function(result) {
              A.injector.set(A.injector.cfg.allDepots,result);

              var eventBack = _isCreate ? A.Cfg.eventOk(A.Cfg.events.users.create) : A.Cfg.eventOk(A.Cfg.events.users.edit);
              A.vent.trigger(eventBack);

          },function(error) {
            console.log('onCreateOrEditUser - unknown error #2');
          },this);

          
        },function(error) {
          console.log('onCreateOrEditUser - unknown error #1');
        },this);
    }
    

  });
});
