/*global module*/
'use strict';

module.exports = function (grunt) {
  return {
    compile: {
      options: {
        amd: true,
        namespace: 'templates',
        processName: function (filePath) {
          var matches = filePath.match(new RegExp('scripts/(modules/(\\w+)/templates|templates)\/(.*).hbs'));
          if (!matches) {
            return filePath;
          }
          grunt.verbose.debug('found template [' + matches[3] + '] in module [' + matches[2] + ']');
          return (matches[2] ? matches[2] + '/' : '') + matches[3];
        },
        processContent: function (content) {
          content = content.replace(/^[\x20\t]+/mg, '').replace(/[\x20\t]+$/mg, '');
          content = content.replace(/^[\r\n]+/, '').replace(/[\r\n]*$/, '');
          content = content.replace(/\n/g, '');
          return content;
        }
      },
      files: {
        '.tmp/scripts/templates.js': [
          '<%= yeoman.app %>/bower_components/qeopa-webapp-core/lib/scripts/modules/**/templates/**/*.hbs',
          '<%= yeoman.app %>/scripts/templates/**/*.hbs',
          '<%= yeoman.app %>/scripts/modules/**/templates/**/*.hbs'
        ]
      }
    }
  };
};
