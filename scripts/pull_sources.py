#!/usr/bin/env python3
"""Pull brand catalog source snapshots for manual fitment verification."""

from __future__ import annotations

import csv
import pathlib
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw" / "source_snapshots"
META_PATH = OUT_DIR / "snapshot_index.csv"

SOURCES = [
    ("Akrapovic", "https://www.akrapovic.com/en/moto/products"),
    ("Yoshimura", "https://www.yoshimura-rd.com/collections/all"),
    ("Two Brothers", "https://www.twobros.com/collections/exhaust-systems"),
    ("FMF", "https://www.fmfracing.com/collections/exhaust"),
    ("Arrow", "https://www.arrow.it/en/assembled/1/motorcycle"),
    ("Leovince", "https://www.leovince.com/en-us/products/motorcycle"),
    ("SC Project", "https://shop.sc-project.com/en-US/motorcycle"),
    ("Remus", "https://remus.eu/product-category/motorcycle/"),
    ("Termignoni", "https://www.termignoni.it/en/catalog/"),
    ("M4", "https://m4exhaust.com/"),
    ("Graves", "https://www.gravesport.com/"),
    ("Vance and Hines", "https://www.vanceandhines.com/product-category/exhausts/"),
    ("Brocks", "https://brocksperformance.com/exhausts/"),
    ("Delkevic", "https://delkevic.com/motorcycle-exhaust-systems/"),
]


def slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for brand, url in SOURCES:
        out_file = OUT_DIR / f"{now}_{slugify(brand)}.html"
        status = "ok"
        error_text = ""
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "MotoExhaustDataRefresh/1.0 (+local-personal-use)",
                },
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                out_file.write_bytes(response.read())
        except Exception as exc:  # noqa: BLE001
            status = "error"
            error_text = str(exc)
            out_file.write_text(f"ERROR: {exc}\n", encoding="utf-8")

        rows.append(
            {
                "timestamp_utc": now,
                "brand": brand,
                "url": url,
                "status": status,
                "snapshot_file": str(out_file.relative_to(ROOT)).replace("\\", "/"),
                "error": error_text,
            }
        )

    with META_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["timestamp_utc", "brand", "url", "status", "snapshot_file", "error"],
        )
        writer.writeheader()
        writer.writerows(rows)

    ok = sum(1 for r in rows if r["status"] == "ok")
    print(f"Saved {ok}/{len(rows)} source snapshots to {OUT_DIR}")
    print(f"Index written to {META_PATH}")


if __name__ == "__main__":
    main()
