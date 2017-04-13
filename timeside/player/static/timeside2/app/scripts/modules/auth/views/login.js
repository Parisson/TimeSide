define([
  'marionette',
  'templates',
  'vent',
  'injector',
  'jquery',
  '#qt_core/controllers/config',
  '#navigation_core/baseviews/formview',
  '#behaviors/index'
],

function (Marionette, templates, vent,injector, $,Cfg,FormView,behaviors) {
  'use strict';

  return FormView.extend({


    ////////////////////////////////////////////////////////////////////////////////////
    //Validation behavior
    validatorConfig: {
      selectorInputs : '.login_form input',
      dataattrib : 'validation',
      constraints : {
        /*'username' : {
          email : {message : 'Must be a valid email'},
          presence : true
        },*/
        'password' : {
          length: {
            minimum: 4,
            message: "must be at least 4 characters"
          },
          presence : true

        }
      },
      updateComponent : 'updateComponentBootstrapValidation'
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Form behavior
    formConfig : {
      selectorInputs : '.login_form input',
      dataattrib : 'validation',
      waitingSelector : 'button.has-spinner',
      setWaitingFunction : function(elt,isWaiting) {
        if (isWaiting)
          $(elt).addClass('active');
        else
          $(elt).removeClass('active');
      },
      launchEvent : Cfg.events.auth.login
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //View definition

    template: templates['auth/login'],
    className: 'login_view',

    ui: { 
      btnGo :'#btnGo',
      btnTestNotif : '#btn-testnotif'
    },
    events: {
      'click @ui.btnGo' : 'onClickGo',
      'click @ui.btnTestNotif' : 'onClickTestNotif',
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Life cycle

    initialize: function () {
      
      
    },

    onRender:function() {
      
    },


    onClose: function () {
      
    },

    ////////////////////////////////////////////////////////////////////////////////////
    //Logic
    onClickTestNotif:function() {
      vent.trigger(Cfg.events.ui.notification.show, {type : 'info', text : 'Zis is a test'});
    },

    onClickGo:function() {
      var self=this;
      this.triggerMethod('validateContentUI',function(success) {
        if (success)  
          self.triggerMethod('launchSubmit');
      });
    }
   
    
   
  });
});
