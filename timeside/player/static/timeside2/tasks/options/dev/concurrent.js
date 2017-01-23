/* global module */
'use strict';

module.exports = {
  options: {
    logConcurrentOutput: true
  },
  server: {
    tasks: [
      'handlebars',
      'style'/*,
      'data',
      'fixtures'*/
    ]
  },
  build: {
    tasks: [
      'handlebars',
      'style',
      'buildit'
    ]
  }
};
