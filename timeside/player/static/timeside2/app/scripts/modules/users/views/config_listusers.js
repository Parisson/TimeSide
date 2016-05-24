define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  var getDataApi = function() {
   return "";
  };

  //generic get translated function
  var getTranslatedFunc = function(nameAttrib) {
    return function(data) {
      var mainLocale = A.injector.get(A.injector.cfg.currentMainLocale);
      if (! data[nameAttrib])
        return "Xx_";
      return data[nameAttrib][mainLocale] ? data[nameAttrib][mainLocale] : "XX__";
    };
  };

  var getSubGetterFunc = function(nameAttrib,nameInAttrib) {
    return function(data) {
      var mainLocale = A.injector.get(A.injector.cfg.currentMainLocale);
      if (! data[nameAttrib])
        return "Xx_";
      var subObj = data[nameAttrib];
      if (! subObj[nameInAttrib])
        return "Xx2_";


      return subObj[nameInAttrib][mainLocale] ? subObj[nameInAttrib][mainLocale] : "XX3__";
    };
  };

  //generic createButtons function
  var createButtonsFunc = function()  {
    return function(data) {
      var htmlCode =  '<a href="/#users/edit/'+data.id+'"><button type="button" data-id="'+data.id+'" class="btn_edit_item btn btn-info">Edit</button></a>'
        +'&nbsp;<button type="button" data-id="'+data.id+'" class="btn_delete_item btn btn-danger">Delete</button>';
      return {type : 'html', value : htmlCode}; //works with handlebars helper val
    }
  };

  //config
  var configListDataRef = {
    title : "users",
    url : "/#users/list",
    showFilter : true,
    hasAllData : false,
    viewId : A.Cfg.views.qeopa.list_users.viewid,
    eventDelete : A.Cfg.eventApi(A.Cfg.events.users.delete),
    eventForFilter : A.Cfg.eventApi(A.Cfg.events.users.get),
    newButton : {
        label : "New user",
        url : "/#users/new"
    },
    injectorListId : A.injector.cfg.currentListData,
    beforeShowDataFunc : function(data) {
      var mainLocale = A.injector.get(A.injector.cfg.currentMainLocale);
      if (_.isArray(data))
        _.each(data,function(item) {
           item.set('_dyn_detail',item.getDetail(mainLocale));
        });

      /*data = _.filter(data,function(item) {
        return item.get('role')!=="CLIENT"
      });*/ //nique la pagination
     
      return data;
    },
    list : {
      headers : ["Email","Role","Téléphone","Detail", "Actions"], //last getter defined below in createOkConfig
      getters : ['email','role','telephone','_dyn_detail',createButtonsFunc()]
    }
    
  };

  return configListDataRef;

});
