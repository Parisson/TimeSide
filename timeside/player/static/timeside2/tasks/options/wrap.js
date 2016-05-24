/*global module*/
'use strict';

module.exports = {
  
  data: {
    expand: true,
    cwd: 'data',
    src: ['**/*.json'],
    dest: 'app/data/',
    ext: '.js',
    options: {
      wrapper: [
        'define(', ');'
      ],
      separator: ''
    }
  }
};
