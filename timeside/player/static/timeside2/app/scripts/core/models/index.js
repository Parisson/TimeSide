define([
  'injector',

  './client/processor',
  './client/analysis',
  './client/item'
  
],

function (injector,ProcessorModel,AnalysisModel,ItemModel) {

  var idGenerator=0;

  var hop= {
  	/*'device' : DeviceModel,*/

    processor : ProcessorModel,
    item : ItemModel,
    analysis : AnalysisModel,
   

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
