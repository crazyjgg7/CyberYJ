#!/usr/bin/env python3
"""
校验字段展开版本地权威知识库（effective）。
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

from cyberYJ.utils.authoritative_local_kb_effective import (
    evaluate_effective_authoritative_local_kb,
    write_effective_authoritative_local_kb,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="先重新生成 effective 产物")
    parser.add_argument(
        "--allowlist-path",
        default=str(ROOT / "data" / "core" / "convention_allowlist.json"),
        help="convention 白名单文件路径",
    )
    args = parser.parse_args()
    allowlist_path = args.allowlist_path

    if args.refresh:
        write_effective_authoritative_local_kb(
            data_root=str(ROOT / "data"),
            mapping_path=str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
            sources_path=str(ROOT / "data" / "core" / "sources.json"),
            allowlist_path=allowlist_path,
            output_dir=str(ROOT / "data" / "authoritative"),
        )

    report = evaluate_effective_authoritative_local_kb(
        index_path=str(ROOT / "data" / "authoritative" / "effective_index.json"),
        entries_path=str(ROOT / "data" / "authoritative" / "effective_entries.jsonl"),
        sources_path=str(ROOT / "data" / "core" / "sources.json"),
        allowlist_path=allowlist_path,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
