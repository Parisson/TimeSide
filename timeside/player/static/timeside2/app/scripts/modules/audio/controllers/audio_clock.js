define([
  '#qt_core/controllers/all',
  'buzz'
],
/**
  NOT USED
    Je garde cette classe de côté au cas où le pooling sur buzz.js pose souci, mais en l'état, elle n'est même pas instanciée. 

    Will be cleant if uselessness is confirmed.



  -----------------------
  This controller is the only source to broadcast time events from audio
    As audio can only update every 0.25 or 0.5seconds, this controller listen for play/stop and simulate a clock
    Every time we have a 'real' update from the audio controller, we adjust the time

  Vars
    this.currentTime

  ..... Pas dit qu'on ait besoin de ça en fait.... Voir si on peut pooler directement l'audio...

**/
function (A,buzz) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      
    },

    onDestroy : function() {
    },

    //////////////////////////////////////////////////////////////////////////////////////////
    // loop function to send time
    sendTimeUpdate:function() {

    },
    

  });
});
