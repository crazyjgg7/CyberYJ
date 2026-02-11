#!/usr/bin/env python3
"""
检查权威映射覆盖率（M4）
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.authoritative_coverage import evaluate_authoritative_coverage


def main() -> int:
    report = evaluate_authoritative_coverage(
        str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
        str(ROOT / "data" / "mappings" / "authoritative_coverage_targets.json"),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
