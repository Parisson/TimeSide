/*global module*/
'use strict';

module.exports = {
  options: {
    prefix: 'icon-',
    includedemo: true,
    svg: {
      xmlns: 'http://www.w3.org/2000/svg',
      'xmlns:xlink' : "http://www.w3.org/1999/xlink",
      style: 'width:0;height:0;visibility:hidden;'
    }
  },
  default: {
    files: {
      '<%= yeoman.app %>/assets/icons.svg': ['<%= yeoman.app %>/assets/svg/icons/*.min.svg']
    },
  }
};
