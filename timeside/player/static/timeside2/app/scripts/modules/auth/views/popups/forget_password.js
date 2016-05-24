define([
  'marionette',
  'templates',
  'vent',
  'injector',
  '#qt_core/controllers/config',
  '#navigation_core/baseviews/base_popupview'
],

/**
  
**/
function (Marionette, templates,vent,injector,Cfg,BasePopupView) {
  'use strict';

  return BasePopupView.extend({

    ////////////////////////////////////////////////////////////////////////////////////
    //Validation behavior
    validatorConfig: {
      selectorInputs : '.forgetpassword_form input',
      dataattrib : 'validation',
      constraints : {
        'username' : {
          presence : true
        },
        'username2' : {
          equality : 'username',
          presence : true

        }
      },
      updateComponent : 'updateComponentBootstrapValidation'
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Form behavior
    formConfig : {
      selectorInputs : '.forgetpassword_form input',
      dataattrib : 'validation',
      waitingSelector : 'button.has-spinner',
      setWaitingFunction : function(elt,isWaiting) {
        if (isWaiting)
          $(elt).addClass('active');
        else
          $(elt).removeClass('active');
      },
      launchEvent : Cfg.eventApi(Cfg.events.auth.ask_resetPassword)
    },

    ////////////////////////////////////////////////////////////////////////////////////
    // View definition
    template: templates['auth/popup_forgetpassword'],
    className: 'popup_forgetpassword',

    events: {
      'click @ui.btnGo' : 'onClickGo'
    },

    ui : {
      btnGo :'#btnGo'
    },

    initialize: function () {
    },

    onDestroy: function () {
      
    },

    onRender:function() {
    },

    serializeData: function () {
      return {
        
      }
    },

   

    ////////////////////////////////////////////////////////////////////////////////////
    // Popup specific
    historyBackOnClose:function() {return true;},


    //data en entrée doit être une liste de plats}      
    setData:function(data) {
        
    },

    ////////////////////////////////////////////////////////////////////////////////////
    // 
     ////////////////////////////////////////////////////////////////////////////////////
    //Logic
    onClickGo:function() {
      var self=this;
      this.triggerMethod('validateContentUI',function(success) {
        if (success)  
          self.triggerMethod('launchSubmit');
      });
    }

    

  });
});
