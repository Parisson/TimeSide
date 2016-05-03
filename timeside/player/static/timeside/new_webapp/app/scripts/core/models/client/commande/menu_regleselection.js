define([
  'backbone.associations',
  '../../qeopa_basemodel',
  './menu_selection'
],

function (Backbone,QeopaBaseModel,SelectionModel) {

  'use strict';

  return QeopaBaseModel.extend({
    defaults: {
      id : 0,
      typeRegle : '',
      titre : {},
      selections : [],

      //dynamic
      labelsPerSelection : [] //array de array de string
    },

    relations: [{
      type: Backbone.Many,
      key: 'selections',
      relatedModel: SelectionModel
    }],

    //////////////////////////////////////////
    hasSelection:function(selection) {
      var hasSelect = false;
      if (this.get('selections')) {
        this.get('selections').each(function(_select) {
          if (_select.get('id')===selection.get('id'))
            hasSelect=true;
        });
      }
      return hasSelect;
    },

    //////////////////////////////////////////
    updateAttribs:function() {
      var _labsPerSelection = [];
      if (this.get('selections')) {
        this.get('selections').each(function(_selection) {
          _selection.updateAttribs();
          var _labels = _selection.get('labelsPlats'); //isArray
          _labsPerSelection.push(_labels);
        });
      }
      this.set('labelsPerSelection',_labsPerSelection);
    }

  });
});
