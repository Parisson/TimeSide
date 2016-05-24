module.exports = {
  build: [
    'clean:dist',
    'concurrent:build'
  ],
  buildicons: [
    'svgmin',
    'svgstore'
  ],
  default: [
    /*'lint-code',
    'lint-test',*/
    'build'
  ],
  dev: [
    /*'karma:unit:start',*/
    'watch'
  ]/*,
  data: [
    'clean:data',
    'wrap:data'
  ]*/
};
