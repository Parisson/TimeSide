define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  var getDataApi = function() {
    return {};
  };

  //used for create && edit
  var beforeSubmitData = function(data) {

    var mappingRole = {
      ADMIN_SI : "ROLE_AdminSI",
      DISPATCHER : "ROLE_Dispatcher",
      AGENT_DEPOT : "ROLE_AgentDepot",
      COMMERCIAL : "ROLE_Commercial"
    };
    if (mappingRole[data.role])
      data.role = mappingRole[data.role];
    else
      data.role = "ROLE_"+data.role;

    if (data['password'].length===0) {
      delete data['password'];
      delete data['confirm_password'];
    }
    else {
      data['confirmPassword'] = data['confirm_password'];
      delete data['confirm_password'];
    }

    if (data['zoneCommerciale']) {
      data['zone']=data['zoneCommerciale'];
      delete data['zoneCommerciale'];
    }

    var dataApi = data['id'] ? {id : data['id']} : undefined; //for edit
    return {data : data, dataApi : dataApi};
  };

  //config
  var config = {
    name : "users",
    baseEvent : "users",
    commands : [
      {
        name : "create",
        apiFunctionName : 'createUser',
        urlAfterSuccess : '/#users/list',
        createDataBeforeCall : beforeSubmitData
      },
      {
        name : "delete",
        apiFunctionName : 'deleteUser',
        urlAfterSuccess : '/#users/list',
        createDataBeforeCall : function(data) {
          return {data : undefined, dataApi : {id : data['id']}};
        }
      },
      { 
        name : "edit",
        apiFunctionName : 'editUser',
        urlAfterSuccess : '/#users/list',
        createDataBeforeCall : beforeSubmitData
      },
      { 
        name : "edit_mine",
        apiFunctionName : 'editUser',
        urlAfterSuccess : '/#users/editmine',
        createDataBeforeCall : beforeSubmitData
      },
      ////////////////////////GET LIST
      {
        name : "get",
        apiFunctionName : 'getUsers',
        createDataBeforeCall : function(data) {
          return {data : data, dataApi : getDataApi()};
        },
        onSuccess:function(res) {
          
          //Result update
          var result=[];

          var paginateData = res.body ? _.omit(res.body,['content']) : null;
          A.injector.set(A.injector.cfg.pagination_data,paginateData);

          //processing...
          if (res.body && res.body.content) 
            _.each(res.body.content,function(obj) {
              var _item = new A.modelsClient.user(obj);
              _item.fromServer()
              result.push(_item);
            });

          A.vent.trigger(A.Cfg.eventApiOk(A.Cfg.events.users.get),result);
        }
      },  

    ]
  };

  return config;

});
