import json
from pathlib import Path

from cyberYJ.utils.authoritative_convention_gap import (
    evaluate_authoritative_convention_gap,
)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_authoritative_convention_gap_shape():
    report = evaluate_authoritative_convention_gap(
        "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
    )
    assert "total_summary_items" in report
    assert "convention_only_items" in report
    assert "mixed_convention_items" in report
    assert "convention_only_ratio" in report
    assert "by_module" in report
    assert "convention_only_field_paths" in report
    assert "allowed_convention_only_fields" in report
    assert "unexpected_convention_only_fields" in report
    assert "passed" in report


def test_authoritative_convention_gap_project_baseline():
    report = evaluate_authoritative_convention_gap(
        "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
    )
    assert report["total_summary_items"] >= 150
    assert report["mixed_convention_items"] == 0
    assert report["convention_only_items"] <= 18


def test_authoritative_convention_gap_counts(tmp_path):
    path = tmp_path / "authoritative_text_map.json"
    _write_json(
        path,
        {
            "version": "1.0.0",
            "items": [
                {
                    "field_path": "data.core.hexagrams[*].judgment_summary",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "摘要",
                    "source_ref": ["convention"],
                },
                {
                    "field_path": "data.fengshui.ba_zhai.rules",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "摘要",
                    "source_ref": ["ctext_yijing"],
                },
                {
                    "field_path": "data.scenarios.career.hexagrams[*].overall_tendency",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "摘要",
                    "source_ref": ["convention", "ctext_yijing"],
                },
            ],
        },
    )

    report = evaluate_authoritative_convention_gap(str(path), convention_only_threshold=1)
    assert report["total_summary_items"] == 3
    assert report["convention_only_items"] == 1
    assert report["mixed_convention_items"] == 1
    assert report["passed"] is False


def test_authoritative_convention_gap_allowlist(tmp_path):
    mapping_path = tmp_path / "authoritative_text_map.json"
    allowlist_path = tmp_path / "allowlist.json"

    _write_json(
        mapping_path,
        {
            "version": "1.0.0",
            "items": [
                {
                    "field_path": "data.scenarios.career.prompt_template",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "模板摘要",
                    "source_ref": ["convention"],
                },
                {
                    "field_path": "data.scenarios.career.output_structure",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "结构摘要",
                    "source_ref": ["convention"],
                },
            ],
        },
    )
    _write_json(
        allowlist_path,
        {
            "version": "1.0.0",
            "allowed_convention_only_field_paths": [
                "data.scenarios.career.prompt_template"
            ],
        },
    )

    report = evaluate_authoritative_convention_gap(
        str(mapping_path),
        convention_only_threshold=2,
        allowlist_path=str(allowlist_path),
    )
    assert report["convention_only_items"] == 2
    assert report["allowed_convention_only_fields"] == [
        "data.scenarios.career.prompt_template"
    ]
    assert report["unexpected_convention_only_fields"] == [
        "data.scenarios.career.output_structure"
    ]
    assert report["passed"] is False
