#!/usr/bin/env python3
"""
检查 data 目录 source_ref 一致性
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.source_ref_integrity import evaluate_source_ref_integrity


def main() -> int:
    report = evaluate_source_ref_integrity(
        str(ROOT / "data"),
        str(ROOT / "data" / "core" / "sources.json"),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
