const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const rename = require('gulp-rename');
const cleanCSS = require('gulp-clean-css');

// scss
function localGeneratorScss() {
  return gulp
    .src('./localStyles.scss')
    .pipe(sass())
    .pipe(rename('local.css' ))
    .pipe(cleanCSS())
    .pipe(gulp.dest('./'))
};

const buildMinifiedAssets = gulp.series(
  localGeneratorScss
);

gulp.task('watch_files', function(cb) {
  buildMinifiedAssets(function () {
    // Start watchers after initial minify build
    gulp.watch('./localStyles.scss', localGeneratorScss);
    cb();
  });
});

