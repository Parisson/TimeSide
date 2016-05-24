/*global module*/
'use strict';

module.exports = {
  dist: {
    files: [{
      src: ['<%= yeoman.dist %>/images/{,*/}*.{png,jpg,jpeg,gif,webp}']
    }, {
      src: ['<%= yeoman.dist %>/scripts/*.js']
    }, {
      src: ['<%= yeoman.dist %>/styles/*.css']
    }]
  }
};
