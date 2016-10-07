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
    // Get Items

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

        //below : makes a GET ??? a bit un a hurry, so we'll have to understand.
       /* A._i.getOnCfg('api').postAnnotation({
          track : track.get('uuid'),
          start_time : timeStart,
          stop_time : timeEnd,
          title : "Annotation Title",
          description : text
        }).on('success',function(res) {
            alert('success!');
            return callback();
        });*/
    },

     /////////////////////////////////////////////////////////////////////
    // Get One Item & nivigate to view
    
  

   

  });
});
