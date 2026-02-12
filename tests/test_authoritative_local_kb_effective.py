import json
from pathlib import Path

from cyberYJ.utils.authoritative_local_kb_effective import (
    build_effective_authoritative_local_kb,
    evaluate_effective_authoritative_local_kb,
    write_effective_authoritative_local_kb,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_effective_local_kb_build_and_evaluate(tmp_path):
    data_root = tmp_path / "data"
    mapping_path = tmp_path / "authoritative_text_map.json"
    sources_path = tmp_path / "sources.json"
    allowlist_path = tmp_path / "convention_allowlist.json"

    _write_json(
        data_root / "core" / "hexagrams.json",
        [{"id": 1, "judgment_summary": "元吉"}],
    )
    _write_json(
        mapping_path,
        {
            "version": "1.0.0",
            "items": [
                {
                    "field_path": "data.core.hexagrams[*]",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "卦象结构摘要",
                    "locator": "第1页",
                    "source_ref": ["ctext_yijing"],
                },
                {
                    "field_path": "data.core.hexagrams[*].judgment_summary",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "卦辞摘要",
                    "locator": "第1页",
                    "source_ref": ["ctext_yijing"],
                }
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
            }
        ],
    )
    _write_json(
        allowlist_path,
        {
            "version": "1.0.0",
            "allowed_convention_only_field_paths": [],
        },
    )

    output = write_effective_authoritative_local_kb(
        data_root=str(data_root),
        mapping_path=str(mapping_path),
        sources_path=str(sources_path),
        allowlist_path=str(allowlist_path),
        output_dir=str(tmp_path / "authoritative"),
    )
    assert Path(output["index_path"]).exists()
    assert Path(output["entries_path"]).exists()
    assert output["total_fields"] >= 1
    assert output["unresolved_fields_count"] == 0

    report = evaluate_effective_authoritative_local_kb(
        index_path=output["index_path"],
        entries_path=output["entries_path"],
        sources_path=str(sources_path),
        allowlist_path=str(allowlist_path),
    )
    assert report["passed"] is True
    assert report["unresolved_fields_count"] == 0
    assert report["unknown_source_refs"] == []
    assert report["unexpected_convention_fields_count"] == 0


def test_effective_local_kb_project_baseline():
    root = Path("/Users/apple/dev/CyberYJ")
    report = build_effective_authoritative_local_kb(
        data_root=str(root / "data"),
        mapping_path=str(root / "data/mappings/authoritative_text_map.json"),
        sources_path=str(root / "data/core/sources.json"),
        allowlist_path=str(root / "data/core/convention_allowlist.json"),
    )
    assert report["total_fields"] >= 610
    assert report["unresolved_fields_count"] == 0
    assert report["unexpected_convention_fields_count"] == 0


def test_effective_local_kb_unexpected_convention_field(tmp_path):
    data_root = tmp_path / "data"
    mapping_path = tmp_path / "authoritative_text_map.json"
    sources_path = tmp_path / "sources.json"
    allowlist_path = tmp_path / "convention_allowlist.json"

    _write_json(
        data_root / "scenarios" / "career.json",
        {
            "prompt_template": "test",
        },
    )
    _write_json(
        mapping_path,
        {
            "version": "1.0.0",
            "items": [
                {
                    "field_path": "data.scenarios.career",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "场景对象",
                    "locator": "内部模板",
                    "source_ref": ["convention"],
                },
                {
                    "field_path": "data.scenarios.career.prompt_template",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "模板",
                    "locator": "内部模板",
                    "source_ref": ["convention"],
                }
            ],
        },
    )
    _write_json(
        sources_path,
        [
            {
                "source_id": "convention",
                "title": "行业惯例汇编",
                "edition": "internal",
                "section": "templates",
                "url_or_archive": "https://example.com",
                "license": "summary_only",
                "notes": "test",
            }
        ],
    )
    _write_json(
        allowlist_path,
        {
            "version": "1.0.0",
            "allowed_convention_only_field_paths": [],
        },
    )

    report = build_effective_authoritative_local_kb(
        data_root=str(data_root),
        mapping_path=str(mapping_path),
        sources_path=str(sources_path),
        allowlist_path=str(allowlist_path),
    )
    assert report["total_fields"] >= 1
    assert report["unresolved_fields_count"] == 0
    assert report["unexpected_convention_fields_count"] >= 1
    assert report["passed"] is False
