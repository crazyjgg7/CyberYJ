#!/usr/bin/env python3
"""
检查高频输出字段的来源证据映射
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.source_evidence_check import evaluate_source_evidence


def main() -> int:
    report = evaluate_source_evidence(
        str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
        str(ROOT / "data" / "mappings" / "source_evidence_targets.json"),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
