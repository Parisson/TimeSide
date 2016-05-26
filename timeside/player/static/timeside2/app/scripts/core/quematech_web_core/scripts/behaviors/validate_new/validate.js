define([
  'jquery',
  'marionette',
  'underscore',
  'vent',
  'validator',
  './form_helper'
],
function ($,Marionette, _, vent,validate,FormHelper) {
  'use strict';

  /****

  @SEE : http://validatejs.org/


  New form to validation behavior
    va chercher sur la vue un obj "validatorConfig"

    validatorConfig : {
        selectorInputs : selector to gather inputs
        dataattrib : les inputs doivent avoir un data-* (*=dataattrib) qui permet de sérialiser
          l'objet du formulaire cf constraints
        constraints : http://validatejs.org/#constraints
          objet liant un attribut de l'obj issu de serialisation du formulaire
        updateComponent : function(elt,status,message)
          fonction called on elt (not jquery) with status (error | ok) & message if error
  
    methodes : onValidateContent // triggerMethod('validateContent')
      renvoie un objet de type {attribut : "message d'erreur"}

    }
  ****/
  return Marionette.Behavior.extend({

    events : {
      
    },
   
    initialize: function () {
      if (this.view.validatorConfig) {
        this.validatorConfig = this.view.validatorConfig;
        if (this.validatorConfig.updateComponent==="updateComponentBootstrapValidation")
          this.validatorConfig.updateComponent = this.updateComponentBootstrapValidation;
      }
    },

    //////////////////////////////////////////////////////////////////
    onRender:function() {
      if (! this.validatorConfig)
        return console.error('No validator config for this behavior....'+this.view);

      //chopper tous les inputs et écouter focusout dessus
      this.$allInputs = this.view.$el.find(this.validatorConfig.selectorInputs);
      this.focusOutFunction = _.bind(this.onFocusOut,this);
      this.$allInputs.on('focusout',this.focusOutFunction);
    },


    //destroy hook
    onBeforeDestroy:function() {
      if (this.$allInputs)
        this.$allInputs.off('focusout');
      this.$allInputs = undefined;
    },

    //for validation, bootstrap specific method
    updateComponentBootstrapValidation : function(elt,status,message) {
      var daddyComp = $(elt).parent();
      var lbl = daddyComp.find('label.control-label');
      if (lbl.length>0)
        lbl[0].innerText=message ? message : '';

      if (status==="error") {
        daddyComp.addClass("has-error").removeClass('has-success');
      }
      else {
       daddyComp.addClass("has-success").removeClass('has-error'); 
      }
    },


     //////////////////////////////////////////////////////////////////
    //Récupération d'un objet de type { dataattrib : DOMElt} pour tous
    getObjAttribElement:function() {
      if (! (this.validatorConfig))
        return;

      

      var $inputs = this.view.$el.find(this.validatorConfig.selectorInputs);
      var objAttribElt = {};
      _.each($inputs,function(_input) {


        if (_input.dataset && _input.dataset[this.validatorConfig.dataattrib])
          objAttribElt[_input.dataset[this.validatorConfig.dataattrib]]=_input;
      },this);

      return objAttribElt;
    },

    //////////////////////////////////////////////////////////////////
    //création de l'objet de sérialisation
    onFocusOut:function(evt) {
      //1 chopper la contrainte dans this.validatorConfig.constraints et la value du input
        //ça vaut
      var attributeName = evt.currentTarget.dataset[this.validatorConfig.dataattrib];
      var valueInput = FormHelper.getValueFromInput(evt.currentTarget,this.validatorConfig.dataattrib);

      var specificConstraint = {}
      specificConstraint[attributeName] = this.validatorConfig.constraints[attributeName];

      var arg = {}; arg[attributeName] = valueInput;
       //pour faire la validation, il faut récupérer toutes les valeurs (cas du confirm password qui dépend du password)
      var allValues = this.getValueObject();
      var result = validate(allValues,this.validatorConfig.constraints);

     

      //test avec customValidate
     //2 appeler validate sur cette contrainte et cette value
      if (this.validatorConfig.customValidation) {
        var otherResults = this.validatorConfig.customValidation(allValues,this.view);
        if (otherResults && otherResults[attributeName])
          result = result ? _.extend(result,otherResults) : otherResults; //on ne met result à jour que pour attributeName de l'input
      }

      if ((!result) || (! result[attributeName]))
        this.validatorConfig.updateComponent(evt.currentTarget,'ok',undefined);
      else
        this.validatorConfig.updateComponent(evt.currentTarget,'error',result[attributeName]);


     

      //3 : custom validation ? tricky..., second temps

      //4 : si erreur validate, on l'affiche, sinon on nettoie


    },

    getValueObject:function() {
      if (! (this.validatorConfig))
        return

      var ok= FormHelper.getValueObject(this.view.$el,this.validatorConfig.selectorInputs,this.validatorConfig.dataattrib);
      if (this.validatorConfig.customGetValues) {
        var _okFromView = this.validatorConfig.customGetValues(this.view);
        if (_okFromView)
          ok = _.extend(ok,_okFromView);
      }
      return ok;

    },

    //////////////////////////////////////////////////////////////////
    //validation des champs &&  et mise dans le champs "validate_errors" de la vue
    onValidateContent:function() {
      if (! (this.validatorConfig && this.validatorConfig.constraints))
        return false;

      var objvalues = this.getValueObject();
      if (! objvalues)
        return false;

      var result = validate(objvalues,this.validatorConfig.constraints);

      if (this.validatorConfig.customValidation) {
        var otherResults = this.validatorConfig.customValidation(objvalues,this.view);
        if (otherResults)
          result = result ? _.extend(result,otherResults) : otherResults;
      }

      this.view.validate_values = objvalues;
      this.view.validate_errors = result;

      return result;

    },


    //////////////////////////////////////////////////////////////////
    //validation simple d'un champs (en focusOut)


     //////////////////////////////////////////////////////////////////
    //validation globale des champs avec mise à jour des messages et labels


    //callback return &&  et mise dans le champs "validate_errors" de la vue
    onValidateContentUI:function(callback) {
      if (callback===undefined)
        callback=function(){};

      var _eltPerAttrib=  this.getObjAttribElement();
      var _errors = this.onValidateContent();
      if (! _errors)
        return callback(true);

      //on prend les success
      var _successes = [];
      _.each(_eltPerAttrib,function(value,attrib) {
        if (_errors[attrib])
          return;
        _successes.push(attrib);
      });

      var hasError=false;

      //update des elements en erreur
      _.each(_errors,function(arrayMsgs,attrib) {
        hasError=true;
        var elt = _eltPerAttrib[attrib];
        if (elt && this.validatorConfig.updateComponent) {
          this.validatorConfig.updateComponent(elt,'error',arrayMsgs[0]);
        }
      },this);

      //update des elements success
       _.each(_successes,function(attrib) {
        var elt = _eltPerAttrib[attrib];
        if (elt && this.validatorConfig.updateComponent) {
          this.validatorConfig.updateComponent(elt,'ok',undefined);
        }
      },this);

      this.view.validate_errors = _errors;

      callback(!hasError);
    }



    
  });
});
