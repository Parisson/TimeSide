    'use strict';

var locale;

var qtcore_url = './core/quematech_web_core/scripts';

require.config({
  waitSeconds: 0,
 
  paths: {
    

      
    '#config': 'core/config',
    '#config_core': './core/quematech_web_core/scripts'+'/config',
    '#behaviors' : './core/quematech_web_core/scripts'+'/behaviors',
    '#controllers' : './controllers',

    '#qt_core' : './core/quematech_web_core/scripts',
    

    injector: './core/quematech_web_core/scripts'+'/injector',
    vent: './core/quematech_web_core/scripts'+'/vent',
    logger: './core/quematech_web_core/scripts'+'/controllers/logger',
    //modules core
    '#beans'              : './core/quematech_web_core/scripts'+'/modules/beans',
    '#upload'             : './core/quematech_web_core/scripts'+'/modules/upload',

    //modules in
    '#navigation'         : './modules/navigation',
    '#navigation_core'         :  './core/quematech_web_core/scripts'+'/modules/navigation',
    '#auth_core'               :  './core/quematech_web_core/scripts'+'/modules/auth',
    '#auth'               : './modules/auth',
    '#users'              : './modules/users',
    '#visu'            : './modules/visu',
    '#audio'            : './modules/audio',
    '#data'            : './modules/data',

    buzz                  : '../bower_components/buzz/dist/buzz',
    bootstrap             : '../bower_components/bootstrap/dist/js/bootstrap',
    jquery                : '../bower_components/jquery/dist/jquery',
    'jquery-ui'               : '../bower_components/jquery-ui/jquery-ui.min',
    FileAPI               : '../bower_components/FileAPI/dist/FileAPI',
    backbone              : '../bower_components/backbone/backbone',
    underscore            : '../bower_components/underscore/underscore',
    'handlebars.runtime'  : '../bower_components/handlebars/handlebars.runtime.amd',
    handlebars            : './core/quematech_web_core/scripts'+'/vendor/handlebars',
    marionette            : '../bower_components/backbone.marionette/lib/core/backbone.marionette',
    'backbone.babysitter' : '../bower_components/backbone.babysitter/lib/backbone.babysitter',
    'backbone.wreqr'      : '../bower_components/backbone.wreqr/lib/backbone.wreqr',
    syphon                : '../bower_components/backbone.syphon/lib/amd/backbone.syphon',
    superagent            : '../bower_components/superagent/superagent',
    text                  : '../bower_components/requirejs-text/text',
    json                  : '../bower_components/requirejs-plugins/src/json',
    replace               : '../bower_components/require.replace/require.replace',
    fixtures              : '../fixtures',
    
    commando              : '../bower_components/commandojs/dist/commando.amd',
    superapi              : './core/quematech_web_core/scripts'+'/vendor/superapi2',/*'../bower_components/superapi/dist/amd/superapi.amd',*/
    'superagent-es6'      : '../bower_components/radiooooo_core/lib/scripts/vendor/superagent-es6',
    'wreqr.injector'      : './core/quematech_web_core/scripts'+'/vendor/wreqr.injector2'/*'../bower_components/wreqr.injector/dist/wreqr.injector'*/,
    localforage           : '../bower_components/localforage/dist/localforage',
    'backbone.associations': '../bower_components/backbone-associations/backbone-associations',
    velocity              : '../bower_components/velocity/velocity',
    swiper                : '../bower_components/swiper/dist/js/swiper',
    modernizr             : '../bower_components/modernizr/modernizr',

    exif                  : './core/quematech_web_core/scripts'+'/vendor/exif',
    binaryajax            : './core/quematech_web_core/scripts'+'/vendor/binaryajax',
    'canvasresize'          : './core/quematech_web_core/scripts'+'/vendor/canvasresize',
    '_moment'               : '../bower_components/moment/moment',
    'moment-fr'             : '../bower_components/moment/locale/fr',
    'moment'                : './core/quematech_web_core/scripts'+'/vendor/moment',
    hammer                  : '../bower_components/hammerjs/hammer',
    fastclick               : '../bower_components/fastclick/lib/fastclick',
    validator               : '../bower_components/validate.js/validate',


    'bootstrap-colorpicker' : '../bower_components/mjolnic-bootstrap-colorpicker/dist/js/bootstrap-colorpicker',

    d3                      : '../bower_components/d3/d3'
  },

  shim: {
    'bootstrap' : {'deps' : ['jquery']},
    /*'ckeditor-jquery':{
        deps:['jquery','ckeditor-core']
    },*/
    'bootstrap-colorpicker' : {
         deps:['jquery','bootstrap']
    },
    'jquery-ui' : {deps : ['jquery']}
  },

  config: {
    replace: {
      // Replace `nls` with the locale of the navigator
      // It will be used to find the right `i18n.json` translation file.
      pattern: 'nls',
      value: function () {
        if (locale) {
          return locale;
        }
        var parts = window.location.search.match(/([^?=&]+)(=([^&]*))?/g);
        for (var i in parts) {
          var tokens = parts[i].split('=');
          if ('lang' === tokens[0]) {
            locale = tokens[1];
            return locale;
          }
        }
        var language = window.navigator.language || window.navigator.userLanguage;
        locale = language.substr(0, 2) || 'en';
        return locale;
      }
    }
  },

  deps: ['jquery', 'underscore',"binaryajax", "exif", "canvasresize","bootstrap","bootstrap-colorpicker"]/**,"jquery.ui.widget", "jqueryiframetransport", "fileupload"]**/
});
