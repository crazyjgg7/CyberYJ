#!/usr/bin/env python3
"""
检查高频字段 locator 完整性（M4）
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.authoritative_locator_quality import evaluate_authoritative_locator_quality


def main() -> int:
    report = evaluate_authoritative_locator_quality(
        str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
        str(ROOT / "data" / "mappings" / "source_evidence_targets.json"),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
