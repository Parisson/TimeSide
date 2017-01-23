/* global module */
'use strict';

module.exports = function (grunt) {
  grunt.registerTask('serve', function (target) {
    grunt.task.run([
      'clean:server',
      'concurrent:server',
      'connect:livereload',
      'open:server',
      /*'karma:unit:start',*/
      'watch'
    ]);
  });
};
