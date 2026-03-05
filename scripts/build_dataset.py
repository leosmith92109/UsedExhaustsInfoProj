#!/usr/bin/env python3
"""Build app-ready exhaust dataset JSON from relational CSV files."""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
from collections import Counter, defaultdict
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BIKES_PATH = ROOT / "data" / "raw" / "bikes.csv"
PRODUCTS_PATH = ROOT / "data" / "raw" / "exhaust_products.csv"
FITMENTS_PATH = ROOT / "data" / "raw" / "fitments.csv"
OUT_PATH = ROOT / "data" / "generated" / "exhaust_dataset.json"
STATS_PATH = ROOT / "data" / "generated" / "dataset_stats.json"


def read_csv(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_float(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_int(value: str) -> int | None:
    value = value.strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def price_range(price_usd: int | None) -> str:
    if price_usd is None:
        return "$$$"
    if price_usd < 300:
        return "$"
    if price_usd <= 600:
        return "$$"
    if price_usd <= 1000:
        return "$$$"
    return "$$$$"


def material_title(material: str) -> str:
    if material == "stainless":
        return "stainless steel"
    return material


def build_description(category: str, bike_model: str, product_name: str, brand: str, verification: str) -> str:
    tone = {
        "Sport/Supersport": "high-rpm race tone",
        "Adventure/Dual-sport": "deep touring character",
        "Dirt/Off-road": "crisp off-road response",
        "Cruiser/Harley-style": "deep V-twin pulse",
    }.get(category, "performance-focused note")

    verification_note = (
        "This fitment is source-verified for the listed years."
        if verification == "verified"
        else "This fitment is a candidate match and should be confirmed against part-number fitment tables before purchase."
    )

    return (
        f"{brand} {product_name} is linked for {bike_model} with a {tone}. "
        f"Use this entry as a starting point for pricing, used-market checks, and sound research. {verification_note}"
    )


def build_pros(material: str, verification: str, weight: float | None) -> list[str]:
    output = [f"{material_title(material).capitalize()} construction"]
    if weight is None:
        output.append("Weight savings not published")
    else:
        output.append(f"Approx. {weight:.1f} lb weight savings")
    output.append("Verified fitment reference" if verification == "verified" else "Broad catalog candidate coverage")
    return output[:3]


def build_cons(verification: str, db_rating: int | None, source_url: str) -> list[str]:
    output: list[str] = []
    if verification != "verified":
        output.append("Fitment needs exact part-number confirmation")
    if db_rating is None:
        output.append("Manufacturer dB value not published")
    if not source_url:
        output.append("Direct fitment source link not captured")
    while len(output) < 3:
        output.append("Availability varies by region")
    return output[:3]


def make_competitor_rows(entries_for_bike: list[dict[str, Any]], current: dict[str, Any]) -> list[dict[str, str]]:
    competitors = [item for item in entries_for_bike if item["brand"] != current["brand"]]
    competitors.sort(key=lambda item: (item["priceUSD"] if item["priceUSD"] is not None else 10**9, item["brand"], item["productName"]))
    selected = competitors[:2]

    rows: list[dict[str, str]] = []
    for comp in selected:
        rows.append(
            {
                "brand": comp["brand"],
                "product": comp["productName"],
                "summary": (
                    f"{comp['brand']} {comp['productName']} is another option for this bike generation; "
                    f"compare listed fitment years and part references before purchasing."
                ),
            }
        )
    return rows


def build_dataset(include_candidates: bool) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bikes = {row["bike_id"]: row for row in read_csv(BIKES_PATH)}
    products = {row["product_id"]: row for row in read_csv(PRODUCTS_PATH)}
    fitments = read_csv(FITMENTS_PATH)

    dataset: list[dict[str, Any]] = []
    by_bike: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)

    for fit in fitments:
        verification = fit.get("verification_status", "candidate")
        if not include_candidates and verification != "verified":
            continue

        bike = bikes.get(fit["bike_id"])
        product = products.get(fit["product_id"])
        if not bike or not product:
            continue

        fit_start = int(fit["fitment_year_start"])
        fit_end = int(fit["fitment_year_end"])
        bike_years = f"{fit_start}-{fit_end}" if fit_start != fit_end else str(fit_start)

        weight = parse_float(product.get("weight_savings_lbs", ""))
        db_rating = parse_int(product.get("db_rating", ""))
        db_note = product.get("db_rating_note", "").strip() or "Manufacturer not specified."
        price = parse_int(product.get("price_usd", ""))

        entry_id = slugify(f"{fit['fitment_id']}-{bike['make']}-{bike['model']}")
        tags = sorted(
            {
                bike["make"].lower(),
                bike["model"].lower(),
                bike["bike_category"].split("/")[0].lower(),
                product["brand"].lower().replace("&", "and"),
                product["type"],
                product["material"],
                verification,
            }
        )

        entry: dict[str, Any] = {
            "id": entry_id,
            "brand": product["brand"],
            "productName": product["product_name"],
            "type": product["type"],
            "bikeCategory": bike["bike_category"],
            "bikeMake": bike["make"],
            "bikeModel": bike["model"],
            "bikeYears": bike_years,
            "material": product["material"],
            "weightSavingsLbs": weight,
            "dbRating": db_rating,
            "dbRatingNote": db_note,
            "priceUSD": price if price is not None else 0,
            "priceRange": price_range(price),
            "description": build_description(bike["bike_category"], bike["model"], product["product_name"], product["brand"], verification),
            "pros": build_pros(product["material"], verification, weight),
            "cons": build_cons(verification, db_rating, fit.get("source_url", "")),
            "competitorComparisons": [],
            "brandListingUrl": product["brand_listing_url"],
            "youtubeSearchQuery": f"{product['brand']} {product['product_name']} {bike['model']} exhaust sound",
            "tags": tags,
            "verificationStatus": verification,
            "fitmentSourceUrl": fit.get("source_url", ""),
            "fitmentNotes": fit.get("fitment_notes", ""),
            "generation": bike.get("generation", ""),
        }

        dataset.append(entry)
        by_bike[bike["bike_id"]].append(entry)

    for bike_entries in by_bike.values():
        for entry in bike_entries:
            entry["competitorComparisons"] = make_competitor_rows(bike_entries, entry)

    dataset.sort(key=lambda item: (item["bikeMake"], item["bikeModel"], item["brand"], item["productName"], item["bikeYears"]))

    status_counts = Counter(item["verificationStatus"] for item in dataset)
    category_counts = Counter(item["bikeCategory"] for item in dataset)
    brand_counts = Counter(item["brand"] for item in dataset)

    stats = {
        "rows": len(dataset),
        "status_counts": dict(status_counts),
        "category_counts": dict(category_counts),
        "brand_counts": dict(brand_counts),
    }

    return dataset, stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verified-only", action="store_true", help="Exclude candidate fitments from generated dataset")
    args = parser.parse_args()

    dataset, stats = build_dataset(include_candidates=not args.verified_only)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    STATS_PATH.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    print(f"Wrote {len(dataset)} rows to {OUT_PATH}")
    print(f"Stats written to {STATS_PATH}")


if __name__ == "__main__":
    main()
