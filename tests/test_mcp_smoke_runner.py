from cyberYJ.tools.mcp_smoke import DEFAULT_SMOKE_CASES, validate_response_payload


def test_default_smoke_cases_fixed_two_keywords():
    assert len(DEFAULT_SMOKE_CASES) == 2
    assert DEFAULT_SMOKE_CASES[0]["text"] == "风水：上坤下乾，问事业"
    assert DEFAULT_SMOKE_CASES[0]["expected_tool"] == "fengshui_divination"
    assert DEFAULT_SMOKE_CASES[1]["text"] == "罗盘：坐北朝南 住宅"
    assert DEFAULT_SMOKE_CASES[1]["expected_tool"] == "luopan_orientation"


def test_validate_response_payload_requires_protocol_fields():
    errors = validate_response_payload({"tool": "fengshui_divination"}, "fengshui_divination")
    assert "missing field: data" in errors
    assert "missing field: meta" in errors


def test_validate_response_payload_requires_trace_and_sources():
    payload = {
        "tool": "luopan_orientation",
        "data": {},
        "meta": {"success": True}
    }
    errors = validate_response_payload(payload, "luopan_orientation")
    assert "data.trace must exist" in errors
    assert "data.sources must exist" in errors


def test_validate_response_payload_ok():
    payload = {
        "tool": "fengshui_divination",
        "data": {
            "trace": ["step1"],
            "sources": ["source1"]
        },
        "meta": {"success": True}
    }
    errors = validate_response_payload(payload, "fengshui_divination")
    assert errors == []
