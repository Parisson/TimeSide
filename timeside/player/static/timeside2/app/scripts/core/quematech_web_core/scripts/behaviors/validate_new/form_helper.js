define([
  'jquery',
  'marionette',
  'underscore',
  'vent',
  'validator',
  '#qt_core/controllers/config'
],
function ($,Marionette, _, vent,validate,Cfg) {
  'use strict';

  var helper = function () {
    
  };

  helper.prototype = {

    addValue:function(objValue,attrib,value) {
      if (! objValue[attrib]) {
        objValue[attrib] = value;
        return;
      }

      if (objValue[attrib] && (! _.isArray(objValue[attrib]))) {
        var array = [objValue[attrib]];
        objValue[attrib] = array;
      }
      objValue[attrib].push(value);
    },

    //new
    /**TODO!!!! Un jour : factoriser getValueObject avec cette méthode!!!
      Here : used for focusOUt validation*/
    getValueFromInput:function(_input,dataattrib) {
      var _result;
      if (_input.dataset && _input.dataset[dataattrib]) {
        if (_input.nodeName.toLowerCase()==='textarea') {
          var _value = $(_input).val();
          _result = _value;
        }
        else if (_input.nodeName.toLowerCase()==='select') {
          if (_input.multiple) {
            var _values=[];
            _.each(_input.selectedOptions,function(_opt) {
              _values.push(_opt.value);
            });
            _result = _values;
          }
          else {

            var _value = _input.options.length>0 ? _input.options[_input.selectedIndex].value : undefined;
            _result = _value;
          }
        }
        else if (_input.type==="checkbox") {
          _result = _input.checked;
        }
        else {
          _result = _input.value;
        }
      }

      return _result;
    },

    getValueObject:function($el,selectorInputs,dataattrib) {
      var $inputs = $el.find(selectorInputs);
      var objValues = {};
      _.each($inputs,function(_input) {
       

        if (_input.dataset && _input.dataset[dataattrib]) {
          if (_input.nodeName.toLowerCase()==='textarea') {
            var _value = $(_input).val();
            this.addValue(objValues,_input.dataset[dataattrib],_value);
          }
          else if (_input.nodeName.toLowerCase()==='select') {
            if (_input.multiple) {
              var _values=[];
              _.each(_input.selectedOptions,function(_opt) {
                _values.push(_opt.value);
              });
              this.addValue(objValues,_input.dataset[dataattrib],_values);
            }
            else {

              var _value = _input.options.length>0 ? _input.options[_input.selectedIndex].value : undefined;
              this.addValue(objValues,_input.dataset[dataattrib],_value);
            }
          }
          else if (_input.type==="checkbox") {
            this.addValue(objValues,_input.dataset[dataattrib],_input.checked);
          }
          else {
            this.addValue(objValues,_input.dataset[dataattrib],_input.value);
          }
        }
      },this);

      return objValues;
    },
    
  };

  return new helper();
});
