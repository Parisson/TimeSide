define([
  'injector',

  './client/processor',
  './client/analysis',
  './client/item',
  './client/result_analysis'
  
],

function (injector,ProcessorModel,AnalysisModel,ItemModel,ResultAnalysisModel) {

  var idGenerator=0;

  var hop= {
  	/*'device' : DeviceModel,*/

    processor : ProcessorModel,
    item : ItemModel,
    analysis : AnalysisModel,
    resultAnalysis : ResultAnalysisModel,
   

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
