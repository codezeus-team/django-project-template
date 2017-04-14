var autoprefixer = require('gulp-autoprefixer');
var browserSync  = require('browser-sync');
var config       = require('../config').sass;
var gulp         = require('gulp');
var handleErrors = require('../utils/handleErrors');
var sass         = require('gulp-sass');

gulp.task('sass', function () {
  return gulp.src(config.src)
    .pipe(sass(config.settings))
    .on('error', handleErrors)
    .pipe(autoprefixer({ browsers: ['last 2 version'] }))
    .pipe(gulp.dest(config.dest))
    .pipe(browserSync.reload({stream:true}));
});
