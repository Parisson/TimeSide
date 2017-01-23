/*global module*/
'use strict';

module.exports = {
  requirejs: {
    options: {
      patterns: [{
        match: /src="bower_components\/requirejs\/require.js"/g,
        replacement: 'src="scripts/require.js"'
      }],
      usePrefix: false
    },
    files: [{
      src: ['<%= yeoman.dist %>/index.html'],
      dest: '<%= yeoman.dist %>/index.html'
    }]
  },
  ckeditor: {
    options: {
      patterns: [{
        match: /src="\/bower_components\/ckeditor\/ckeditor.js"/g,
        replacement: 'src="scripts/ckeditor/ckeditor.js"'
      }],
      usePrefix: false
    },
    files: [{
      src: ['<%= yeoman.dist %>/index.html'],
      dest: '<%= yeoman.dist %>/index.html'
    }]
  },
  nonminified: {
    options: {
      patterns: [{
        match: /src="bower_components\/requirejs\/require.js"/g,
        replacement: 'src="scripts/require.js"'
      }, {
        match: /src="bower_components\/svg4everybody\/svg4everybody.ie8.js"/g,
        replacement: 'src="scripts/svg4everybody.ie8.js"'
      }],
      usePrefix: false
    },
    files: [{
      src: ['<%= yeoman.dist %>/index.html'],
      dest: '<%= yeoman.dist %>/index.html'
    }]
  }
};
