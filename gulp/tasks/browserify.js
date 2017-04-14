var argv            = require('yargs').argv;
var browserSync     = require('browser-sync');
var browserify      = require('browserify');
var bundleLogger    = require('../utils/bundleLogger');
var config          = require('../config');
var gulp            = require('gulp');
var gutil           = require('gulp-util');
var handleErrors    = require('../utils/handleErrors');
var isWatching      = require('../utils/isWatching');
var source          = require('vinyl-source-stream');
var watchify        = require('watchify');

var production = !!argv.production;

gulp.task('browserify', function(callback) {
  var bundleQueue = config.browserify.bundleConfigs.length;

  var browserifyThis = function(bundleConfig) {
    var bundler = browserify({
      cache: {},
      packageCache: {},
      fullPaths: true,
      entries: bundleConfig.entries,
      extensions: config.browserify.extensions,
      transform: config.browserify.transform,
      debug: production ? false : true
    });

    var bundle = function() {
      bundleLogger.start(bundleConfig.outputName);

      return bundler
        .bundle()
        .on('error', handleErrors)
        .pipe(source(bundleConfig.outputName))
        .pipe(gulp.dest(bundleConfig.dest))
        .on('end', reportFinished);
    };

    if (isWatching) {
      gutil.log('Enabling Watchify for Browserify');
      bundler = watchify(bundler);
      bundler.on('update', bundle);
    }

    var reportFinished = function() {
      bundleLogger.end(bundleConfig.outputName);

      if (bundleQueue) {
        bundleQueue--;
        if (bundleQueue === 0) {
          callback();
          browserSync.reload();
        } else {
          browserSync.reload();
        }
      }
    };

    return bundle();
  };

  config.browserify.bundleConfigs.forEach(browserifyThis);
});
