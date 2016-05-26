define([
  'underscore',
  'marionette',
  'injector',
  'vent',
  'logger',
  '#navigation/controllers/view.factory',
  './eventid.factory',
  'json!#config/views.json'
],

function (_,Marionette, injector, vent,logger,ViewFactory,EventIdFactory,ConfigView) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options) {
     //app reference
     this.app = options.application;
     this.currentEvents = undefined;
     this.nextView = undefined;

     vent.on('navigate:page',this.onNavigatePage,this);   
     vent.on('show:view',this.onShowView,this);
     
    },

   


    /*================================================================================================*/

    /**
      First input for navigation. This code will get the data and then on its call
      Here : view is a viewid from view.json
    **/
    onNavigatePage:function(viewid,dataid) {
      var view = this._getViewObjFromViewId(viewid);
      if (!view)
        throw new Error("1-no view for : "+viewid);

      this.doNavigatePage(viewid,dataid);
    },

    //direct navigate function (after histroy)
    doNavigatePage:function(viewid,dataid) {
      //1 : ask for commandid and commandreturnid to get data
      var view = this._getViewObjFromViewId(viewid);
      if (!view)
        throw new Error("2-no view for : "+viewid);

      this.nextView = view;
      this.navigationData = dataid;
      if (view.needEvents==="0") {
        //on va directement au showView
        this.onShowView(this.nextView);
        return;
      }


      var events = EventIdFactory.getEventAndBackEvent(view);//.viewid);
      if (events==undefined) {
        console.log("No event Error on "+viewid);
        return;
      }
      this.currentEvents = events;

      //1.5 : listeners
      vent.on(events.ok,this.onOkData,this);
      vent.on(events.error,this.onErrorData,this);

      //2 : launch command
      vent.trigger(events.event,dataid);
    },

    //sous fonction de récupération du view object
    _getViewObjFromViewId:function(viewid) {
      var viewResult;
      _.each(ConfigView.qeopa,function(arg) {
        if (arg.viewid && arg.viewid===viewid)
          viewResult=arg;
      });
       _.each(ConfigView.qt,function(arg) {
        if (arg.viewid && arg.viewid===viewid)
          viewResult=arg;
      });
      return viewResult;
    },

    onOkData:function(arg) {
      this.removeDataListeners();

      vent.trigger('show:view',this.nextView,arg);
    },

    onErrorData:function(arg) {
      this.removeDataListeners();
      console.log("Error error data "+arg);
    },

    //sous fonction, enlève les listeners
    removeDataListeners:function() {
      vent.off(this.currentEvents.ok,this.onOkData,this);
      vent.off(this.currentEvents.error,this.onErrorData,this);
    },

    /*================================================================================================*/

    /**
    * View comes from the views.json file in config, with a viewid and a type params
    * type can be used to check if a total change is necessary or just replace the current view...
    * Now we're cooking with gas!
    *
    * 
    **/
    onShowView:function(view,data) {
      var viewComponent;
      var isInLayout = false;
     
      viewComponent = ViewFactory.getView(view.viewid,view.injectorModelId ? view.injectorModelId : undefined);
      

      //var viewComponent = ViewFactory.getView(view.viewid,view.injectorModelId);
      if (viewComponent.updateData && view.injectorModelId)
        viewComponent.updateData(view.injectorModelId); //donne l'injector model id à suivre pour la data
      if (viewComponent.setDataNavigation && this.navigationData)
        viewComponent.setDataNavigation(this.navigationData); //donne la data d'appel aucazou 
      
      if (view.category)
        vent.trigger('view:newcategory',view.category);

      logger.log("NavigationController","Result from "+view.viewid+" is : "+viewComponent.toString());

      vent.trigger('view:waiting:remove'); //cf behaviors/view/waiting.js
      vent.trigger('popup:forceclose');

      
      //set layout
      this.app.layout.setLayout(view);

      this.app.layout.showView(viewComponent);
      
    },

    

  });
});
