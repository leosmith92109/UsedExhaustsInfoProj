#!/usr/bin/env python3
"""Simple CLI query tool for generated dataset."""

from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "generated" / "exhaust_dataset.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--make", default="", help="Filter by bike make")
    parser.add_argument("--model", default="", help="Filter by bike model substring")
    parser.add_argument("--brand", default="", help="Filter by exhaust brand")
    parser.add_argument("--status", default="", help="Filter by verification status")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    rows = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    out = []
    for row in rows:
        if args.make and row["bikeMake"].lower() != args.make.lower():
            continue
        if args.model and args.model.lower() not in row["bikeModel"].lower():
            continue
        if args.brand and row["brand"].lower() != args.brand.lower():
            continue
        if args.status and row.get("verificationStatus", "").lower() != args.status.lower():
            continue
        out.append(row)

    print(f"Matches: {len(out)}")
    for row in out[: args.limit]:
        print(
            f"- {row['bikeYears']} {row['bikeMake']} {row['bikeModel']} | "
            f"{row['brand']} {row['productName']} | {row.get('verificationStatus','')}"
        )


if __name__ == "__main__":
    main()
