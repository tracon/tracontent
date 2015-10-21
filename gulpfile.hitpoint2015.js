import gulp from "gulp";
import gutil from "gulp-util";
import less from "gulp-less";
import autoprefixer from "gulp-autoprefixer";
import sourcemaps from "gulp-sourcemaps";
import cssnano from "gulp-cssnano";
import rename from "gulp-rename";
import size from "gulp-size";
import {production} from "./gulp-env";

gulp.task("style:build", () => {
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

gulp.task("style:watch", () => {
    gulp.watch("site_specific/hitpoint2015/static_src/less/**/*.less", ["style:build"]);
});
