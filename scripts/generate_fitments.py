#!/usr/bin/env python3
"""Generate fitment relations between bikes and exhaust products.

- Candidate rows are rule-based and marked as candidate.
- Optional verified rows can be supplied in data/raw/verified_fitments.csv.
"""

from __future__ import annotations

import csv
import hashlib
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[1]
BIKES_PATH = ROOT / "data" / "raw" / "bikes.csv"
PRODUCTS_PATH = ROOT / "data" / "raw" / "exhaust_products.csv"
VERIFIED_PATH = ROOT / "data" / "raw" / "verified_fitments.csv"
OUT_PATH = ROOT / "data" / "raw" / "fitments.csv"
TODAY = date.today().isoformat()

MAX_PER_CATEGORY = {
    "Sport/Supersport": 10,
    "Adventure/Dual-sport": 9,
    "Dirt/Off-road": 8,
    "Cruiser/Harley-style": 10,
}

# Affinity scores. Higher means more likely to be selected for candidate fitments.
MAKE_AFFINITY = {
    "Honda": {"Yoshimura": 3, "Akrapovic": 2, "M4": 2, "Arrow": 2, "Leovince": 2},
    "Yamaha": {"Graves": 4, "Akrapovic": 2, "Yoshimura": 2, "M4": 2, "Brocks": 2},
    "Kawasaki": {"Brocks": 4, "Akrapovic": 2, "Arrow": 2, "M4": 2, "Two Brothers": 2},
    "Suzuki": {"Yoshimura": 4, "M4": 3, "Brocks": 2, "Two Brothers": 2},
    "KTM": {"Akrapovic": 4, "FMF": 3, "Remus": 2, "Arrow": 2, "SC Project": 2},
    "BMW": {"Akrapovic": 3, "Remus": 3, "Arrow": 2, "Leovince": 2},
    "Ducati": {"Termignoni": 4, "Akrapovic": 3, "SC Project": 3, "Arrow": 2},
    "Triumph": {"Arrow": 3, "SC Project": 2, "Akrapovic": 2, "Remus": 2},
    "Harley-Davidson": {"Vance & Hines": 5, "Two Brothers": 2, "Remus": 2, "Akrapovic": 1},
    "Indian": {"Vance & Hines": 3, "Remus": 2, "Two Brothers": 2, "Akrapovic": 1},
    "Husqvarna": {"FMF": 3, "Akrapovic": 3, "SC Project": 2, "Remus": 1},
    "GasGas": {"FMF": 4, "Akrapovic": 2, "SC Project": 2},
    "Aprilia": {"SC Project": 4, "Akrapovic": 3, "Arrow": 3, "Leovince": 2},
    "Moto Guzzi": {"Arrow": 3, "Remus": 3, "Leovince": 2, "SC Project": 1},
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def read_csv(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def stable_tiebreak(*parts: str) -> int:
    digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def product_categories(product: dict[str, str]) -> set[str]:
    return {item.strip() for item in product["target_categories"].split("|") if item.strip()}


def score_product_for_bike(bike: dict[str, str], product: dict[str, str]) -> int:
    score = 10
    make = bike["make"]
    brand = product["brand"]
    score += MAKE_AFFINITY.get(make, {}).get(brand, 0)

    if bike["bike_category"] == "Dirt/Off-road" and brand in {"FMF", "Akrapovic", "Yoshimura"}:
        score += 2
    if bike["bike_category"] == "Cruiser/Harley-style" and brand in {"Vance & Hines", "Remus", "Two Brothers"}:
        score += 2
    if bike["bike_category"] == "Adventure/Dual-sport" and brand in {"Akrapovic", "Arrow", "Remus"}:
        score += 2

    return score


def verified_rows() -> list[dict[str, str]]:
    if not VERIFIED_PATH.exists():
        VERIFIED_PATH.write_text(
            "fitment_id,bike_id,product_id,fitment_year_start,fitment_year_end,verification_status,source_url,source_checked_on,fitment_notes\n",
            encoding="utf-8",
        )
        return []
    return read_csv(VERIFIED_PATH)


def main() -> None:
    bikes = read_csv(BIKES_PATH)
    products = read_csv(PRODUCTS_PATH)
    verified = verified_rows()

    fitments: list[dict[str, str]] = []
    seen_pairs: set[tuple[str, str, str, str]] = set()

    for bike in bikes:
        bike_cat = bike["bike_category"]
        matches = [p for p in products if bike_cat in product_categories(p)]
        scored = sorted(
            matches,
            key=lambda p: (
                -score_product_for_bike(bike, p),
                stable_tiebreak(bike["bike_id"], p["product_id"]),
                p["product_id"],
            ),
        )
        limit = MAX_PER_CATEGORY.get(bike_cat, 8)
        selected = scored[:limit]

        for product in selected:
            key = (bike["bike_id"], product["product_id"], bike["year_start"], bike["year_end"])
            if key in seen_pairs:
                continue
            seen_pairs.add(key)

            fitment_id = slugify(f"{bike['bike_id']}-{product['product_id']}-{bike['year_start']}-{bike['year_end']}")
            fitments.append(
                {
                    "fitment_id": fitment_id,
                    "bike_id": bike["bike_id"],
                    "product_id": product["product_id"],
                    "fitment_year_start": bike["year_start"],
                    "fitment_year_end": bike["year_end"],
                    "verification_status": "candidate",
                    "source_url": "",
                    "source_checked_on": "",
                    "fitment_notes": "Rule-based candidate fitment. Verify exact part number before purchase.",
                }
            )

    # Guarantee every product appears at least once in the relation set.
    used_products = {item["product_id"] for item in fitments}
    for product in products:
        if product["product_id"] in used_products:
            continue

        compatible_bikes = [bike for bike in bikes if bike["bike_category"] in product_categories(product)]
        if not compatible_bikes:
            continue
        bike = sorted(compatible_bikes, key=lambda b: (b["make"], b["model"], int(b["year_start"])))[0]
        key = (bike["bike_id"], product["product_id"], bike["year_start"], bike["year_end"])
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        fitment_id = slugify(f"{bike['bike_id']}-{product['product_id']}-{bike['year_start']}-{bike['year_end']}")
        fitments.append(
            {
                "fitment_id": fitment_id,
                "bike_id": bike["bike_id"],
                "product_id": product["product_id"],
                "fitment_year_start": bike["year_start"],
                "fitment_year_end": bike["year_end"],
                "verification_status": "candidate",
                "source_url": "",
                "source_checked_on": "",
                "fitment_notes": "Rule-based candidate fitment. Verify exact part number before purchase.",
            }
        )

    # Merge verified rows on top; if duplicate bike/product/year exists, verified wins.
    for row in verified:
        key = (row["bike_id"], row["product_id"], row["fitment_year_start"], row["fitment_year_end"])
        fitments = [f for f in fitments if (f["bike_id"], f["product_id"], f["fitment_year_start"], f["fitment_year_end"]) != key]
        if not row.get("fitment_id"):
            row["fitment_id"] = slugify(
                f"{row['bike_id']}-{row['product_id']}-{row['fitment_year_start']}-{row['fitment_year_end']}"
            )
        if not row.get("source_checked_on"):
            row["source_checked_on"] = TODAY
        fitments.append(row)

    fitments.sort(
        key=lambda r: (
            r["verification_status"],
            r["bike_id"],
            r["product_id"],
            int(r["fitment_year_start"]),
            int(r["fitment_year_end"]),
        )
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "fitment_id",
                "bike_id",
                "product_id",
                "fitment_year_start",
                "fitment_year_end",
                "verification_status",
                "source_url",
                "source_checked_on",
                "fitment_notes",
            ],
        )
        writer.writeheader()
        writer.writerows(fitments)

    candidate_count = sum(1 for item in fitments if item["verification_status"] == "candidate")
    verified_count = sum(1 for item in fitments if item["verification_status"] == "verified")
    print(f"Wrote {len(fitments)} fitments ({candidate_count} candidate, {verified_count} verified) to {OUT_PATH}")


if __name__ == "__main__":
    main()
