from cyberYJ.dialog.router import route_message


def test_route_fengshui_basic():
    result = route_message("风水：上坤下乾，问事业")
    assert result["tool"] == "fengshui_divination"
    assert result["arguments"]["upper_trigram"] == "坤"
    assert result["arguments"]["lower_trigram"] == "乾"
    assert result["arguments"]["question_type"] == "事业"


def test_route_fengshui_changing_line():
    result = route_message("风水：上乾下坤 初爻变")
    assert result["tool"] == "fengshui_divination"
    assert result["arguments"]["changing_line"] == 1


def test_route_luopan_basic():
    result = route_message("罗盘：坐北朝南 住宅")
    assert result["tool"] == "luopan_orientation"
    assert result["arguments"]["sitting_direction"] == "坐北朝南"
    assert result["arguments"]["building_type"] == "住宅"


def test_route_luopan_apartment():
    result = route_message("罗盘：坐北朝南 公寓")
    assert result["arguments"]["building_type"] == "住宅"


def test_route_luopan_birth():
    result = route_message("罗盘：坐亥向巳 办公室 1990-05-15")
    assert result["arguments"]["owner_birth"] == "1990-05-15"


def test_route_unknown_prefix():
    result = route_message("帮我看下风水")
    assert "error" in result
