/*global module*/
'use strict';

module.exports = {
    options: {
        /*map: true, // inline sourcemaps 

        // or 
        map: {
            inline: false, // save all sourcemaps as separate files... 
            annotation: 'dist/css/maps/' // ...to the specified directory 
        },*/

        processors: [
            require('pixrem')(), // add fallbacks for rem units 
            require('autoprefixer-core')({browsers: 'last 2 versions'}), // add vendor prefixes 
            require('cssnano')() // minify the result 
        ]
    },
    dist: {
        files: {
            '.tmp/styles/main.css' : '.tmp/styles/main.css'
        }
    },
    dev: {
        files: {
            '.tmp/styles/main.css' : '.tmp/styles/main.css'
        }
    }
};
