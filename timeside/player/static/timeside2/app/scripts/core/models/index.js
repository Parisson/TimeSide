define([
  'injector',

  './client/processor',
  './client/analysis',
  './client/item',
  './client/result_analysis',
  './client/annotation_track'
  
],

function (injector,ProcessorModel,AnalysisModel,ItemModel,ResultAnalysisModel,AnnotationTrackModel) {

  var idGenerator=0;

  var hop= {
  	/*'device' : DeviceModel,*/

    processor : ProcessorModel,
    item : ItemModel,
    analysis : AnalysisModel,
    resultAnalysis : ResultAnalysisModel,
    annotationTrack : AnnotationTrackModel,
   

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
