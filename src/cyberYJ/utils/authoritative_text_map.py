"""
权威文本替换映射表加载与校验
"""

from typing import Any, Dict, List, Optional
import json
import re

from cyberYJ.utils.data_loader import get_data_loader

ALLOWED_TEXT_KIND = {"summary", "licensed_text", "citation_only"}
ALLOWED_LICENSE = {"public_domain", "licensed", "summary_only", "citation_only"}


def load_authoritative_text_map(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_authoritative_text_map(
    data: Dict[str, Any],
    sources_index: Optional[List[Dict[str, Any]]] = None
) -> List[str]:
    errors: List[str] = []

    if not isinstance(data, dict):
        return ["mapping root must be an object"]

    if "version" not in data:
        errors.append("missing root field: version")

    items = data.get("items")
    if not isinstance(items, list):
        errors.append("items must be a list")
        return errors

    source_ids = None
    if sources_index is not None:
        source_ids = {s.get("source_id") for s in sources_index}

    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"items[{idx}] must be an object")
            continue

        field_path = item.get("field_path")
        if not field_path or not isinstance(field_path, str):
            errors.append(f"items[{idx}].field_path is required and must be string")

        text_kind = item.get("text_kind")
        if text_kind not in ALLOWED_TEXT_KIND:
            errors.append(
                f"items[{idx}].text_kind must be one of {sorted(ALLOWED_TEXT_KIND)}"
            )

        license_kind = item.get("license")
        if license_kind not in ALLOWED_LICENSE:
            errors.append(
                f"items[{idx}].license must be one of {sorted(ALLOWED_LICENSE)}"
            )

        if text_kind != "citation_only":
            content = item.get("content")
            if not content or not isinstance(content, str):
                errors.append(f"items[{idx}].content is required for text_kind != citation_only")

        source_ref = item.get("source_ref")
        if not isinstance(source_ref, list) or not source_ref:
            errors.append(f"items[{idx}].source_ref must be a non-empty list")
        else:
            if source_ids is not None:
                for sid in source_ref:
                    if sid not in source_ids:
                        errors.append(f"items[{idx}].source_ref unknown source_id: {sid}")

    return errors


def validate_authoritative_text_map_file(path: str) -> List[str]:
    data = load_authoritative_text_map(path)
    sources_index = get_data_loader().get_sources()
    return validate_authoritative_text_map(data, sources_index)


_CORE_HEX_JUDGMENT = re.compile(r"hexagrams\[\?\(@\.id==(?P<id>\d+)\)\]\.judgment_summary$")
_CORE_HEX_IMAGE = re.compile(r"hexagrams\[\?\(@\.id==(?P<id>\d+)\)\]\.image_summary$")
_SCENARIO_FIELD = re.compile(
    r"data\.scenarios\.(?P<scenario>\w+)\.hexagrams(?:\['(?P<id>\d+)'\]|\[\*\])\.(?P<field>\w+)$"
)
_SCENARIO_SPECIFIC = re.compile(
    r"data\.scenarios\.(?P<scenario>\w+)\.hexagrams(?:\['(?P<id>\d+)'\]|\[\*\])\.scenario_specific(?:\.(?P<sub>[^\.]+)|\[\*\])\.(?P<field>\w+)$"
)
_SOLAR_TERMS_FIELD = re.compile(
    r"data\.core\.solar_terms(?:\[[^]]*name=='(?P<name>[^']+)'[^]]*\])?(?:\.(?P<field>\w+))?"
)
_FENGSHUI_FIELD = re.compile(
    r"data\.fengshui\.(?P<section>\w+)(?:\.(?P<field>\w+))?"
)


def match_mapping_item(
    item: Dict[str, Any],
    hexagram_id: int,
    scenario_code: Optional[str]
) -> Optional[Dict[str, str]]:
    field_path = item.get("field_path")
    if not isinstance(field_path, str):
        return None

    m = _CORE_HEX_JUDGMENT.search(field_path)
    if m and int(m.group("id")) == hexagram_id:
        return {"target": "main_hexagram.judgment", "field_path": field_path}

    m = _CORE_HEX_IMAGE.search(field_path)
    if m and int(m.group("id")) == hexagram_id:
        return {"target": "main_hexagram.image", "field_path": field_path}

    m = _SCENARIO_FIELD.search(field_path)
    if m and scenario_code and m.group("scenario") == scenario_code:
        item_id = m.group("id")
        if item_id is None or int(item_id) == hexagram_id:
            field = m.group("field")
            return {"target": f"scenario_analysis.{field}", "field_path": field_path}

    m = _SCENARIO_SPECIFIC.search(field_path)
    if m and scenario_code and m.group("scenario") == scenario_code:
        item_id = m.group("id")
        if item_id is None or int(item_id) == hexagram_id:
            sub = m.group("sub")
            if sub is None:
                sub = "*"
            field = m.group("field")
            return {
                "target": f"scenario_specific.{sub}.{field}",
                "field_path": field_path
            }

    return None


def match_solar_terms_item(
    item: Dict[str, Any],
    term_name: str
) -> Optional[Dict[str, str]]:
    field_path = item.get("field_path")
    if not isinstance(field_path, str):
        return None

    m = _SOLAR_TERMS_FIELD.search(field_path)
    if not m:
        return None

    name = m.group("name")
    if name and name != term_name:
        return None

    return {
        "target": "solar_terms",
        "field": m.group("field") or "",
        "field_path": field_path
    }


def match_luopan_item(item: Dict[str, Any]) -> Optional[Dict[str, str]]:
    field_path = item.get("field_path")
    if not isinstance(field_path, str):
        return None

    m = _FENGSHUI_FIELD.search(field_path)
    if not m:
        return None

    return {
        "target": "luopan",
        "section": m.group("section"),
        "field": m.group("field") or "",
        "field_path": field_path
    }
