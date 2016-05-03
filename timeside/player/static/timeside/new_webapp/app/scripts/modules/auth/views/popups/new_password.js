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
      selectorInputs : '.newpassword_form input',
      dataattrib : 'validation',
      constraints : {
        'email' : {
          email : true,
          presence : true,

        },
        password : {
          length : {
            minimum : 6
          }

        },
        confirm_password : {
          equality : "password"
        }
      },
       customValidation : function(objValues,view) {
        var result = {};
        if (objValues['password'].length===0)
          result['password'] = ["Please enter a password"];

        if (objValues['confirm_password'].length===0)
          result['confirm_password'] = ["Please confirm password"];
      

        var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/;
        if (objValues['password'].length>0 && (! re.test(objValues.password))) {
          result["password"] = ["must contain at least one lowercase, one uppercase and one number"];
        }
        return result;

      },
      updateComponent : 'updateComponentBootstrapValidation'
    },


    ////////////////////////////////////////////////////////////////////////////////////
    //Form behavior
    formConfig : {
      selectorInputs : '.newpassword_form input',
      dataattrib : 'validation',
      waitingSelector : 'button.has-spinner',
      setWaitingFunction : function(elt,isWaiting) {
        if (isWaiting)
          $(elt).addClass('active');
        else
          $(elt).removeClass('active');
      },
      launchEvent : Cfg.eventApi(Cfg.events.auth.changePassword)
    },

    ////////////////////////////////////////////////////////////////////////////////////
    // View definition
    template: templates['auth/popup_newpassword'],
    className: 'popup_newpassword',

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
