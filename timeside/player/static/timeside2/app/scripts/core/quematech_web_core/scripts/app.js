define([
  'logger',
  'backbone',
  'injector',
  'marionette',
  'vent',
  '#qt_core/controllers/api',
  'commands/index',
  'controllers/nav',
  'controllers/initdata',
  'routers/router',
  'views/layout',
  '#beans/beans',
  "modernizr",
  'fastclick',
  '#qt_core/controllers/config'
],

function (logger, Backbone, injector,Marionette,vent,api,commandoPool,NavController,InitDataController,Router, LayoutView, beans, 
  Modernizr, FastClick,Cfg) {
  'use strict';
  
  //Done
  FastClick.attach(document.body);

  console.error('WARN : mainLocale done in code');
  injector.set(injector.cfg.currentMainLocale,'fr');
  injector.set(injector.cfg.currentSubLocales,[]);


  //A déplacer!!!!
  

  api.setInterceptEndCallFunction(function(res) {
    
    try {

      // Get CSRF Token value from Cookie using jQuery
      function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              var cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                  var cookie = jQuery.trim(cookies[i]);
                  // Does this cookie string begin with the name we want?
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }
      var csrfToken = getCookie('csrftoken');
      //var csrfTokenSelonThomas = $.cookie('csrftoken');
      

      //var csrfToken = res.xhr.getResponseHeader("X-CSRF-TOKEN");
      if (csrfToken) {
        //console.log("Ok CSRF : "+csrfToken);
        injector.set(injector.cfg.csrfToken,csrfToken);
        var apiController = injector.get(injector.cfg.apiController);
        apiController.removeHeader("X-CSRFToken");
        apiController.addHeader("X-CSRFToken",csrfToken);
      }
      else {
        console.log('No CSRF Token?');
      }
    }
    catch (e) {
      console.error("error while catching end call XHR : "+(e ? JSON.stringify(e) : "NULL?"));
    }
  });


  //end déplacer
  var app = new Marionette.Application();

  app.addInitializer(function () {
    this.commandoPool = commandoPool;

    //temp eric : trace when error
    this.commandoPool.commandError =function(error) {
      console.log('Error : '+error);
      if (error.stack)
        console.log(error.stack);
    };

    window.quemaInjector = injector;
    window.quemaVent = vent;

    injector.set(injector.config['commando.pool'], commandoPool);

    this.apiController = api;
    injector.set(injector.config.api, api.api);
    injector.set(injector.config.apiController, api);

    /*var apiController = injector.get(injector.cfg.apiController);
    apiController.removeHeader("X-CSRFToken");
    apiController.addHeader("X-CSRFToken","7634de7f116fe36d4c152f66c57544abb765181c");
    injector.set(injector.cfg.csrfToken,"7634de7f116fe36d4c152f66c57544abb765181c");*/

  });


  

 
  return app;
});
