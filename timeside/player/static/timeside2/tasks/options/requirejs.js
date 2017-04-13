/*global module*/
'use strict';

module.exports = {

  widget: {
    options: {
      baseUrl: '<%= yeoman.app %>/scripts',
      optimize: 'none',
      out: '<%= yeoman.dist %>/scripts/main_widget.js',
      // name: '../bower_components/almond/almond',
      mainConfigFile: '<%= yeoman.app %>/scripts/config.js',
      paths: {
        templates: '../../.tmp/scripts/templates',
        almond: '<%= yeoman.app %>/bower_components/almond/almond'
      },
      // TODO: Figure out how to make sourcemaps work with grunt-usemin
      // https://github.com/yeoman/grunt-usemin/issues/30
      // generateSourceMaps: true,
      // required to support SourceMaps
      // http://requirejs.org/docs/errors.html#sourcemapcomments
      preserveLicenseComments: false,
      useStrict: true,
      wrap: true,
      include: [
        '#core/modules',
        'modules_widget',
        'app_widget',
        'main_widget'
      ]
    }
  

  },

  dist: {
    // Options: https://github.com/jrburke/r.js/blob/master/build/example.build.js
    options: {
      baseUrl: '<%= yeoman.app %>/scripts',
      optimize: 'none',
      out: '<%= yeoman.dist %>/scripts/main.js',
      // name: '../bower_components/almond/almond',
      mainConfigFile: '<%= yeoman.app %>/scripts/config.js',
      paths: {
        templates: '../../.tmp/scripts/templates',
        almond: '<%= yeoman.app %>/bower_components/almond/almond'
      },
      // TODO: Figure out how to make sourcemaps work with grunt-usemin
      // https://github.com/yeoman/grunt-usemin/issues/30
      // generateSourceMaps: true,
      // required to support SourceMaps
      // http://requirejs.org/docs/errors.html#sourcemapcomments
      preserveLicenseComments: false,
      useStrict: true,
      wrap: true,
      include: [
        /*'#core/modules',*/
        'modules',
        'app',
        'main',
        'moment-fr'
      ]
    }
  }
};
