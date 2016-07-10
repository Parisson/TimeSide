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
    name : "analysis",
    baseEvent : "data:analysis",
    commands : [
     
      ////////////////////////GET LIST
      {
        name : "get",
        apiFunctionName : 'getAnalysis',
        createDataBeforeCall : function(data) {
          return {data : undefined, dataApi : getDataApi()};
        },
       
        onSuccess:function(res) {
          //@TODO
          //create model objects and return model
          var result=[];
          if (res && res.body)
            result = _.map(res.body,function(obj) {
              return new A.models.analysis(obj);
            }),
         
          A.vent.trigger(A.Cfg.eventApiOk(A.Cfg.events.data.analysis.get),result);


        }
      }


    ]
  };

  return config;

});
