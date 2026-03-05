#!/usr/bin/env python3
"""Refresh all relational data and regenerate app dataset."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"


def run_step(script_name: str, *args: str) -> None:
    command = [sys.executable, str(SCRIPTS_DIR / script_name), *args]
    print(f"[run] {' '.join(command)}")
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verified-only", action="store_true", help="Build app dataset with verified fitments only")
    parser.add_argument("--pull-sources", action="store_true", help="Pull latest brand catalog snapshots before rebuild")
    args = parser.parse_args()

    if args.pull_sources:
      run_step("pull_sources.py")

    run_step("generate_bikes.py")
    run_step("seed_exhaust_products.py")
    run_step("generate_fitments.py")

    build_args = ["--verified-only"] if args.verified_only else []
    run_step("build_dataset.py", *build_args)

    print("Refresh complete.")


if __name__ == "__main__":
    main()
