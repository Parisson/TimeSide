/*global module*/
'use strict';

module.exports = {
  dist: {
    files: [
      {
        expand: true,
        dot: true,
        cwd: '<%= yeoman.app %>',
        dest: '<%= yeoman.dist %>',
        src: [
          '*.html',
          '*.{ico,txt}',
          '.htaccess',
          'images/**/*.{webp,gif,jpg,jpeg,png}',
          'fonts/{,*/}*.*',
          'assets/{,*/}*.{svg,png,jpg,jpeg}',
          'styles/fonts/{,*/}*.*',
          'styles/images/{,*/}*.*'
        ]
      },
      {
        expand: true,
        dot: true,
        cwd: '<%= yeoman.app %>/bower_components/ckeditor',
        dest: '<%= yeoman.dist %>/scripts/ckeditor',
        src: '**/*'
      }
    ]
  },
  widget: {
    files: [
      {
        expand: true,
        dot: true,
        cwd: '<%= yeoman.app %>',
        dest: '<%= yeoman.dist %>',
        src: [
          '*.html',
          '*.{ico,txt}',
          '.htaccess',
          'images/**/*.{webp,gif,jpg,jpeg,png}',
          'fonts/{,*/}*.*',
          'assets/{,*/}*.{svg,png,jpg,jpeg}'
        ]
      }
    ]
  },
  nonminified: {
    files: [
      {
        src: '<%= yeoman.app %>/bower_components/requirejs/require.js',
        dest: '<%= yeoman.dist %>/scripts/require.js'
      },
      {
        src: '<%= yeoman.app %>/bower_components/svg4everybody/svg4everybody.ie8.js',
        dest: '<%= yeoman.dist %>/scripts/svg4everybody.ie8.js'
      }
    ]
  },
  requirejs: {
    files: [{
      expand: true,
      cwd: '<%= yeoman.app %>/bower_components/requirejs/',
      src: 'require.js',
      dest: '<%= yeoman.dist %>/scripts/'
    }]
  },
};
