/**
 * Created by Admin on 2017/11/14.
 */
var gulp = require('gulp'),               // 載入 gulp
    gulpSass = require('gulp-sass');    // 載入 gulp-sass
    concat = require('gulp-concat');
    livereload = require('gulp-livereload');

gulp.task('watch', function () {
    livereload.listen();
    gulp.watch('static/sass/**/*.sass', ['styles']);
    gulp.watch('templates/**/*.html', ['styles']);
});

gulp.task('styles', function () {
    gulp.src('static/sass/**/*.sass')    // 指定要處理的 Scss 檔案目錄
        .pipe(gulpSass({          // 編譯 Scss
            outputStyle: 'compressed'
        }))
        .pipe(concat('app.css'))
        .pipe(gulp.dest('static/css'))  // 指定編譯後的 css 檔案目錄
        .pipe(livereload())
});