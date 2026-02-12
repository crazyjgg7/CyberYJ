from pydantic import ValidationError

from cyberYJ.api.models import DivinationRequest


def test_divination_request_rejects_invalid_length():
    try:
        DivinationRequest(coins=[6, 7, 8])
        assert False, "expected ValidationError"
    except ValidationError:
        assert True


def test_divination_request_rejects_invalid_coin_value():
    try:
        DivinationRequest(coins=[6, 7, 8, 9, 7, 1])
        assert False, "expected ValidationError"
    except ValidationError:
        assert True


def test_divination_request_accepts_six_valid_coins():
    req = DivinationRequest(coins=[6, 7, 8, 9, 7, 8], question="事业")
    assert req.coins == [6, 7, 8, 9, 7, 8]
    assert req.question == "事业"
