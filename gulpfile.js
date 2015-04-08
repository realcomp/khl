var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var minifyCSS = require('gulp-minify-css');
var ngAnnotate = require('gulp-ng-annotate');
var closure = require('gulp-jsclosure');
var coffee = require('gulp-coffee');
var paths = {
    scripts: ['base/static/js/sportomatics.js', 'base/static/js/classes/*.js',  'base/static/js/router.js', 'base/static/js/services/*.js', 'base/static/js/controllers/*.js'],
    libs: ['base/static/js/libs/*.js']
};

gulp.task('coffee-controllers', function() {
  gulp.src('base/static/js/controllers/*.coffee')
      .pipe(coffee({bare: true}))
      .pipe(gulp.dest('base/static/js/controllers'))
});

gulp.task('coffee-services', function() {
  gulp.src('base/static/js/services/*.coffee')
      .pipe(coffee({bare: true}))
      .pipe(gulp.dest('base/static/js/services'))
});

gulp.task('coffee-classes', function() {
    gulp.src('base/static/js/classes/*.coffee')
        .pipe(coffee({bare: true}))
        .pipe(gulp.dest('base/static/js/classes'))
});

gulp.task('scripts', function () {
    gulp.src(paths.scripts)
        //.pipe(ngAnnotate())
        //.pipe(uglify())
        // .pipe(closure())
        .pipe(concat('app.js'))
        .pipe(gulp.dest('./base/static/build/'))
});

gulp.task('libs', function () {
    gulp.src(paths.libs)
        //.pipe(ngAnnotate())
        .pipe(uglify())
        .pipe(concat('libs.min.js'))
        .pipe(gulp.dest('./base/static/build/'))
});

gulp.task('minify-css', function() {
    gulp.src(paths.css)
        .pipe(minifyCSS({keepBreaks:true}))
        .pipe(concat('app.css'))
        .pipe(gulp.dest('./build/'))
});

gulp.task('watch', function() {
    gulp.watch(['base/static/js/controllers/*.coffee'], ['coffee-controllers']);
    gulp.watch(['base/static/js/services/*.coffee'], ['coffee-services']);
    gulp.watch(['base/static/js/classes/*.coffee'], ['coffee-classes']);
    gulp.watch(paths.scripts, ['scripts']);
    gulp.watch(paths.libs, ['libs']);
});

gulp.task('default', ['watch', 'coffee-controllers', 'coffee-services', 'coffee-classes', 'scripts', 'libs']);
