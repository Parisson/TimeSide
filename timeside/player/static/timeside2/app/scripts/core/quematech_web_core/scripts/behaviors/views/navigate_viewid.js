define([
  'jquery',
  'marionette',
  '#qt_core/controllers/all'
],
function ($,Marionette, A) {
  'use strict';

  /**
    Very simple navigate on data-viewid launched
  **/
  return Marionette.Behavior.extend({


    _getViewObjFromViewId:function(viewid) {
      var viewResult;
      _.each(A.Cfg.views.qeopa,function(arg) {
        if (arg.viewid && arg.viewid===viewid)
          viewResult=arg;
      });
       _.each(A.Cfg.views.qt,function(arg) {
        if (arg.viewid && arg.viewid===viewid)
          viewResult=arg;
      });
      return viewResult;
    },

    events : {
      'click [data-viewid]' : 'onNavigate'
    },

    onNavigate:function(ev) {
      var viewid = ev.currentTarget.dataset.viewid;
      var exists = this._getViewObjFromViewId(viewid);
      if (!exists)
        console.error('This view id does not exist : '+viewid);

      A._v.trigCfg('navigate.page','',viewid);

      return false;
    },
   
    initialize: function () {
      
    },

    //////////////////////////////////////////////////////////////////
    onRender:function() {
     
    },

    //destroy hook
    onBeforeDestroy:function() {
    },

    onClickClose:function() {
      vent.trigger('popup:forceclose');
    }



    
  });
});
