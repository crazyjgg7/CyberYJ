import json
from pathlib import Path

from cyberYJ.utils.authoritative_local_kb import (
    build_authoritative_local_kb,
    evaluate_authoritative_local_kb,
    write_authoritative_local_kb,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_authoritative_local_kb_build_and_evaluate(tmp_path):
    mapping_path = tmp_path / "authoritative_text_map.json"
    sources_path = tmp_path / "sources.json"

    _write_json(
        mapping_path,
        {
            "version": "1.0.0",
            "items": [
                {
                    "field_path": "data.core.hexagrams[*].judgment_summary",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "摘要A",
                    "locator": "第1页",
                    "source_ref": ["ctext_yijing"],
                },
                {
                    "field_path": "data.fengshui.flying_stars_periods.periods[*].name",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "摘要B",
                    "locator": "第12页",
                    "source_ref": ["sanmin_dili_bianzheng_shu"],
                },
            ],
        },
    )
    _write_json(
        sources_path,
        [
            {
                "source_id": "ctext_yijing",
                "title": "周易（易经）",
                "edition": "CTP",
                "section": "全文",
                "url_or_archive": "https://ctext.org/book-of-changes",
                "license": "See site terms",
                "notes": "test",
            },
            {
                "source_id": "sanmin_dili_bianzheng_shu",
                "title": "地理辨正疏",
                "edition": "三民版",
                "section": "卷一",
                "url_or_archive": "https://example.com",
                "license": "See site terms",
                "notes": "test",
            },
        ],
    )

    output = write_authoritative_local_kb(
        mapping_path=str(mapping_path),
        sources_path=str(sources_path),
        output_dir=str(tmp_path / "authoritative"),
    )

    assert Path(output["index_path"]).exists()
    assert Path(output["entries_path"]).exists()
    assert output["total_entries"] == 2

    report = evaluate_authoritative_local_kb(
        index_path=output["index_path"],
        entries_path=output["entries_path"],
        sources_path=str(sources_path),
    )
    assert report["passed"] is True
    assert report["total_entries"] == 2
    assert report["unknown_source_refs"] == []
    assert report["count_mismatch"] is False


def test_project_authoritative_local_kb_baseline():
    root = Path("/Users/apple/dev/CyberYJ")
    kb = build_authoritative_local_kb(
        mapping_path=str(root / "data/mappings/authoritative_text_map.json"),
        sources_path=str(root / "data/core/sources.json"),
    )
    assert kb["total_entries"] > 0
    assert kb["source_stats"]
