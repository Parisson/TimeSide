module.exports = {
  options: {  // this options only affect the compile task
    console: true,
    debugger: false
  },
  clean: {
    src: '<%= yeoman.dist %>/scripts/main.js',
    dest: '<%= yeoman.dist %>/scripts/main.js'
  }
};
