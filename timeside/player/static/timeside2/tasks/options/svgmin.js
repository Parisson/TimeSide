/*global module*/
'use strict';

module.exports = {
  options: {
    plugins: [
      {
        removeViewBox: false
      },
      {
        removeUselessStrokeAndFill: false
      }
    ]
  },
  dist: {
    files: [{
      expand: true,
      cwd: './assets/svg',
      src: ['**/*.svg'],
      dest: '<%= yeoman.app %>/assets/svg',
      ext: '.min.svg'
    }]
  }
};
