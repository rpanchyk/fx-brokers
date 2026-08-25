# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

KNOWN_POINTS = (
    "homepage",
    "country",
    "regulations",
    "accounts",
    "swaps",
    "kyc",
    "deposit",
    "withdrawal",
    "rts",
    "ukraine",
    "platforms",
    "algo",
)


@dataclass(frozen=True)
class Point:
    id: str
    label: str


@dataclass(frozen=True)
class AppConfig:
    title: str
    language: str
    filename_pattern: str
    orientation: str
    paper_size: str
    broker_ids: list[str]
    points: list[Point]

    def has(self, point_id: str) -> bool:
        return any(p.id == point_id for p in self.points)

    def label(self, point_id: str) -> str:
        for p in self.points:
            if p.id == point_id:
                return p.label
        return point_id


def _one_of(value: object, allowed: tuple[str, ...], field: str, default: str) -> str:
    raw = str(value or default).strip()
    for item in allowed:
        if raw.lower() == item.lower():
            return item
    raise ValueError(f"output.{field} must be one of {allowed}, got: {value!r}")


def _unique(ids: list[str], what: str) -> list[str]:
    seen: set[str] = set()
    dups: list[str] = []
    out: list[str] = []
    for item in ids:
        if item in seen:
            dups.append(item)
            continue
        seen.add(item)
        out.append(item)
    if dups:
        raise ValueError(f"Duplicate {what}: {', '.join(dups)}")
    return out


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"{path} is empty or not a mapping")

    output = raw.get("output") or {}
    if not isinstance(output, dict):
        raise ValueError("output must be a mapping")

    brokers_raw = raw.get("brokers") or []
    if not isinstance(brokers_raw, list):
        raise ValueError("brokers must be a YAML list of ids")
    broker_ids = _unique([str(b).strip() for b in brokers_raw if str(b).strip()], "brokers")
    raw_points = raw.get("points") or []
    if not isinstance(raw_points, list):
        raise ValueError("points must be a list")

    points: list[Point] = []
    for i, item in enumerate(raw_points, start=1):
        if not isinstance(item, dict) or not item.get("id"):
            raise ValueError(f"points[{i}] must have id")
        pid = str(item["id"]).strip()
        if pid not in KNOWN_POINTS:
            raise ValueError(f"Unknown point id {pid!r}. Known: {', '.join(KNOWN_POINTS)}")
        points.append(Point(id=pid, label=str(item.get("label") or pid)))
    _unique([p.id for p in points], "point ids")
    if not broker_ids:
        raise ValueError("brokers list is empty")
    if not points:
        raise ValueError("points list is empty")

    return AppConfig(
        title=str(output.get("title") or "Аналітика форекс-брокерів"),
        language=_one_of(output.get("language"), ("uk", "en"), "language", "uk"),
        filename_pattern=str(output.get("filename_pattern") or "FxBrokers_{YYYY}-{MM}.pdf"),
        orientation=_one_of(output.get("orientation"), ("portrait", "landscape"), "orientation", "portrait"),
        paper_size=_one_of(output.get("paper_size"), ("A4", "A3"), "paper_size", "A4"),
        broker_ids=broker_ids,
        points=points,
    )
