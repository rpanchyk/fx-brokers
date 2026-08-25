# -*- coding: utf-8 -*-
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml

REQUIRED_FIELDS = (
    "name",
    "homepage",
    "country",
    "regulations",
    "ukraine",
    "algo",
    "accounts",
    "swaps",
    "kyc",
    "platforms",
    "deposit",
    "withdrawal",
    "rts",
)
STATUSES = ("yes", "no", "partial")


def load_brokers(path: Path, broker_ids: list[str]) -> dict[str, dict]:
    """Load research records for the given broker ids.

    PyYAML turns bare ``yes``/``no`` into booleans; we convert status fields
    back to ``yes`` | ``no`` | ``partial``.
    """
    if not path.exists():
        raise FileNotFoundError(f"Broker dataset not found: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must be a mapping of broker id → fields")

    missing = [bid for bid in broker_ids if bid not in raw]
    if missing:
        raise ValueError("no research data in data/brokers.yaml for: " + ", ".join(missing))

    out: dict[str, dict] = {}
    for bid in broker_ids:
        rec_raw = raw[bid]
        if not isinstance(rec_raw, dict):
            raise ValueError(f"{bid}: broker record must be a mapping")
        rec = _normalize(deepcopy(rec_raw))
        rec["id"] = bid
        _validate(bid, rec)
        out[bid] = rec
    return out


def _normalize(rec: dict) -> dict:
    if not isinstance(rec, dict):
        raise ValueError("Broker record must be a mapping")
    for key in ("ukraine", "rts"):
        block = rec.get(key)
        if isinstance(block, dict) and "status" in block:
            block["status"] = status_str(block["status"])
    plat = rec.get("platforms")
    if isinstance(plat, dict):
        for k in ("mt4", "mt5", "ctrader"):
            if k in plat:
                plat[k] = status_str(plat[k])
    for pay in ("deposit", "withdrawal"):
        block = rec.get(pay)
        if isinstance(block, dict):
            for k in ("card", "bank_iban", "crypto"):
                if k in block:
                    block[k] = status_str(block[k])
    return rec


def status_str(value) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    text = str(value).strip().lower() if value is not None else ""
    if text in STATUSES:
        return text
    if text in ("так", "true", "1"):
        return "yes"
    if text in ("ні", "false", "0"):
        return "no"
    raise ValueError(f"status must be yes/no/partial, got {value!r}")


def _validate(bid: str, rec: dict) -> None:
    missing = [f for f in REQUIRED_FIELDS if f not in rec]
    if missing:
        raise ValueError(f"{bid}: missing fields: {', '.join(missing)}")
    for key in ("ukraine", "rts"):
        block = rec.get(key)
        if not isinstance(block, dict) or block.get("status") not in STATUSES:
            raise ValueError(f"{bid}: {key}.status must be yes/no/partial")
    plat = rec.get("platforms")
    if not isinstance(plat, dict):
        raise ValueError(f"{bid}: platforms must be a mapping")
    for k in ("mt4", "mt5", "ctrader"):
        if plat.get(k) not in STATUSES:
            raise ValueError(f"{bid}: platforms.{k} must be yes/no/partial")
    if not isinstance(rec.get("algo"), dict):
        raise ValueError(f"{bid}: algo must be a mapping")
    for pay in ("deposit", "withdrawal"):
        block = rec.get(pay)
        if not isinstance(block, dict):
            raise ValueError(f"{bid}: {pay} must be a mapping")
        for k in ("card", "bank_iban", "crypto"):
            if block.get(k) not in STATUSES:
                raise ValueError(f"{bid}: {pay}.{k} must be yes/no/partial")
