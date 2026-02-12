#!/usr/bin/env python3
"""
检查 authoritative_text_map 的 convention 剩余缺口。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.authoritative_convention_gap import (
    evaluate_authoritative_convention_gap,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--threshold",
        type=int,
        default=18,
        help="允许的 convention_only 最大条数（默认 18）",
    )
    args = parser.parse_args()

    report = evaluate_authoritative_convention_gap(
        mapping_path=str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
        convention_only_threshold=args.threshold,
        allowlist_path=str(ROOT / "data" / "core" / "convention_allowlist.json"),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
