/* global module */
'use strict';

module.exports = function (grunt) {
  grunt.registerTask('buildit', function () {
    grunt.task.run([
      'useminPrepare',
      'requirejs:dist',
      'concat',
      'cssmin',
      'copy:dist',
      'copy:nonminified',
      'replace:nonminified',
      'usemin'
    ]);
  });
};
