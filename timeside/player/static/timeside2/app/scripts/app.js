define([
  'backbone',
  '#qt_core/controllers/all',
  'controllers/nav',
  'controllers/initdata',
  'routers/router',
  'views/layout',
  '#qt_core/app'
],

function (Backbone,A ,NavController,InitDataController,Router, LayoutView,app) {
  'use strict';
  
  //here app comes from core
  
  app.addRegions({main: '.ts-content'});



  app.addInitializer(function () {
    var self=this;
    var startApp = function() {
     Backbone.history.start();
    };
    A.vent.on(A.Cfg.eventOk(A.Cfg.events.init.start),startApp);

    this.initController = new InitDataController();
    this.router = new Router({
      controller: new NavController({region: app.layout})
    });
    A.injector.set(A.injector.config['mainRouter'],this.router);

    var originajax = $.ajax;
    /*$.ajax = function(obj) {
      if ( (! obj.headers) && A.injector.get('serverToken') )
        obj.headers = {
              "Authorization" : "Token "+A.injector.get('serverToken')
        };

      return originajax(obj);
    };*/


    this.layout = new LayoutView();
    app.main.show(this.layout);

    app.modules=[];
    require(['modules'], function (modules) {

        // load application modules
        modules(app);

        // start init
        A.vent.trigger('initdata:start');
    });

  });

 
  return app;
});
