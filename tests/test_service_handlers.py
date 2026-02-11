from cyberYJ.server.handlers.solar_terms import SolarTermsHandler
from cyberYJ.server.handlers.compass import CompassHandler
from cyberYJ.server.handlers.fengshui import FengshuiHandler


def test_solar_terms_lookup_basic():
    handler = SolarTermsHandler()
    result = handler.execute(
        {
            "timestamp": "2026-02-10T00:00:00+08:00",
            "timezone": "Asia/Shanghai",
        }
    )

    assert result["solar_term"]
    assert "solar_longitude" in result
    assert "trace" in result and len(result["trace"]) > 0
    assert "sources" in result and len(result["sources"]) > 0


def test_luopan_orientation_basic():
    handler = CompassHandler()
    result = handler.execute(
        {
            "sitting_direction": "坐北朝南",
            "building_type": "住宅",
            "timestamp": "2026-02-10T00:00:00+08:00",
            "timezone": "Asia/Shanghai",
        }
    )

    assert "direction_class" in result
    assert "house_gua" in result
    assert "auspicious_positions" in result
    assert "inauspicious_positions" in result
    assert "trace" in result and len(result["trace"]) > 0
    assert "sources" in result and len(result["sources"]) > 0


def test_luopan_orientation_missing_required():
    handler = CompassHandler()
    try:
        handler.execute({"building_type": "住宅"})
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "sitting_direction" in str(exc)


def test_solar_terms_invalid_timezone():
    handler = SolarTermsHandler()
    try:
        handler.execute({"timezone": "Invalid/Timezone"})
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "无效时区" in str(exc)


def test_luopan_invalid_building_type():
    handler = CompassHandler()
    try:
        handler.execute(
            {
                "sitting_direction": "坐北朝南",
                "building_type": "别墅",
            }
        )
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "building_type" in str(exc)


def test_fengshui_invalid_changing_line():
    handler = FengshuiHandler()
    try:
        handler.execute(
            {
                "upper_trigram": "乾",
                "lower_trigram": "坤",
                "changing_line": 7,
            }
        )
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "changing_line" in str(exc)
