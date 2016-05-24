/* global require, module */
'use strict';

module.exports = function (grunt) {
  // show elapsed time at the end
  require('time-grunt')(grunt);

  var path = require('path');

  function loadConfig (path) {
    var glob = require('glob');
    var object = {};
    var key;

    glob.sync('*', {cwd: path}).forEach(function (option) {
      key = option.replace(/\.js$/,'');
      var req;
      try {
        req = require(path + option);
        object[key] = 'function' === typeof req ? req(grunt) : req;
      }
      catch (e) {}
    });

    return object;
  }

  // configurable paths
  var yeomanConfig = {
    app: 'app',
    dist: 'dist',
    doc: 'docs'
  };

  var config = {
    yeoman: yeomanConfig,
    livereload: 35729
  };

  grunt.util._.extend(config, loadConfig('./tasks/options/'));

  // target specific configuration
  var env = grunt.option('target') || 'dev';
  if (env) {
    grunt.util._.extend(config, loadConfig('./tasks/' + env + '/'));
    grunt.util._.extend(config, loadConfig('./tasks/options/' + env + '/'));
  }

  grunt.initConfig(config);

  require('load-grunt-config')(grunt, {
    configPath: path.join(process.cwd(), 'tasks'),
    init: false,
    config: config,
    jitGrunt: {
      useminPrepare: 'grunt-usemin'
    }
  });

};
