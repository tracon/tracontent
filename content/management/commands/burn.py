import html
import mimetypes
import os
import re
import shutil
import tempfile

import boto3
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.utils.timezone import now

from tabulate import tabulate

from content.models import BlogCategory, BlogPost, Page, Redirect


MEDIA_URL_PROBE_KEY = "__burn_probe__"
REDIRECT_HTML_TEMPLATE = (
    '<!doctype html><meta charset="utf-8">'
    '<meta http-equiv="refresh" content="0;url={target}">'
)


class Command(BaseCommand):
    help = "Render every non-con2.fi site to static HTML and upload it to the static bucket"

    def add_arguments(self, parser):
        parser.add_argument("--output-dir", default=None)
        parser.add_argument("--bucket", default=os.environ.get("BURN_BUCKET_NAME", "static"))
        parser.add_argument("--site", default=None)
        parser.add_argument("--no-upload", action="store_true")

    def handle(self, *args, **options):
        output_dir = options["output_dir"] or tempfile.mkdtemp(prefix="burn-")
        resolved_bucket = options["bucket"]
        no_upload = options["no_upload"]

        s3 = None
        if not no_upload:
            if resolved_bucket == settings.AWS_STORAGE_BUCKET_NAME:
                raise CommandError(
                    f"Refusing to burn into {resolved_bucket!r}: same bucket as "
                    f"MINIO_BUCKET_NAME (the live media bucket)."
                )
            s3 = boto3.client(
                "s3",
                endpoint_url=os.environ["MINIO_ENDPOINT_URL"],
                aws_access_key_id=os.environ["MINIO_ACCESS_KEY_ID"],
                aws_secret_access_key=os.environ["MINIO_SECRET_ACCESS_KEY"],
            )

        media_url_prefix = get_media_url_prefix()

        # Don't let an unexpected exception in one page's rendering (eg. a broken
        # page_controller_code hook) abort the whole run -- surface it as a 500 instead.
        client = Client(raise_request_exception=False)

        sites = Site.objects.exclude(domain="con2.fi")
        if options["site"]:
            sites = sites.filter(domain=options["site"])

        self.stdout.write(f"Staging output to {output_dir}")

        report = {}

        for site in sites:
            self.stdout.write(f"Burning {site.domain}...")
            site_dir = os.path.join(output_dir, site.domain)
            key_map = {}  # local relative path -> (s3_key, content_type)
            media_keys_seen = set()
            failures = []
            shadowed = []

            for url, kind, obj in enumerate_site_urls(site):
                burn_url(
                    client,
                    site,
                    url,
                    kind,
                    obj,
                    site_dir,
                    media_url_prefix,
                    key_map,
                    media_keys_seen,
                    failures,
                    shadowed,
                )

            for redirect in Redirect.objects.filter(site=site):
                body = build_redirect_html(redirect.target)
                write_dual_key(site_dir, key_map, redirect.path, body, "text/html; charset=utf-8")

            copy_static_assets(site_dir)
            fetch_media_files(site_dir, media_keys_seen, failures)

            if not no_upload:
                upload_site_tree(s3, resolved_bucket, site_dir, site.domain, key_map)

            report[site.domain] = dict(failures=failures, shadowed=shadowed)

        self.print_report(report)

    def print_report(self, report):
        rows = [(domain, len(result["failures"]), len(result["shadowed"])) for domain, result in report.items()]
        total_failures = sum(len(result["failures"]) for result in report.values())

        self.stdout.write("")
        self.stdout.write(tabulate(rows, headers=["site", "# failures", "# shadowed by redirect"]))

        for domain, result in report.items():
            for url, status in result["failures"]:
                self.stdout.write(self.style.WARNING(f"{domain}: {url} -> {status}"))

        if total_failures:
            raise CommandError(f"{total_failures} URL(s) failed to render across all sites; see warnings above")


def get_media_url_prefix():
    # DEFAULT_FILE_STORAGE is S3Boto3Storage, so FileField.url (and CKEditor's
    # get_media_url()) never go through MEDIA_URL -- they return an absolute
    # Minio URL. Derive the real prefix from the storage backend itself instead
    # of assuming MEDIA_URL. Relies on AWS_QUERYSTRING_AUTH staying False
    # (hardcoded in settings.py), so this URL has no per-call signature.
    probe = default_storage.url(MEDIA_URL_PROBE_KEY)
    assert probe.endswith(MEDIA_URL_PROBE_KEY), f"Unexpected storage URL shape: {probe!r}"
    return probe[: -len(MEDIA_URL_PROBE_KEY)]


def enumerate_site_urls(site):
    current_time = now()
    urls = []

    for page in Page.objects.filter(site=site, public_from__lte=current_time):
        urls.append((page.get_local_url(), "page", page))

    for post in BlogPost.objects.filter(site=site, public_from__lte=current_time):
        urls.append(("/" + post.path, "blog_post", post))

    # BlogCategory has no public_from field -- always included.
    for category in BlogCategory.objects.filter(site=site):
        urls.append(("/" + category.path, "blog_category", category))

    urls.append(("/blog/", "blog_index", None))
    urls.append(("/blog/rss", "blog_rss", None))
    urls.append(("/blog/atom", "blog_atom", None))

    return urls


def burn_url(client, site, url, kind, obj, site_dir, media_url_prefix, key_map, media_keys_seen, failures, shadowed):
    response = client.get(url, HTTP_HOST=site.domain)

    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "text/html; charset=utf-8")
        body = response.content

        if kind in ("page", "blog_post", "blog_category", "blog_index"):
            # Image URLs baked into the rendered HTML point at the live Minio
            # tracontent bucket (see get_media_url_prefix), not a relative path
            # -- rewrite them to the relative /media/<key> path the burned
            # copy will actually be served from, so the static site doesn't
            # stay silently dependent on tracontent's Minio bucket forever.
            text = body.decode("utf-8", errors="replace")
            keys = extract_media_keys(text, media_url_prefix)
            for key in keys:
                text = text.replace(media_url_prefix + key, "/media/" + key)
            body = text.encode("utf-8")
            media_keys_seen.update(keys)

        if kind == "blog_rss":
            write_single_key(site_dir, key_map, "blog/rss", body, content_type)
        elif kind == "blog_atom":
            write_single_key(site_dir, key_map, "blog/atom", body, content_type)
        elif kind == "page" and obj.is_front_page:
            write_single_key(site_dir, key_map, "index.html", body, content_type)
        else:
            write_dual_key(site_dir, key_map, url, body, content_type)
    elif 300 <= response.status_code < 400:
        # A Redirect row shadows this Page/BlogPost/BlogCategory/blog index at the
        # same path -- correct app behavior, written separately by the Redirect loop.
        shadowed.append(url)
    else:
        failures.append((url, response.status_code))


def write_dual_key(site_dir, key_map, path, content, content_type):
    path = path.strip("/")
    # The bare (extensionless) variant can't share a filesystem slot with a
    # child page nested under the same path (eg. page "tapahtuma" vs. its
    # child "tapahtuma/tyovoima", which needs "tapahtuma/" to be a
    # directory) -- paths never contain dots (validate_path), so staging it
    # locally under a synthetic ".html" name is always unambiguous. The real
    # (extensionless) S3 key is restored by upload_site_tree via key_map.
    write_single_key(site_dir, key_map, path + ".html", content, content_type, s3_key=path)
    write_single_key(site_dir, key_map, path + "/index.html", content, content_type)


def write_single_key(site_dir, key_map, local_key, content, content_type, s3_key=None):
    full_path = os.path.join(site_dir, local_key)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "wb") as f:
        f.write(content)
    key_map[local_key] = (s3_key if s3_key is not None else local_key, content_type)


def extract_media_keys(html_body, media_url_prefix):
    pattern = re.escape(media_url_prefix) + r"([^\"'\)\s]+)"
    return set(re.findall(pattern, html_body))


def copy_static_assets(site_dir):
    shutil.copytree(settings.STATIC_ROOT, os.path.join(site_dir, "static"), dirs_exist_ok=True)


def fetch_media_files(site_dir, media_keys, failures):
    for key in media_keys:
        try:
            with default_storage.open(key, "rb") as source:
                data = source.read()
        except Exception as e:
            failures.append((f"media:{key}", str(e)))
            continue

        full_path = os.path.join(site_dir, "media", key)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(data)


def build_redirect_html(target):
    return REDIRECT_HTML_TEMPLATE.format(target=html.escape(target)).encode("utf-8")


def upload_site_tree(s3, bucket, site_dir, domain, key_map):
    for root, _dirs, files in os.walk(site_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, site_dir)
            if relative_path in key_map:
                s3_key, content_type = key_map[relative_path]
            else:
                # static/media files, never registered in key_map: local path == S3 key.
                s3_key = relative_path
                content_type = mimetypes.guess_type(relative_path)[0] or "application/octet-stream"
            with open(full_path, "rb") as f:
                s3.put_object(
                    Bucket=bucket,
                    Key=f"{domain}/{s3_key}",
                    Body=f.read(),
                    ContentType=content_type,
                )
