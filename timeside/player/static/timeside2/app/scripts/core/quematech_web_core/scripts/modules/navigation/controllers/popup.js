define([
  'underscore',
  'marionette',
  'injector',
  'vent',
  '#navigation/controllers/popupid.factory',
  '#qt_core/controllers/config'
],

function (_,Marionette, injector, vent,PopupFactory,Cfg) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options) {
     //app reference
     this.app = options.application;
       
     vent.on(Cfg.events.ui.popup.show,this.onShowPopup,this);
     
    },

    //sous fonction de récupération du view object
    _getViewObjFromViewId:function(viewid) {
      var viewResult;
      _.each(Cfg.views.popups,function(arg) {
        if (arg.popupid && arg.popupid===viewid)
          viewResult=arg;
      });
      return viewResult;
    },

    /**
    * View comes from the views.json file in config, with a viewid and a type params
    * type can be used to check if a total change is necessary or just replace the current view...
    * Now we're cooking with gas!
    *
    * 
    **/
    onShowPopup:function(popupId,data) {

      var popup = this._getViewObjFromViewId(popupId);
      if (! popup)
        throw new Error('no popup on '+popupId);

      var popupComponent = PopupFactory.getPopup(popup.popupid);
      if (data && popupComponent.setData)
        popupComponent.setData(data);

      if (popup.category)
        vent.trigger('view:newcategory',popup.category);
      
      console.log("Result from "+popup.popupid+" is : "+popupComponent.toString(),popupComponent);
      
      vent.trigger(Cfg.events.ui.waiting.stop); //cf behaviors/view/waiting.js

      this.app.layout.showPopup(popupComponent);

      
    }
    

  });
});
