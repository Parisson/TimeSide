/*global module*/
'use strict';

module.exports = {
  dist: {
    files: {
      '<%= yeoman.dist %>/scripts/main.js': [
        '<%= yeoman.dist %>/scripts/main.js'
      ]
    }
  },
  widget : {
    files: {
      '<%= yeoman.dist %>/scripts/main_widget.js': [
        '<%= yeoman.dist %>/scripts/main_widget.js'
      ]
    }
  },
  requirejs: {
    files: {
      '<%= yeoman.dist %>/scripts/require.js': [
        '<%= yeoman.dist %>/scripts/require.js'
      ]
    }
  }
};
