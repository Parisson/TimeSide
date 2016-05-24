/*global module*/
'use strict';

module.exports = {
  options: {
    sassDir: '<%= yeoman.app %>/styles',
    cssDir: '.tmp/styles',
    imagesDir: '<%= yeoman.app %>/images',
    javascriptsDir: '<%= yeoman.app %>/scripts',
    fontsDir: '<%= yeoman.app %>/fonts',
    importPath: '<%= yeoman.app %>/bower_components',
    httpImagesPath: '/images',
    httpGeneratedImagesPath: '/images',
    relativeAssets: false,
    trace: true
  },
  dist: {
    options: {
      outputStyle: 'compressed'
    }
  },
  server: {
    options: {
      debugInfo: true
    }
  }
};
