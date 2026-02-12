#!/usr/bin/env python3
"""
校验本地权威知识库产物一致性。
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

from cyberYJ.utils.authoritative_local_kb import (
    evaluate_authoritative_local_kb,
    write_authoritative_local_kb,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="先重新生成本地权威知识库")
    args = parser.parse_args()

    if args.refresh:
        write_authoritative_local_kb(
            mapping_path=str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
            sources_path=str(ROOT / "data" / "core" / "sources.json"),
            output_dir=str(ROOT / "data" / "authoritative"),
        )

    report = evaluate_authoritative_local_kb(
        index_path=str(ROOT / "data" / "authoritative" / "index.json"),
        entries_path=str(ROOT / "data" / "authoritative" / "entries.jsonl"),
        sources_path=str(ROOT / "data" / "core" / "sources.json"),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
