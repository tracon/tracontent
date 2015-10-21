import autoprefixer from "gulp-autoprefixer";
import browserify from "browserify";
import cssnano from "gulp-cssnano";
import gulp from "gulp";
import gutil from "gulp-util";
import less from "gulp-less";
import rename from "gulp-rename";
import size from "gulp-size";
import source from "vinyl-source-stream";
import sourcemaps from "gulp-sourcemaps";
import streamify from "gulp-streamify";
import uglify from "gulp-uglify";
import {production} from "./gulp-env";

gulp.task("hitpoint2015:build", ["hitpoint2015:styles", "hitpoint2015:scripts"])

gulp.task("hitpoint2015:styles", () => {
    return gulp.src("site_specific/hitpoint2015/static_src/less/hitpoint2015.less")
        .pipe(sourcemaps.init())
        .pipe(less({
            paths: [
                '.',
                './node_modules/bootstrap-less',
            ]
        }))
        .pipe(autoprefixer())
        .pipe((production ? cssnano() : gutil.noop()))
        .pipe(rename("hitpoint2015.css"))
        .pipe(size())
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest("site_specific/hitpoint2015/static/hitpoint2015/css"));
});

gulp.task("hitpoint2015:scripts", () => {
    var pipeline = browserify({
            entries: ["site_specific/hitpoint2015/static_src/js/hitpoint2015.js"],
            extensions: ["js"],
            debug: !production,
            cache: {},
            packageCache: {}
        })
        .bundle()
        .pipe(source("hitpoint2015.js"));

    if(production) {
        pipeline = pipeline.pipe(streamify(uglify()));
    }

    return pipeline.pipe(gulp.dest("site_specific/hitpoint2015/static/hitpoint2015/js"));
});

gulp.task("hitpoint2015:watch", () => {
    gulp.watch(["site_specific/hitpoint2015/static_src/less/**/*.less", "site_specific/hitpoint2015/static_src/js/**/*.js"], ["hitpoint2015:build"]);
});
