define([
  ''
  

],

function () {

  return {

    /**
      Take an array of models and send back an array of objs such as : 
        attribDisplay : attrib to display as 'display'
        mainLocale : do we take directly attrib (=null) or do we translated it (='fr')? 
        idSelected = if no null, id to know if obj has selected = true
    **/
    createListWithSelected:function(arrayModels,attribDisplay,mainLocale,idSelected) {
      var result=[];
      _.each(arrayModels,function(_model) {
        var obj = {id : _model.get('id')};
        if (_model.get('codeSAP'))
          obj.codeSAP = _model.get('codeSAP');
        if (mainLocale && mainLocale.length>0) {
          obj['display'] = _model.get(attribDisplay) && _model.get(attribDisplay)[mainLocale] ? 
            _model.get(attribDisplay)[mainLocale] : _model.get(attribDisplay);
        }
        else {
          obj['display'] = _model.get(attribDisplay); 
        }
        if (idSelected!==null && idSelected!==undefined) {//can be 0 
          obj['selected'] = obj.id ===idSelected;
        }
        result.push(obj);
      });
      return result;
    },

    /**
      Produces an object with {mainLocale : dataBefore[attribMainLocale], subLocale_1 : dataBefore[baseAttribSubLocales+subLocale1]}
    **/
  	mergeFieldsTranslated:function(dataBefore,mainLocale,attribMainLocale,subLocales,baseAttribSubLocales) {
      var result = {};
      result[mainLocale] = dataBefore[attribMainLocale];

      if (baseAttribSubLocales && subLocales) {
        _.each(subLocales,function(_subLocale) {
          var _attrib = baseAttribSubLocales + _subLocale;
          if (dataBefore[_attrib]) {
            result[_subLocale] = dataBefore[_attrib];
          }
        });
      }

      return result;
    },

    /**
      Produces an object with {finalAttribName_main : dataBefore[attribName][mainLocale], finalAttribName_other_subLocale1 : blabla
    **/
    createDirectTranslatedFields:function(dataBefore,mainLocale,subLocales,attribName,finalAttribName) {
      var result = {};
      if (! dataBefore[attribName])
        return result;
      var attrib = dataBefore[attribName];
      result[finalAttribName+'_main'] = attrib[mainLocale];
      _.each(subLocales,function(_subLocale) {
        result[finalAttribName+'_other_'+_subLocale] = attrib[_subLocale];
      });
      return result;
    }

  };

});
