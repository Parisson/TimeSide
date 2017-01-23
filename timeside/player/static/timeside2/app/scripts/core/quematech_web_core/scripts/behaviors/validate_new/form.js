define([
  'jquery',
  'marionette',
  'underscore',
  'vent',
  'validator',
  '#qt_core/controllers/config',
  './form_helper'
],
function ($,Marionette, _, vent,validate,Cfg,FormHelper) {
  'use strict';

  /****

   NEW Form management!
    view must define :
       formConfig : {
        selectorInputs : '.login_form input', // selector for input for values
        dataattrib : 'validation', //data-stuff to know which attribute on what
        waitingSelector : 'button.has-spinner', // element for waiting
        setWaitingFunction : function(elt,isWaiting) //func to apply to waiting
        launchEvent : '@todoEVENT'
      },
    
  ****/
  return Marionette.Behavior.extend({

    events : {
      
    },
   
    initialize: function () {
      if (this.view.formConfig) {
        this.formConfig = this.view.formConfig;
      }

      this.isWaiting=false;
      this.listenWaitCloseEvent=false;

    },

    //////////////////////////////////////////////////////////////////
    onRender:function() {
     
    },


    //destroy hook
    onBeforeDestroy:function() {
      if (this.listenWaitCloseEvent) {
          this.listenWaitCloseEvent=false;
          vent.off(Cfg.events.ui.waiting.stop,this.onWaitingStop,this);
      }
    },

     //////////////////////////////////////////////////////////////////
    //set / remove waiting
    setWaiting:function(waitingBool) {

      //update UI
      if (this.formConfig && this.formConfig.waitingSelector && this.formConfig.setWaitingFunction)
        this.formConfig.setWaitingFunction(this.formConfig.waitingSelector,waitingBool);

      if (waitingBool) {
        if (! this.listenWaitCloseEvent) {
          this.listenWaitCloseEvent=true;
          vent.on(Cfg.events.ui.waiting.stop,this.onWaitingStop,this);
        }
      }
      else {
        if (this.listenWaitCloseEvent) {
          this.listenWaitCloseEvent=false;
          vent.off(Cfg.events.ui.waiting.stop,this.onWaitingStop,this);
        }
      }

      this.isWaiting = waitingBool;
    },

    onWaitingStop:function() {
      this.setWaiting(false); //remove event
    },


    //////////////////////////////////////////////////////////////////
    //création de l'objet de sérialisation avec values
    getValueObject:function() {
      if (! (this.formConfig))
        return;

      return FormHelper.getValueObject(this.view.$el,this.formConfig.selectorInputs,this.formConfig.dataattrib);

      /*var $inputs = this.view.$el.find(this.formConfig.selectorInputs);
      var objValues = {};
      _.each($inputs,function(_input) {
       

        if (_input.dataset && _input.dataset[this.formConfig.dataattrib]) {
          if (_input.nodeName.toLowerCase()==='select') {
            var _value = _input.options[_input.selectedIndex].value;
             objValues[_input.dataset[this.formConfig.dataattrib]] = _value;
          }
          else if (_input.type==="checkbox") {
            objValues[_input.dataset[this.formConfig.dataattrib]] = _input.checked;
          }
          else {
            objValues[_input.dataset[this.formConfig.dataattrib]]=_input.value;
          }
        }
      },this);

      return objValues;*/
    },

    hasFileUpload:function() {
      var _result=false;
      var $inputs = this.view.$el.find(this.formConfig.selectorInputs);
       _.each($inputs,function(_input) {
        if (_input.dataset && _input.dataset[this.formConfig.dataattrib]) {
          if (_input.type==='file' && _input.files && _input.files.length>0) {
            _result=true;
          }
        }
      },this);

       return _result;
    },

    //////////////////////////////////////////////////////////////////
    // Launch submit (no validation done here, @see validate.js!)
    onLaunchSubmit:function() {
      if (this.isWaiting) {
        return;
      }

      var valueObject = this.getValueObject();
      this.currentValueObject = valueObject;
      this.setWaiting(true);

      if (this.hasFileUpload()) {
        alert(']todo : test & adapt upload so we know which file id goes with which data-attrib');
        this.view.triggerMethod('startUploadImages',_.bind(this.onImagesUploaded,this));
      }
      else {
        this.updateDataBeforeperformSubmit();
      }

     
    },

    onImagesUploaded:function(ids) {
      if (ids && ids.length>0)
        _.each(ids,function(_idObj) {
          if (this.currentValueObject[_idObj.idElement])
            this.currentValueObject[_idObj.idElement] = _idObj.idFile;
        },this);

      this.updateDataBeforeperformSubmit();
    },

    //after images have been uploaded
    updateDataBeforeperformSubmit:function() {
      
      //var valueObject = this.getValueObject();
      if (this.formConfig.beforeSubmitFunction) {
         this.currentValueObject = this.formConfig.beforeSubmitFunction(this.currentValueObject,this.view);
      }

      if (this.formConfig.getWarnings) {
        var _warnings = this.formConfig.getWarnings(this.currentValueObject,this.view); //[{txt}]
        if (_warnings.length>0) {
          var _text="Some warnings have been found, are you sure you want to save ? : [";
          _.each(_warnings,function(_warn) {
            _text=_text+(_warn.txt ? _warn.txt : 'unknown')+", ";
          })

          vent.trigger(Cfg.events.ui.notification.show, 
          {type : 'warning', title : 'Warning',text : _text,
          actions : [
            {label : 'Go on', type : 'danger', callback : _.bind(this.onWarningGoOn,this)},
            {label : 'Abort', type : 'info', callback :  _.bind(this.onWarningStop,this)}
          ]});
          return;
        }
      }   
      this.performSubmit();  
        
    },

    //warnings : ok
    onWarningGoOn:function() {
      vent.trigger(Cfg.events.ui.notification.hide);
      this.performSubmit();
    },

    onWarningStop:function() {
      this.setWaiting(false);
      vent.trigger(Cfg.events.ui.notification.hide);
    },

    //onWarnings
    performSubmit:function() {
      var valueObject =this.currentValueObject;
      if (this.formConfig.launchEvent) {
        if (_.isString(this.formConfig.launchEvent))
          return vent.trigger(this.formConfig.launchEvent,valueObject);
        else if (_.isFunction(this.formConfig.launchEvent)) {
          var _event = this.formConfig.launchEvent(this.view);
          return vent.trigger(_event,valueObject);
        }
      }
      console.error('performSubmit but nothing ? '+JSON.stringify(this.formConfig));
    }



    

    



    
  });
});
