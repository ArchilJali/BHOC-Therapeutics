#!/usr/bin/env python3
"""Read-only source audit of images, social previews and JSON-LD media URLs.

Run on a checkout of current main, not on the stale SEO preview branch:
python3 seo-bot/media_url_lint.py --root . --out _seo_output/media-url-integrity.json
No HTTP requests, source changes or publication. Checks .html and .htm.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

BAD_EMBEDDED_SCHEME = re.compile(r"https?://[^\"'\s<>]*https?://", re.I)
IMAGE_META = {"og:image", "og:image:secure_url", "twitter:image", "twitter:image:src"}
SKIP = {".git", "node_modules", "_site", "_seo_output", "seo-runner"}


def validate_url(value: str, root: Path) -> str | None:
    value = html.unescape(value).strip()
    if not value or value.startswith(("data:", "blob:", "#")):
        return None
    if BAD_EMBEDDED_SCHEME.search(value):
        return "multiple_concatenated_absolute_urls"
    try:
        parsed = urlsplit(value)
    except ValueError:
        return "invalid_url"
    if parsed.scheme in ("http", "https"):
        if not parsed.hostname:
            return "invalid_absolute_url"
        if "https:" in parsed.path or "http:" in parsed.path:
            return "embedded_scheme_in_path"
        return None  # External HTTP success is NOT established by this audit.
    if parsed.scheme or value.startswith("//"):
        return None  # May be a valid URI of a different type.
    if value.startswith("/"):
        path = (root / unquote(parsed.path).lstrip("/")).resolve()
        if not path.is_relative_to(root.resolve()):
            return "local_path_escapes_root"
        if not path.is_file():
            return "local_media_asset_missing_in_source"
    return None


class MediaHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.media: list[tuple[str, str]] = []
        self.in_jsonld = False
        self.json_text: list[str] = []
        self.json_errors = 0

    def handle_starttag(self, tag: str, attrs):
        attrs = dict(attrs)
        if tag in ("img", "source"):
            if attrs.get("src"):
                self.media.append((tag + ".src", attrs["src"]))
            if attrs.get("srcset"):
                for part in attrs["srcset"].split(","):
                    token = part.strip().split(" ", 1)[0]
                    if token:
                        self.media.append((tag + ".srcset", token))
        if tag == "meta":
            prop = (attrs.get("property") or attrs.get("name") or "").lower()
            if prop in IMAGE_META and attrs.get("content"):
                self.media.append(("meta." + prop, attrs["content"]))
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.in_jsonld = True
            self.json_text = []

    def handle_data(self, data: str):
        if self.in_jsonld:
            self.json_text.append(data)

    def handle_endtag(self, tag: str):
        if tag != "script" or not self.in_jsonld:
            return
        self.in_jsonld = False
        try:
            payload = json.loads("".join(self.json_text))
        except (ValueError, TypeError):
            self.json_errors += 1
            return
        self.walk_schema(payload)

    def walk_schema(self, node, in_image=False):
        if isinstance(node, list):
            for item in node:
                self.walk_schema(item, in_image)
        elif isinstance(node, dict):
            type_field = node.get("@type", [])
            is_image_object = type_field == "ImageObject" or (
                isinstance(type_field, list) and "ImageObject" in type_field
            )
            active = in_image or is_image_object
            for key, value in node.items():
                if key in ("image", "thumbnailUrl", "logo"):
                    if isinstance(value, str):
                        self.media.append(("schema." + key, value))
                    else:
                        self.walk_schema(value, True)
                elif key in ("url", "contentUrl") and active and isinstance(value, str):
                    self.media.append(("schema." + key, value))
                elif isinstance(value, (dict, list)):
                    self.walk_schema(value, active)


def scan_file(file_path: Path, root: Path) -> dict:
    parser = MediaHTML()
    parser.feed(file_path.read_text(encoding="utf-8", errors="replace"))
    bad = []
    for location, value in parser.media:
        issue = validate_url(value, root)
        if issue:
            bad.append({"field": location, "url": value, "issue": issue})
    return {"path": file_path.relative_to(root).as_posix(),
            "media_urls_checked": len(parser.media),
            "jsonld_parse_errors": parser.json_errors, "issues": bad}


def scan(root: Path) -> dict:
    root = root.resolve()
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in {".html", ".htm"}
        and not any(part in SKIP for part in p.relative_to(root).parts)
    )
    rows = [scan_file(p, root) for p in files]
    bad = [dict(path=r["path"], **issue) for r in rows for issue in r["issues"]]
    return {
        "audit_type": "source_only_media_url_integrity",
        "files_checked": len(files),
        "media_urls_checked": sum(r["media_urls_checked"] for r in rows),
        "issues": bad,
        "issue_counts": dict(Counter(x["issue"] for x in bad)),
        "limitations": [
            "No network fetch or image-pixel/ALT accuracy validation.",
            "An existing valid URL may still return an HTTP error or wrong image.",
            "Google indexing and social cache state are not assessed.",
        ],
    }


def self_test():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "assets/news").mkdir(parents=True)
        (root / "assets/news/good.webp").write_bytes(b"example")
        broken = "https://raw.githubusercontent.com/user/repo/mainhttps://raw.githubusercontent.com/user/repo/main/image.webp"
        sample = (
            '<meta property="og:image" content="' + broken + '">'
            '<img src="' + broken + '">'
            '<img src="/assets/news/good.webp">'
            '<script type="application/ld+json">'
            + json.dumps({"@type": "NewsArticle", "image": {"@type": "ImageObject", "url": broken}})
            + "</script>"
        )
        (root / "index.htm").write_text(sample, encoding="utf-8")
        result = scan(root)
        assert result["files_checked"] == 1, result
        assert result["issue_counts"] == {"multiple_concatenated_absolute_urls": 3}, result
        assert validate_url("/assets/news/good.webp", root) is None
        assert validate_url("/assets/news/missing.webp", root) == "local_media_asset_missing_in_source"
    print("media-url-lint self-test OK")


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--root", type=Path, default=Path("."))
    args.add_argument("--out", type=Path)
    args.add_argument("--self-test", action="store_true")
    options = args.parse_args()
    if options.self_test:
        self_test()
        return
    result = scan(options.root)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if options.out:
        options.out.parent.mkdir(parents=True, exist_ok=True)
        options.out.write_text(payload + "\n", encoding="utf-8")
    print("BHOC_MEDIA_URL_ISSUES=" + json.dumps({
        "files_checked": result["files_checked"],
        "media_urls_checked": result["media_urls_checked"],
        "issue_counts": result["issue_counts"],
        "first_issues": result["issues"][:12],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
