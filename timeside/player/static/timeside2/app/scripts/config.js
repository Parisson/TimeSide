    'use strict';

var locale;

var qtcore_url = './core/quematech_web_core/scripts';

require.config({
  waitSeconds: 0,
 
  paths: {
    

      
    '#config': 'core/config',
    '#config_core': qtcore_url+'/config',
    '#behaviors' : qtcore_url+'/behaviors',
    '#controllers' : './controllers',

    '#qt_core' : qtcore_url,
    

    injector: qtcore_url+'/injector',
    vent: qtcore_url+'/vent',
    logger: qtcore_url+'/controllers/logger',
    //modules core
    '#beans'              : qtcore_url+'/modules/beans',
    '#upload'             : qtcore_url+'/modules/upload',

    //modules in
    '#navigation'         : './modules/navigation',
    '#navigation_core'         :  qtcore_url+'/modules/navigation',
    '#auth_core'               :  qtcore_url+'/modules/auth',
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
    handlebars            : qtcore_url+'/vendor/handlebars',
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
    superapi              : qtcore_url+'/vendor/superapi2',/*'../bower_components/superapi/dist/amd/superapi.amd',*/
    'superagent-es6'      : '../bower_components/radiooooo_core/lib/scripts/vendor/superagent-es6',
    'wreqr.injector'      : qtcore_url+'/vendor/wreqr.injector2'/*'../bower_components/wreqr.injector/dist/wreqr.injector'*/,
    localforage           : '../bower_components/localforage/dist/localforage',
    'backbone.associations': '../bower_components/backbone-associations/backbone-associations',
    velocity              : '../bower_components/velocity/velocity',
    swiper                : '../bower_components/swiper/dist/js/swiper',
    modernizr             : '../bower_components/modernizr/modernizr',

    exif                  : qtcore_url+'/vendor/exif',
    binaryajax            : qtcore_url+'/vendor/binaryajax',
    'canvasresize'          : qtcore_url+'/vendor/canvasresize',
    '_moment'               : '../bower_components/moment/moment',
    'moment-fr'             : '../bower_components/moment/locale/fr',
    'moment'                : qtcore_url+'/vendor/moment',
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
