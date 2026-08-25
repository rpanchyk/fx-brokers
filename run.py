#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Зібрати PDF-аналітику форекс-брокерів за config.yml.

Дата зрізу — день запуску (або --as-of).

    python run.py
    python run.py --config config.yml
    python run.py --as-of 2026-08
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config_loader import load_config
from src.data_loader import load_brokers
from src.pdf.builder import build_pdf


def _period_ok(value: str) -> bool:
    parts = value.strip().split("-")
    return len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate FxBrokers_YYYY-MM.pdf")
    parser.add_argument("--config", default=str(ROOT / "config.yml"))
    parser.add_argument(
        "--as-of",
        default=None,
        help="Override run date / period, YYYY-MM or YYYY-MM-DD (default: today)",
    )
    args = parser.parse_args()

    try:
        cfg = load_config(Path(args.config))
        if args.as_of is not None and not _period_ok(args.as_of):
            raise ValueError("--as-of must be YYYY-MM or YYYY-MM-DD")
        brokers = load_brokers(ROOT / "data" / "brokers.yaml", cfg.broker_ids)
        out = build_pdf(cfg, brokers, ROOT, as_of_override=args.as_of)
    except (ValueError, FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
