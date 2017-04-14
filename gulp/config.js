/**
 * Gulp Configuration
 *
 * A set of paths and options for Gulp to properly build our application.
 */

// Define Global Variables for our main object
var dest = './{{project_name}}/static/';
var src = './{{project_name}}/dev/';

module.exports = {
  // Define module variables for easy access to source and destination dirs
  src: src,
  dest: dest,

  // BrowserSync allows us to have livereload as we work on files
  browserSync: {
    mode: 'proxy',
    all: {
      port: process.env.PORT || 8000,
      open: true
    },
    debug: {
      logFileChanges: true,
      logLevel: "debug"
    },
    serverOptions: {
      files: [
        dest + "/**",
        "!" + dest + "/**.map"
      ],
    },
    proxyOptions: {
      proxy: '127.0.0.1:8000'
    }
  },

  // Compile our SCSS files
  sass: {
    src: [
      src + 'scss/screen.scss',
      src + 'scss/**/*.scss'
    ],
    dest: dest + 'css',
    settings: {}
  },

  // Compile our JS files
  js: {
    src: [
      src + 'js/app.js',
      src + 'js/**/*.js'
    ],
    dest: src + 'js',
    settings: {
      bare: true
    }
  },

  // Handle minimizing JS Files into a single file
  browserify: {
    extensions: [],
    transform: [],
    bundleConfigs: [
      {
        entries: src + '/js/app.js',
        dest: dest + '/js',
        outputName: 'app.js'
      }
    ]
  },

  // Django Templates
  templates: {
    src: [
      src + '../apps/*/templates/*.html',
      src + '../apps/*/templates/**/*.html',
      src + '../templates/*.html'
    ]
  }
}
