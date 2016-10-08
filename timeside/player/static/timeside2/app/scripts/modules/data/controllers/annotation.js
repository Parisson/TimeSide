define([
  '#qt_core/controllers/all'
],

/*
    Controller en charge de poster des annotations
**/
function (A) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      A._i.setOnCfg('annotationControlller',this);
    },

    onDestroy : function() {
     
     
    },

    /////////////////////////////////////////////////////////////////////
    // get updated data for a track
    udpateTrackDataFromServer:function(oldTrackObject,callback) {
      var urlAnnotation = oldTrackObject.get('url');
      $.get(urlAnnotation,function(res) {
        var item = A._i.getOnCfg('currentItem');

        //Replace in item
        var oldTrack = item.get('annotationTracksObjects').find(function(annotationTrack) {
          return annotationTrack.get('uuid')==oldTrackObject.get('uuid');
        });

        if (!oldTrack) {
          return console.error('udpateTrackDataFromServer : old track not found on : '+oldTrackObject.get('uuid'));
        }

        oldTrack.set('annotations',res.annotations);
        return callback(oldTrack); //du coup, on garde oldTrack comme objet dans le modèle
      });
    },

    /////////////////////////////////////////////////////////////////////
    // create Items

    postAnnotation:function(track,timeStart,timeEnd,text,callback) {
        var data = {
          track : track.get('url'),
          start_time : timeStart,
          stop_time : timeEnd,
          title : "Annotation Title",
          description : text
        };

        
        return $.post('http://timeside-dev.telemeta.org/timeside/api/annotations/',data,function(res) {
          console.log('post done');
          return callback();
        });

    },

     /////////////////////////////////////////////////////////////////////
    // Get One Item & nivigate to view
    
  

   

  });
});
