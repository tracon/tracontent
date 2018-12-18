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

gulp.task("hitpoint2019:build", ["hitpoint2019:scripts"])

gulp.task("hitpoint2019:scripts", () => {
    var pipeline = browserify({
            entries: ["site_specific/hitpoint2019/static_src/js/hitpoint2019.js"],
            extensions: ["js"],
            debug: !production,
            cache: {},
            packageCache: {}
        })
        .bundle()
        .pipe(source("hitpoint2019.js"));

    if(production) {
        pipeline = pipeline.pipe(streamify(uglify()));
    }

    return pipeline.pipe(gulp.dest("site_specific/hitpoint2019/static/hitpoint2019/js"));
});

gulp.task("hitpoint2019:watch", () => {
    gulp.watch(["site_specific/hitpoint2019/static_src/less/**/*.less", "site_specific/hitpoint2019/static_src/js/**/*.js"], ["hitpoint2019:build"]);
});
