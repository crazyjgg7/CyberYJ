"""
测试 MCP Server
"""

import json
import pytest

pytest.importorskip("mcp")

from cyberYJ.server import _format_fengshui_result, _format_luopan_result, _format_solar_terms_result


class TestMCPServerFormatting:
    """测试 MCP Server 格式化功能"""

    def test_format_fengshui_result(self):
        """测试格式化风水占卜结果"""
        test_result = {
            "main_hexagram": {
                "id": 1,
                "name": "乾",
                "symbol": "䷀",
                "judgment": "元亨，利贞。",
                "image": "天行健，君子以自强不息。",
                "upper_trigram": "乾",
                "lower_trigram": "乾"
            },
            "five_elements": "上下卦比和（金）",
            "solar_term_influence": "当前节气为立春",
            "fortune_advice": "宜积极进取",
            "do_dont": {
                "do": ["自强不息"],
                "dont": ["骄傲自满"]
            },
            "trace": ["步骤1", "步骤2"],
            "sources": ["来源1"]
        }

        output = _format_fengshui_result(test_result)
        payload = json.loads(output)
        assert payload["tool"] == "fengshui_divination"
        assert payload["data"]["main_hexagram"]["name"] == "乾"
        assert payload["meta"]["success"] is True
        assert "trace" in payload["data"]
        assert "sources" in payload["data"]

    def test_format_luopan_result(self):
        """测试格式化罗盘坐向结果"""
        test_result = {
            "direction_class": "壬山 (北方)",
            "house_gua": "坎宅",
            "sitting_degree": 0.0,
            "facing_degree": 180.0,
            "auspicious_positions": ["生气位（东南方）"],
            "inauspicious_positions": ["绝命位（西方）"],
            "layout_tips": ["主卧宜设在生气位"],
            "trace": ["步骤1", "步骤2"],
            "sources": ["来源1"]
        }

        output = _format_luopan_result(test_result)
        payload = json.loads(output)
        assert payload["tool"] == "luopan_orientation"
        assert payload["data"]["house_gua"] == "坎宅"
        assert payload["meta"]["success"] is True
        assert "trace" in payload["data"]
        assert "sources" in payload["data"]

    def test_format_fengshui_with_changing_hexagram(self):
        """测试带变卦的格式化"""
        test_result = {
            "main_hexagram": {
                "id": 1,
                "name": "乾",
                "symbol": "䷀",
                "judgment": "元亨，利贞。",
                "image": "天行健，君子以自强不息。",
                "upper_trigram": "乾",
                "lower_trigram": "乾"
            },
            "five_elements": "上下卦比和（金）",
            "solar_term_influence": "当前节气为立春",
            "fortune_advice": "宜积极进取",
            "changing_hexagram": {
                "id": 44,
                "name": "姤",
                "judgment": "女壮，勿用取女。",
                "interpretation": "初爻变化说明..."
            },
            "do_dont": {
                "do": ["自强不息", "顺应变化"],
                "dont": ["骄傲自满", "固守成规"]
            },
            "trace": ["步骤1", "步骤2", "步骤3"],
            "sources": ["来源1"]
        }

        output = _format_fengshui_result(test_result)
        payload = json.loads(output)
        assert payload["data"]["changing_hexagram"]["name"] == "姤"
        assert payload["meta"]["success"] is True
        assert "do_dont" in payload["data"]

    def test_format_luopan_with_flying_stars(self):
        """测试带流年飞星的格式化"""
        test_result = {
            "direction_class": "壬山 (北方)",
            "house_gua": "坎宅",
            "sitting_degree": 0.0,
            "facing_degree": 180.0,
            "auspicious_positions": ["生气位（东南方）"],
            "inauspicious_positions": ["绝命位（西方）"],
            "annual_flying_stars": {
                "year": 2024,
                "central_star": 4,
                "palace_map": {
                    "中宫": 4,
                    "坎": 3,
                    "坤": 8
                }
            },
            "layout_tips": ["主卧宜设在生气位"],
            "trace": ["步骤1", "步骤2"],
            "sources": ["来源1"]
        }

        output = _format_luopan_result(test_result)
        payload = json.loads(output)
        assert payload["meta"]["success"] is True
        assert "annual_flying_stars" in payload["data"]

    def test_format_solar_terms_result(self):
        test_result = {
            "solar_term": "立春",
            "solar_longitude": 315.0,
            "longitude": 315.0,
            "days_to_next": 15,
            "next_term": "雨水",
            "trace": ["步骤1"],
            "sources": ["来源1"]
        }
        output = _format_solar_terms_result(test_result)
        payload = json.loads(output)
        assert payload["tool"] == "solar_terms_lookup"
        assert payload["meta"]["success"] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
