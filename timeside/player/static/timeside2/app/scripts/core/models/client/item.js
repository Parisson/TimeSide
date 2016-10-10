define([
  'backbone.associations',
  '../qt_basemodel',
  './annotation_track',
  './analysis_track'
],

function (Backbone,BaseModel,AnnotationTrackModel,AnalysisTrackModel) {

  'use strict';

  return BaseModel.extend({
    defaults: {
      id : 0,
      date_added : '',
      date_modified : '',
      description : '',
      file : '',
      hdf5 : '',
      lock : undefined, //bool true|false
      mime_type : '',
      sha1 : '',
      title : '',
      url : '',
      uuid : '',
      audio_duration : 0, //en secondes!!
      audio_url : {}, //{mp3 : URL, ogg : URL}

      annotation_tracks : [], //urls from server
      annotationTracksObjects : [], //intern objects
      analysis_tracks : [], //urls from server
      analysisTracksObjects : [] //intern objects

    },

    relations: [
     {
        type: Backbone.Many,
        key: 'annotationTracksObjects',
        relatedModel: AnnotationTrackModel
      },
      {
        type: Backbone.Many,
        key: 'analysisTracksObjects',
        relatedModel: AnalysisTrackModel
      }],

    //////////////////////////////////////////

  });
});
