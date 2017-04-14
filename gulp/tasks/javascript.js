var browserSync  = require('browser-sync');
var config       = require('../config').js;
var gulp         = require('gulp');
var handleErrors = require('../utils/handleErrors');

gulp.task('javascript', function () {
  return gulp.src(config.src)
    .on('error', handleErrors)
    .pipe(gulp.dest(config.dest))
    .pipe(browserSync.reload({stream:true}));
});
