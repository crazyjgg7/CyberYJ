#!/usr/bin/env python3
"""
生成字段展开版本地权威知识库（effective）。
"""

from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.authoritative_local_kb_effective import (
    write_effective_authoritative_local_kb,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allowlist-path",
        default=str(ROOT / "data" / "core" / "convention_allowlist.json"),
        help="convention 白名单文件路径",
    )
    args = parser.parse_args()
    result = write_effective_authoritative_local_kb(
        data_root=str(ROOT / "data"),
        mapping_path=str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
        sources_path=str(ROOT / "data" / "core" / "sources.json"),
        allowlist_path=args.allowlist_path,
        output_dir=str(ROOT / "data" / "authoritative"),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
