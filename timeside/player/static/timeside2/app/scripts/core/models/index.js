define([
  'injector',
  
  
],

function (injector) {

  var idGenerator=0;

  var hop= {
  	/*'device' : DeviceModel,*/
   

    getNewId:function() {
      return idGenerator++;
    },

    createUniqueFakeId:function() {
      var _id = idGenerator++;
      return "FAKE"+_id;
    },

    cloneObjModel:function(obj) {
      var result = obj.clone();
      result.set('id',this.getNewId());
      return result;
    }

  };

  injector.set(injector.cfg.models,hop);
  return hop;

});
