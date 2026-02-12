"""
M4 字段清单与映射缺口报告测试
"""

import json
from pathlib import Path

from cyberYJ.utils.m4_mapping_gap import (
    build_m4_field_inventory,
    evaluate_m4_mapping_gap,
    normalize_mapping_field_path,
)


def _write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def test_normalize_mapping_field_path():
    assert (
        normalize_mapping_field_path("hexagrams[?(@.id==11)].judgment_summary")
        == "data.core.hexagrams[*].judgment_summary"
    )
    assert (
        normalize_mapping_field_path(
            "data.scenarios.career.hexagrams['11'].scenario_specific.求职.situation"
        )
        == "data.scenarios.career.hexagrams[*].scenario_specific[*].situation"
    )


def test_build_inventory_and_evaluate_gap(tmp_path):
    data_root = tmp_path / "data"
    mapping_path = tmp_path / "authoritative_text_map.json"

    _write_json(
        data_root / "core" / "hexagrams.json",
        [{"id": 1, "judgment_summary": "元吉", "image_summary": "天行健"}],
    )
    _write_json(
        data_root / "core" / "solar_terms.json",
        [{"id": 1, "name": "立春", "solar_longitude_deg": 315}],
    )
    _write_json(
        data_root / "scenarios" / "career.json",
        {
            "hexagrams": {
                "1": {
                    "overall_tendency": "吉",
                    "scenario_specific": {
                        "求职": {"situation": "机会明显"}
                    },
                }
            }
        },
    )
    _write_json(
        data_root / "fengshui" / "flying_stars_scoring.json",
        {"stars": {"1": {"score": 2, "nature": "吉"}}},
    )

    _write_json(
        mapping_path,
        {
            "version": "1.0.0",
            "items": [
                {
                    "field_path": "hexagrams[?(@.id==11)].judgment_summary",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "卦辞摘要",
                    "source_ref": ["ctext_yijing"],
                },
                {
                    "field_path": "data.scenarios.career.hexagrams['11'].overall_tendency",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "事业倾向摘要",
                    "source_ref": ["convention"],
                },
                {
                    "field_path": "data.fengshui.flying_stars_scoring.stars",
                    "text_kind": "summary",
                    "license": "summary_only",
                    "content": "九星评分摘要",
                    "source_ref": ["cinii_dili_bianzheng_shu"],
                },
            ],
        },
    )

    inventory = build_m4_field_inventory(str(data_root))
    fields = {item["field_path"] for item in inventory["fields"]}
    assert "data.core.hexagrams[*].judgment_summary" in fields
    assert "data.scenarios.career.hexagrams[*].scenario_specific[*].situation" in fields
    assert "data.fengshui.flying_stars_scoring.stars[*].score" in fields

    report = evaluate_m4_mapping_gap(inventory, str(mapping_path))

    assert report["mapped_fields"] > 0
    assert report["coverage_ratio"] < 1.0
    assert (
        "data.scenarios.career.hexagrams[*].scenario_specific[*].situation"
        in report["unmapped_fields"]
    )
    assert report["modules"]["core"]["mapped_fields"] >= 1
    assert report["modules"]["fengshui"]["mapped_fields"] >= 1


def test_project_mapping_gap_fully_covered():
    root = Path("/Users/apple/dev/CyberYJ")
    inventory = build_m4_field_inventory(str(root / "data"))
    report = evaluate_m4_mapping_gap(
        inventory=inventory,
        mapping_path=str(root / "data/mappings/authoritative_text_map.json"),
    )
    assert report["total_fields"] > 0
    assert report["unmapped_fields_count"] == 0
