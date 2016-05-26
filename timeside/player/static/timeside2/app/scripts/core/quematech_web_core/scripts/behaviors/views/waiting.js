define([
  'jquery',
  'marionette',
  'underscore',
  'vent',
  '#behaviors/index'
],
function ($,Marionette, _, vent,behaviors) {
  'use strict';

  /****
  Waiting behavior
    A l'appel de triggerMethod('startWaiting'), la vue va se rajouter la classe waiting.
    De même s'il y a un lien interne
    Et va écouter view:waiting:remove

    Savoir que dans une opération de navigation, l'évènement view:waiting:remove et envoyé par défaut
      (même si ce cas est juste pour être propre en mémoire, car l'objet est détruit.)

  ****/
  return Marionette.Behavior.extend({

    events : {
      'click a[href^="/#"]' : 'onInternLinkClick'
    },
   
    initialize: function () {
      this.listenToCloseWaitingEvent = false;
      vent.on('view:waiting:show',this.onStartWaiting,this);
    },

    //////////////////////////////////////////////////////////////////
    onRender:function() {
     
    },

    onInternLinkClick:function(evt) {
      this.onStartWaiting();
      return true;
    },


    onStartWaiting:function() {
      if (this.listenToCloseWaitingEvent)
        return;
      this.view.$el.addClass('waiting');
      this.listenToCloseWaitingEvent = true;
      vent.on('view:waiting:remove',this.onStopWaitingEvent,this);
    },

    onStopWaitingEvent:function() {
      if (this.listenToCloseWaitingEvent) {
        this.listenToCloseWaitingEvent = false;
        vent.off('view:waiting:remove',this.onStopWaitingEvent,this);
        this.view.$el.removeClass('waiting');
      }
    },

    //destroy hook
    onBeforeDestroy:function() {
      console.log('Behavior : onBeforeDestroy');
      vent.off('view:waiting:show',this.onStartWaiting,this);
      if (this.listenToCloseWaitingEvent)
        this.onStopWaitingEvent();
    }



    
  });
});
