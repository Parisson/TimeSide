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
    return result;
  };

  //config
  var config = {
    name : "items",
    baseEvent : "data:items",
    commands : [
     
      ////////////////////////GET LIST
      {
        name : "get",
        apiFunctionName : 'getItems',
        createDataBeforeCall : function(data) {
          return {data : undefined, dataApi : getDataApi()};
        },
       
        onSuccess:function(res) {
          //@TODO
          //create model objects and return model
          var result=[];

          if (res && res.body)
            result = _.map(res.body,function(obj) {
              var result =  new A.models.item(obj);
              var url = result.get('url');
              var index = url.indexOf("items/");
              var uuid = url.substr(index+"items/".length);
              uuid = uuid.substring(0,uuid.length-1); //virer le dernier carac

              result.set("uuid",uuid);
              return result;
            });
          
          A.vent.trigger(A.Cfg.eventApiOk(A.Cfg.events.data.items.get),result);


        }
      },

       ////////////////////////GET ONE
      {
        name : "getOne",
        apiFunctionName : 'getOneItem',
        createDataBeforeCall : function(data) {
          return {data : undefined, dataApi : {id : data.id}};
        },
       
        onSuccess:function(res) {
          var result = new A.models.item(res.body);
          var url = result.get('url');
          var index = url.indexOf("items/");
          var uuid = url.substr(index+"items/".length);
          uuid = uuid.substring(0,uuid.length-1); //virer le dernier carac

          result.set("uuid",uuid);
          
          A.vent.trigger(A.Cfg.eventApiOk(A.Cfg.events.data.items.getOne),result);
        }
      }


    ]
  };

  return config;

});
