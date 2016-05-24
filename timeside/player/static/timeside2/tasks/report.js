/* global module */
'use strict';

module.exports = function (grunt) {
  grunt.registerTask('report', function () {
    grunt.task.run(['plato:report']);
  });
};
