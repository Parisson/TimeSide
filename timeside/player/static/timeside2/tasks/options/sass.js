/*global module*/
'use strict';

module.exports = {
  options: {
    loadPath: [
      '<%= yeoman.app %>/bower_components/radiooooo_core/lib/styles',
      '<%= yeoman.app %>/bower_components/radiooooo_core/lib/styles/vendors'
    ]
  },
  dist: {
    options: {
      style: 'compressed'
    },
    files: {
      '.tmp/styles/main.css': '<%= yeoman.app %>/styles/main.scss'
    }
  },
  server: {
    options: {
      debugInfo: true
    },
    files: {
      '.tmp/styles/main.css': '<%= yeoman.app %>/styles/main.scss'
    }
  }
};
