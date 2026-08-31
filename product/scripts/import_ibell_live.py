#!/usr/bin/env python3
"""
One-off importer: push the scraped iBELL catalog into the LIVE storefront via its REST API.

This is NOT a Django management command - it only speaks HTTP to the deployed API, so it
runs from wherever the JSON + photos live (the dev machine) with no server access.

Rules:
  * Only products that have a matching local photo are imported.
  * Idempotent: a product whose name already exists on the site is skipped.

Usage:
    export YESSARE_ADMIN_USER=tools
    export YESSARE_ADMIN_PASS='...'
    python3 product/scripts/import_ibell_live.py --dry-run
    python3 product/scripts/import_ibell_live.py

Needs: requests  (pip install requests)
"""
import argparse
import json
import mimetypes
import os
import re
import sys
from decimal import Decimal, InvalidOperation

import requests

DEFAULT_API = os.environ.get("API_BASE", "https://api.yessaretools.com")
DEFAULT_JSON = "/home/das/Downloads/ibell_products.json"
DEFAULT_PHOTOS = "/home/das/Downloads/ibell_photos"

BRAND_NAME = "iBELL"


# --- name / photo matching (mirrors product/management/commands/import_ibell_catalog.py) ---
def slugify(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9.\-]", "_", name)


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def parse_price(raw: str) -> Decimal:
    cleaned = re.sub(r"[^0-9.]", "", raw or "")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return Decimal("0")


def build_image_index(photos_dir):
    exact, fuzzy = {}, {}
    for root, _dirs, files in os.walk(photos_dir):
        for fname in files:
            stem = os.path.splitext(fname)[0]
            path = os.path.join(root, fname)
            exact.setdefault(stem, path)
            fuzzy.setdefault(normalize(stem), path)
    return exact, fuzzy


def find_image(name, exact, fuzzy):
    s = slugify(name)
    if s in exact:
        return exact[s]
    n = normalize(name)
    return fuzzy.get(n)


# --- API client ---
class Api:
    def __init__(self, base):
        self.base = base.rstrip("/")
        self.s = requests.Session()

    def login(self, user, password):
        r = self.s.post(
            f"{self.base}/auth/login/",
            json={"username": user, "password": password},
            timeout=30,
        )
        if r.status_code != 200:
            sys.exit(f"Login failed ({r.status_code}): {r.text}")
        self.s.headers["Authorization"] = f"Bearer {r.json()['access']}"

    def brand_id(self, name):
        r = self.s.get(f"{self.base}/brand/all/", timeout=30)
        r.raise_for_status()
        for b in r.json().get("response", []):
            if (b.get("name") or "").strip().lower() == name.lower():
                return b["id"]
        return None

    def ensure_category(self, name):
        r = self.s.post(f"{self.base}/product/category/", json={"name": name}, timeout=30)
        if r.status_code in (200, 201):
            return r.json()["category"]["id"]
        # already exists (or other) -> look it up
        g = self.s.get(f"{self.base}/product/category/", timeout=30)
        g.raise_for_status()
        for c in g.json().get("response", []):
            if c["name"].strip().lower() == name.strip().lower():
                return c["id"]
        sys.exit(f"Could not create or find category {name!r}: {r.status_code} {r.text}")

    def existing_product_names(self):
        names = set()
        page = 1
        while True:
            r = self.s.get(f"{self.base}/product/", params={"page": page}, timeout=30)
            if r.status_code == 404:
                break
            r.raise_for_status()
            data = r.json()
            for p in data.get("results", []):
                names.add((p.get("name") or "").strip().lower())
            if not data.get("next"):
                break
            page += 1
        return names

    def add_product(self, payload):
        r = self.s.post(f"{self.base}/product/add/", json={"product": payload}, timeout=60)
        if r.status_code not in (200, 201):
            raise RuntimeError(f"add_product {r.status_code}: {r.text}")
        return r.json()["product_id"]

    def upload_image(self, product_id, path):
        mime = mimetypes.guess_type(path)[0] or "image/jpeg"
        with open(path, "rb") as fh:
            r = self.s.post(
                f"{self.base}/product/images/upload/",
                data={"product": str(product_id)},
                files={"images": (os.path.basename(path), fh, mime)},
                timeout=120,
            )
        if r.status_code not in (200, 201):
            raise RuntimeError(f"upload_image {r.status_code}: {r.text}")


def iter_unique_products(data):
    """Yield (name, entry, top_category) once per unique lowercased name."""
    data = dict(data)
    data.pop("meta", None)
    seen = set()
    for top_category, subcats in data.items():
        for _sub, info in subcats.items():
            for entry in info.get("products", []):
                name = (entry.get("name") or "").strip()
                if not name or name.lower() in seen:
                    continue
                seen.add(name.lower())
                yield name, entry, top_category


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--json", default=DEFAULT_JSON)
    ap.add_argument("--photos", default=DEFAULT_PHOTOS)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    user = os.environ.get("YESSARE_ADMIN_USER")
    password = os.environ.get("YESSARE_ADMIN_PASS")
    if not user or not password:
        sys.exit("Set YESSARE_ADMIN_USER and YESSARE_ADMIN_PASS env vars.")

    with open(args.json, encoding="utf-8") as fh:
        catalog = json.load(fh)

    exact_idx, fuzzy_idx = build_image_index(args.photos)

    api = Api(args.api)
    api.login(user, password)

    brand_id = api.brand_id(BRAND_NAME)
    if brand_id is None:
        sys.exit(f"Brand {BRAND_NAME!r} not found on {args.api}. Create it first.")
    print(f"brand {BRAND_NAME!r} -> id {brand_id}")

    existing = api.existing_product_names()
    print(f"{len(existing)} products already on site")

    # category ids (create-or-fetch, unless dry-run and it doesn't exist yet)
    cat_ids = {}
    for _n, _e, top in iter_unique_products(catalog):
        cat_ids.setdefault(top, None)
    for name in list(cat_ids):
        if args.dry_run:
            print(f"[dry-run] ensure category {name!r}")
            cat_ids[name] = None
        else:
            cat_ids[name] = api.ensure_category(name)
            print(f"category {name!r} -> id {cat_ids[name]}")

    stats = {"created": 0, "skipped_exists": 0, "skipped_no_photo": 0, "errors": 0}
    no_photo, errored = [], []

    for name, entry, top in iter_unique_products(catalog):
        img = find_image(name, exact_idx, fuzzy_idx)
        if img is None:
            stats["skipped_no_photo"] += 1
            no_photo.append(name)
            continue

        if name.lower() in existing:
            stats["skipped_exists"] += 1
            continue

        price = str(parse_price(entry.get("price", "")))
        payload = {
            "name": name,
            "brand": brand_id,
            "stock": 0,
            "warranty": "No Warranty",
            "price": {"mrp": price, "selling_price": price, "discount_rate": "0"},
        }
        if cat_ids.get(top):
            payload["category_ids"] = [cat_ids[top]]

        if args.dry_run:
            print(f"[dry-run] create {name!r}  Rs{price}  <- {os.path.basename(img)}")
            stats["created"] += 1
            continue

        try:
            pid = api.add_product(payload)
            api.upload_image(pid, img)
            existing.add(name.lower())
            stats["created"] += 1
            print(f"created [{pid}] {name}")
        except Exception as exc:  # noqa: BLE001
            stats["errors"] += 1
            errored.append((name, str(exc)))
            print(f"ERROR {name}: {exc}", file=sys.stderr)

    print("\n=== summary ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    if no_photo:
        print("\nno photo (skipped):")
        for n in no_photo:
            print(f"  - {n}")
    if errored:
        print("\nerrors:")
        for n, e in errored:
            print(f"  - {n}: {e}")
    if args.dry_run:
        print("\n(dry run - nothing was written)")


if __name__ == "__main__":
    main()
