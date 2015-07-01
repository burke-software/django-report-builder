var gulp = require('gulp');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');

 // Minify JS
gulp.task('dist', function() {
  return gulp.src('massautocomplete.js')
    .pipe(rename({suffix: '.min'}))
    .pipe(uglify())
    .pipe(gulp.dest(''));
});
 // Default Task
gulp.task('default', ['dist']);
