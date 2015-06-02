/**
 * This file is used to build ngHandsontable from `src/*`
 *
 * Installation:
 * 1. Install Grunt CLI (`npm install -g grunt-cli`)
 * 1. Install Grunt 0.4.0 and other dependencies (`npm install`)
 *
 * Build:
 * Execute `grunt` from root directory of this directory (where Gruntfile.js is)
 * To execute automatically after each change, execute `grunt --force default watch`
 *
 * Result:
 * building ngHandsontable will create files:
 *  - dist/ngHandsontable.js
 *  - dist/ngHandsontable.min.js
 *
 * See http://gruntjs.com/getting-started for more information about Grunt
 */
module.exports = function (grunt) {
  var myBanner = '/**\n' +
    ' * <%= pkg.name %> <%= pkg.version %>\n' +
    ' * \n' +
    ' * Copyright 2012-2015 Marcin Warpechowski\n' +
    ' * Licensed under the MIT license.\n' +
    ' * https://github.com/handsontable/ngHandsontable\n' +
    ' * Date: <%= (new Date()).toString() %>\n' +
    '*/\n\n';

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

		concat: {
      options: {
        banner: myBanner
      },
			new: {
				src: [
					'src/ie-shim.js',
					'src/ngHandsontable.js',
					'src/services/*.js',
					'src/directives/*.js'
				],
				dest: 'dist/ngHandsontable.js'
			}
    },

		uglify: {
      options: {
        banner: myBanner
      },
			"dist/ngHandsontable.min.js": ["dist/ngHandsontable.js"]
    },

    jshint: {
      options: {
        jshintrc:true
      },
      files:['src/**/*.js', 'src/*.js']
    },

		watch: {
      files: ['src/**/*', 'bower_components/**/*'],
      tasks: ['concat', 'uglify']
    }
  });

	grunt.registerTask('default', ['jshint', 'concat', 'uglify']);

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');
};