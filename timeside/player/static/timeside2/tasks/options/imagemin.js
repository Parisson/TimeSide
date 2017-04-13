/*global module*/
'use strict';

module.exports = {
  dist: {
    files: [{
      expand: true,
      cwd: '<%= yeoman.app %>/images',
      src: '{,*/}*.{png,jpg,jpeg}',
      dest: '<%= yeoman.dist %>/images'
    }]
  }
};
