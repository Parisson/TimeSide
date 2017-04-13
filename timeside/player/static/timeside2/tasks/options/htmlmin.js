/*global module*/
'use strict';

module.exports = {
  dist: {
    options: {
      removeComments: true,
      removeCommentsFromCDATA: true,
      // https://github.com/yeoman/grunt-usemin/issues/44
      collapseWhitespace: true,
      collapseBooleanAttributes: true,
      removeAttributeQuotes: true,
      removeRedundantAttributes: true,
      useShortDoctype: true,
      removeEmptyAttributes: true,
      removeOptionalTags: true
    },
    files: [{
      expand: true,
      cwd: '<%= yeoman.dist %>',
      src: '*.html',
      dest: '<%= yeoman.dist %>'
    }]
  }
};
