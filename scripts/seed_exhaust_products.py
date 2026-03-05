#!/usr/bin/env python3
"""Seed exhaust product catalog CSV."""

from __future__ import annotations

import csv
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "raw" / "exhaust_products.csv"
TODAY = date.today().isoformat()

BRAND_URLS = {
    "Akrapovic": "https://www.akrapovic.com/en/moto/products",
    "Yoshimura": "https://www.yoshimura-rd.com/collections/all",
    "Two Brothers": "https://www.twobros.com/collections/exhaust-systems",
    "FMF": "https://www.fmfracing.com/collections/exhaust",
    "Arrow": "https://www.arrow.it/en/assembled/1/motorcycle",
    "Leovince": "https://www.leovince.com/en-us/products/motorcycle",
    "SC Project": "https://shop.sc-project.com/en-US/motorcycle",
    "Remus": "https://remus.eu/product-category/motorcycle/",
    "Termignoni": "https://www.termignoni.it/en/catalog/",
    "M4": "https://m4exhaust.com/",
    "Graves": "https://www.gravesport.com/",
    "Vance & Hines": "https://www.vanceandhines.com/product-category/exhausts/",
    "Brocks": "https://brocksperformance.com/exhausts/",
    "Delkevic": "https://delkevic.com/motorcycle-exhaust-systems/",
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def row(brand: str, name: str, ex_type: str, material: str, price: int, categories: str, source: str = "") -> dict[str, str]:
    product_id = slugify(f"{brand}-{name}")
    return {
        "product_id": product_id,
        "brand": brand,
        "product_name": name,
        "type": ex_type,
        "material": material,
        "price_usd": str(price),
        "weight_savings_lbs": "",
        "db_rating": "",
        "db_rating_note": "Manufacturer not specified.",
        "target_categories": categories,
        "brand_listing_url": BRAND_URLS[brand],
        "source_url": source or BRAND_URLS[brand],
        "source_checked_on": TODAY,
    }


def main() -> None:
    products: list[dict[str, str]] = []

    products.extend(
        [
            row("Akrapovic", "Racing Line", "full-system", "titanium", 1899, "Sport/Supersport|Adventure/Dual-sport"),
            row("Akrapovic", "Slip-On Line", "slip-on", "titanium", 999, "Sport/Supersport|Adventure/Dual-sport|Cruiser/Harley-style"),
            row("Akrapovic", "Evolution Line", "full-system", "titanium", 2099, "Sport/Supersport|Dirt/Off-road"),
            row("Akrapovic", "Track Day Link Pipe", "mid-pipe", "stainless", 399, "Sport/Supersport"),
            row("Akrapovic", "Adventure Hexagonal", "slip-on", "titanium", 1099, "Adventure/Dual-sport"),
            row("Akrapovic", "Road-Legal Line", "slip-on", "carbon", 1149, "Sport/Supersport"),
            row("Akrapovic", "Offroad SX Header", "mid-pipe", "stainless", 349, "Dirt/Off-road"),
            row("Akrapovic", "Touring 2-1", "full-system", "titanium", 1999, "Cruiser/Harley-style"),
        ]
    )

    products.extend(
        [
            row("Yoshimura", "AT2", "slip-on", "stainless", 749, "Sport/Supersport|Adventure/Dual-sport|Cruiser/Harley-style"),
            row("Yoshimura", "Alpha T", "slip-on", "carbon", 799, "Sport/Supersport"),
            row("Yoshimura", "Alpha Works", "full-system", "stainless", 1299, "Sport/Supersport"),
            row("Yoshimura", "RS-12", "full-system", "stainless", 999, "Dirt/Off-road"),
            row("Yoshimura", "RS-4", "slip-on", "aluminum", 529, "Dirt/Off-road"),
            row("Yoshimura", "R-77", "slip-on", "stainless", 669, "Cruiser/Harley-style"),
            row("Yoshimura", "Street Alpha", "slip-on", "stainless", 579, "Sport/Supersport|Cruiser/Harley-style"),
            row("Yoshimura", "Adventure Alpha", "slip-on", "stainless", 699, "Adventure/Dual-sport"),
        ]
    )

    products.extend(
        [
            row("Two Brothers", "S1R", "slip-on", "carbon", 649, "Sport/Supersport"),
            row("Two Brothers", "Comp-S", "slip-on", "stainless", 699, "Adventure/Dual-sport|Cruiser/Harley-style"),
            row("Two Brothers", "M2", "slip-on", "aluminum", 499, "Dirt/Off-road"),
            row("Two Brothers", "2-1 Comp", "full-system", "stainless", 1199, "Cruiser/Harley-style"),
            row("Two Brothers", "Tarmac", "slip-on", "stainless", 649, "Sport/Supersport"),
            row("Two Brothers", "Adventure S1", "slip-on", "stainless", 719, "Adventure/Dual-sport"),
            row("Two Brothers", "Racing Header", "mid-pipe", "stainless", 349, "Sport/Supersport"),
            row("Two Brothers", "Storm Series", "slip-on", "carbon", 779, "Sport/Supersport|Cruiser/Harley-style"),
        ]
    )

    products.extend(
        [
            row("FMF", "Factory 4.1 RCT", "full-system", "titanium", 1099, "Dirt/Off-road"),
            row("FMF", "PowerCore 4", "slip-on", "aluminum", 469, "Dirt/Off-road|Adventure/Dual-sport"),
            row("FMF", "Q4", "slip-on", "stainless", 429, "Dirt/Off-road|Adventure/Dual-sport"),
            row("FMF", "MegaBomb Header", "mid-pipe", "stainless", 329, "Dirt/Off-road|Adventure/Dual-sport"),
            row("FMF", "Apex Street", "slip-on", "aluminum", 529, "Cruiser/Harley-style"),
            row("FMF", "4.1 Slip-On", "slip-on", "titanium", 689, "Dirt/Off-road"),
            row("FMF", "Gnarly Pipe", "full-system", "stainless", 559, "Dirt/Off-road"),
            row("FMF", "Adventure Q4 Hex", "slip-on", "aluminum", 579, "Adventure/Dual-sport"),
        ]
    )

    products.extend(
        [
            row("Arrow", "Pro-Race", "slip-on", "titanium", 699, "Sport/Supersport"),
            row("Arrow", "Race-Tech", "slip-on", "titanium", 789, "Sport/Supersport|Adventure/Dual-sport"),
            row("Arrow", "Competition Full System", "full-system", "stainless", 1299, "Sport/Supersport"),
            row("Arrow", "Offroad Thunder", "full-system", "titanium", 1199, "Dirt/Off-road"),
            row("Arrow", "Thunder 2-1", "full-system", "stainless", 1299, "Cruiser/Harley-style"),
            row("Arrow", "Indy Race Evo", "slip-on", "stainless", 679, "Cruiser/Harley-style"),
            row("Arrow", "Adventure Full Kit", "full-system", "stainless", 1399, "Adventure/Dual-sport"),
            row("Arrow", "X-Kone", "slip-on", "titanium", 739, "Sport/Supersport|Adventure/Dual-sport"),
        ]
    )

    products.extend(
        [
            row("Leovince", "LV-10", "slip-on", "stainless", 449, "Sport/Supersport"),
            row("Leovince", "Factory S", "slip-on", "carbon", 679, "Sport/Supersport"),
            row("Leovince", "LV One EVO", "slip-on", "stainless", 529, "Adventure/Dual-sport"),
            row("Leovince", "X3", "slip-on", "titanium", 669, "Adventure/Dual-sport|Dirt/Off-road"),
            row("Leovince", "Classic Racer", "slip-on", "stainless", 589, "Cruiser/Harley-style"),
            row("Leovince", "LV Pro", "slip-on", "stainless", 639, "Cruiser/Harley-style"),
            row("Leovince", "GP Corsa", "slip-on", "stainless", 499, "Sport/Supersport"),
            row("Leovince", "SBK Full", "full-system", "stainless", 1099, "Sport/Supersport"),
        ]
    )

    products.extend(
        [
            row("SC Project", "SC1-R", "slip-on", "titanium", 899, "Sport/Supersport"),
            row("SC Project", "CR-T", "slip-on", "titanium", 949, "Sport/Supersport|Cruiser/Harley-style"),
            row("SC Project", "Adventure-R", "slip-on", "titanium", 969, "Adventure/Dual-sport"),
            row("SC Project", "S1", "slip-on", "carbon", 899, "Adventure/Dual-sport|Cruiser/Harley-style"),
            row("SC Project", "MX Racing", "full-system", "titanium", 1299, "Dirt/Off-road"),
            row("SC Project", "Conic 70s", "slip-on", "stainless", 799, "Cruiser/Harley-style"),
            row("SC Project", "SC1-M", "slip-on", "titanium", 839, "Sport/Supersport"),
            row("SC Project", "CRT Mid-Pipe Kit", "mid-pipe", "stainless", 449, "Sport/Supersport"),
        ]
    )

    products.extend(
        [
            row("Remus", "Hypercone", "slip-on", "titanium", 839, "Sport/Supersport"),
            row("Remus", "NXT Full", "full-system", "stainless", 1399, "Sport/Supersport"),
            row("Remus", "ROXX", "slip-on", "titanium", 849, "Adventure/Dual-sport|Cruiser/Harley-style"),
            row("Remus", "8 Full System", "full-system", "stainless", 1499, "Adventure/Dual-sport"),
            row("Remus", "Slash Cut", "slip-on", "stainless", 899, "Cruiser/Harley-style"),
            row("Remus", "2-1 Touring", "full-system", "stainless", 1499, "Cruiser/Harley-style"),
            row("Remus", "MX Hypercone", "slip-on", "stainless", 549, "Dirt/Off-road"),
            row("Remus", "PowerCone", "slip-on", "stainless", 799, "Sport/Supersport"),
        ]
    )

    products.extend(
        [
            row("Termignoni", "Racing Titanium", "full-system", "titanium", 2299, "Sport/Supersport"),
            row("Termignoni", "Ducati Slip-On", "slip-on", "carbon", 1399, "Sport/Supersport"),
            row("Termignoni", "Adventure Silencer", "slip-on", "titanium", 1099, "Adventure/Dual-sport"),
            row("Termignoni", "Relevance", "slip-on", "stainless", 799, "Sport/Supersport"),
            row("Termignoni", "Retro Cone", "slip-on", "stainless", 899, "Cruiser/Harley-style"),
            row("Termignoni", "MX Factory", "full-system", "titanium", 1499, "Dirt/Off-road"),
        ]
    )

    products.extend(
        [
            row("M4", "GP19", "slip-on", "stainless", 549, "Sport/Supersport"),
            row("M4", "Street Slayer", "slip-on", "stainless", 579, "Sport/Supersport"),
            row("M4", "Race Full System", "full-system", "stainless", 1099, "Sport/Supersport"),
            row("M4", "Adventure Canister", "slip-on", "stainless", 699, "Adventure/Dual-sport"),
            row("M4", "MX Full", "full-system", "stainless", 999, "Dirt/Off-road"),
            row("M4", "Cruiser Twin", "slip-on", "stainless", 739, "Cruiser/Harley-style"),
        ]
    )

    products.extend(
        [
            row("Graves", "Full Titanium System", "full-system", "titanium", 1799, "Sport/Supersport"),
            row("Graves", "Slip-On Cat-Back", "slip-on", "titanium", 1099, "Sport/Supersport"),
            row("Graves", "Works 2", "full-system", "titanium", 1999, "Sport/Supersport"),
            row("Graves", "Dual Carbon", "slip-on", "carbon", 1299, "Sport/Supersport"),
            row("Graves", "Adventure SX", "slip-on", "stainless", 899, "Adventure/Dual-sport"),
            row("Graves", "Motocross Ti", "full-system", "titanium", 1399, "Dirt/Off-road"),
        ]
    )

    products.extend(
        [
            row("Vance & Hines", "Twin Slash", "slip-on", "stainless", 799, "Cruiser/Harley-style"),
            row("Vance & Hines", "Shortshots", "slip-on", "stainless", 749, "Cruiser/Harley-style"),
            row("Vance & Hines", "Hi-Output 2-1", "full-system", "stainless", 1299, "Cruiser/Harley-style"),
            row("Vance & Hines", "Upsweep", "slip-on", "stainless", 699, "Cruiser/Harley-style"),
            row("Vance & Hines", "Adventure 500", "slip-on", "stainless", 899, "Adventure/Dual-sport"),
            row("Vance & Hines", "CS One", "slip-on", "stainless", 599, "Sport/Supersport"),
        ]
    )

    products.extend(
        [
            row("Brocks", "Alien Head 2", "full-system", "stainless", 1599, "Sport/Supersport"),
            row("Brocks", "Penta Carbon", "slip-on", "carbon", 1099, "Sport/Supersport"),
            row("Brocks", "Street Meg", "slip-on", "stainless", 799, "Sport/Supersport"),
            row("Brocks", "Sidewinder", "full-system", "stainless", 1699, "Sport/Supersport"),
            row("Brocks", "ADV Meg", "slip-on", "stainless", 899, "Adventure/Dual-sport"),
            row("Brocks", "V-Twin Short", "slip-on", "stainless", 889, "Cruiser/Harley-style"),
        ]
    )

    products.extend(
        [
            row("Delkevic", "Mini 8", "slip-on", "stainless", 319, "Sport/Supersport|Cruiser/Harley-style"),
            row("Delkevic", "Oval Stainless", "slip-on", "stainless", 349, "Sport/Supersport|Adventure/Dual-sport"),
            row("Delkevic", "Carbon 13", "slip-on", "carbon", 399, "Sport/Supersport"),
            row("Delkevic", "Adventure 14", "slip-on", "stainless", 379, "Adventure/Dual-sport"),
            row("Delkevic", "MX Core", "slip-on", "stainless", 329, "Dirt/Off-road"),
            row("Delkevic", "2-1 Cruiser", "full-system", "stainless", 699, "Cruiser/Harley-style"),
        ]
    )

    products.sort(key=lambda r: (r["brand"], r["product_name"]))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "product_id",
                "brand",
                "product_name",
                "type",
                "material",
                "price_usd",
                "weight_savings_lbs",
                "db_rating",
                "db_rating_note",
                "target_categories",
                "brand_listing_url",
                "source_url",
                "source_checked_on",
            ],
        )
        writer.writeheader()
        writer.writerows(products)

    print(f"Wrote {len(products)} products to {OUT_PATH}")


if __name__ == "__main__":
    main()
