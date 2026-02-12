#!/usr/bin/env python3
"""
生成本地权威知识库产物（index + entries）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.authoritative_local_kb import write_authoritative_local_kb


def main() -> int:
    result = write_authoritative_local_kb(
        mapping_path=str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
        sources_path=str(ROOT / "data" / "core" / "sources.json"),
        output_dir=str(ROOT / "data" / "authoritative"),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
