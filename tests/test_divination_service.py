from cyberYJ.api.divination_service import DivinationService


def test_service_returns_contract_shape():
    service = DivinationService()
    result = service.interpret([6, 7, 8, 9, 7, 7], question="事业发展")
    assert "hexagram" in result
    assert "analysis" in result
    assert "do_dont" in result
    assert "trace" in result
    assert "sources" in result


def test_service_hexagram_core_fields():
    service = DivinationService()
    result = service.interpret([8, 8, 8, 9, 8, 8], question="测试变卦")
    assert result["hexagram"]["code"] == "000100"
    assert result["hexagram"]["upper_trigram"] == "艮"
    assert result["hexagram"]["lower_trigram"] == "坤"
    assert "five_elements" in result["analysis"]
    assert "solar_term" in result["analysis"]
    assert "advice" in result["analysis"]


def test_changing_hexagram_is_null_when_no_changing_lines():
    service = DivinationService()
    result = service.interpret([7, 7, 8, 8, 7, 8], question=None)
    assert result["changing_hexagram"] is None
    assert result["analysis"]["active_lines"] == []


def test_multiple_changing_lines_keep_array_shape():
    service = DivinationService()
    result = service.interpret([6, 9, 8, 9, 6, 7], question="测试")
    assert isinstance(result["analysis"]["active_lines"], list)
    assert len(result["analysis"]["active_lines"]) == 4
    assert isinstance(result["do_dont"]["do"], list)
    assert isinstance(result["do_dont"]["dont"], list)


def test_scene_type_has_priority_over_question_keyword():
    service = DivinationService()
    result = service.interpret(
        coins=[6, 7, 8, 9, 7, 8],
        question="我想问事业",
        scene_type="love",
    )
    assert result["scene_type"] == "love"


def test_response_contains_scene_enhancement_fields():
    service = DivinationService()
    result = service.interpret(
        [6, 7, 8, 9, 7, 8],
        question="问事业",
        scene_type="career",
    )
    assert "scene_type" in result
    assert "keywords" in result and isinstance(result["keywords"], list)
    assert "advice_tags" in result and isinstance(result["advice_tags"], list)
    assert "score" in result and isinstance(result["score"], int)


def test_guard_tone_has_no_attack_phrase_conflict():
    service = DivinationService()
    result = service.interpret(
        coins=[7, 8, 7, 8, 8, 8],
        question="问感情",
        scene_type="love",
    )
    assert result["consistency"]["tone"] == "guard"
    assert result["consistency"]["conflict_count"] == 0
