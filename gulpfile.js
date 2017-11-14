/**
 * Created by Admin on 2017/11/14.
 */
var gulp = require('gulp'),               // 載入 gulp
    gulpSass = require('gulp-sass');    // 載入 gulp-sass
    concat = require('gulp-concat');
    livereload = require('gulp-livereload');
    browserSync = require('browser-sync').create();

gulp.task('watch', function () {
    var server = livereload();

    // app/**/*.*的意思是 app文件夹下的 任何文件夹 的 任何文件

    // gulp.watch('static/**/*.*', function (file) {
    //     server.changed(file.path);
    // });
    gulp.watch("templates/**/*.html").on('change', browserSync.reload);
    gulp.watch('static/sass/**/*.sass', ['styles']);
});

gulp.task('serve', ['styles'], function () {
    browserSync.init({
        proxy: "localhost:2000"   // hostname
    });
});

gulp.task('styles', function () {
    gulp.src('static/sass/**/*.sass')    // 指定要處理的 Scss 檔案目錄
        .pipe(gulpSass({          // 編譯 Scss
            outputStyle: 'compressed'
        }))
        .pipe(concat('app.css'))
        .pipe(gulp.dest('static/css'))  // 指定編譯後的 css 檔案目錄
        .pipe(browserSync.stream())
});

gulp.task('default', ['serve', 'watch']);