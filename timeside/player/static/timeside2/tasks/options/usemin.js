/*global module*/
'use strict';

module.exports = {
  html: ['<%= yeoman.dist %>/{,*/}*.html'],
  css: ['<%= yeoman.dist %>/styles/{,*/}*.css'],
  js: [
    '<%= yeoman.dist %>/scripts/{,*/}*.js',
  ],
  options: {
    assetsDirs: ['<%= yeoman.dist %>'],
    patterns: {
      js: [
        [/<img[^\>]+src=['"]([^"'\{]+)["']/gm, 'Update the JS with the new img filenames'],
        [/url\(\s*['"]([^"'\{]+)["']\s*\)/gm, 'Update the JS with background imgs, case there is some inline style'],
        [/<a[^\>]+href=['"]([^"'#\{]+)["']/gm, 'Update the JS with anchors images'],
        [/url\(\s*['"]?([^'"\)\{]+)['"]?\s*\)/gm, 'Update the JS to reference our revved images'],
        [/href\s*=\s*['"]([^'"\{]+)['"]/gm, 'Update the JS to reference our revved stylesheets'],
        [/<img[^\>]+src=\\['"]([^"'\{]+)\\["']/gm, 'Update the template with the new img filenames'],
        [/attr\(\s*['"]src["']\s*,\s*['"]([^"'\{]+)["']\s*\)/gm, 'Update the filename in attr() call'],
        [/['"](\/[^"'\{]+.(png|jpe?g|gif))["']/gm, 'Update image full path variable']
      ]
    }
  }
};
