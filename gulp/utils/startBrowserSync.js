var _           = require('lodash');
var browserSync = require('browser-sync');
var config      = require('../config');
var gulp        = require('gulp');
var gutil       = require('gulp-util');

var bsConfig    = config.browserSync.all;
var mode        = config.browserSync.mode + "Options";

_.assign(bsConfig, config.browserSync[mode]);

var startBrowserSync = function() {
  if (global.isBuilding === true){
    setTimeout(startBrowserSync, 100);
  } else {
    gutil.log('Build complete, starting BrowserSync');
    browserSync(bsConfig);
  }
};

module.exports = startBrowserSync;
