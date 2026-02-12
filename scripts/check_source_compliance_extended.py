#!/usr/bin/env python3
"""
来源索引扩展合规检查（覆盖全部 source_id）
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.source_compliance import evaluate_source_compliance


def main() -> int:
    report = evaluate_source_compliance(
        str(ROOT / "data" / "core" / "sources.json"),
        str(ROOT / "data" / "core" / "source_compliance_policy_extended.json"),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
