var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var minifyCSS = require('gulp-minify-css');
var ngAnnotate = require('gulp-ng-annotate');
var closure = require('gulp-jsclosure');
var paths = {
    scripts: ['base/static/js/sportomatics.js', 'base/static/js/controllers/*.js'],
    libs: ['base/static/js/libs/*.js']
};

gulp.task('scripts', function () {
    gulp.src(paths.scripts)
        .pipe(ngAnnotate())
        //.pipe(uglify())
        .pipe(closure())
        .pipe(concat('app.js'))
        .pipe(gulp.dest('./base/static/build/'))
});

gulp.task('libs', function () {
    gulp.src(paths.libs)
        .pipe(ngAnnotate())
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
    gulp.watch(paths.scripts, ['scripts']);
    gulp.watch(paths.libs, ['libs']);
});

gulp.task('default', ['watch', 'scripts','libs']);