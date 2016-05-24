/* global module */
'use strict';

module.exports = function (grunt) {
  grunt.registerTask('buildit', function () {
    grunt.task.run([
      'useminPrepare',
      'requirejs:dist',
      'concat',
      'cssmin',
      'groundskeeper',
      'uglify:dist',
      'copy:dist',
      'copy:requirejs',
      'uglify:requirejs',
      'replace:requirejs',
      'replace:ckeditor',
      /*'uglify:generated',
      'imagemin',*/
      'filerev',
      'usemin',
      'htmlmin'
    ]);
  });
};
