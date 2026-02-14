from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WECHAT_ROOT = PROJECT_ROOT / "Wechat-ZY"

SCAN_SUFFIXES = {".js", ".json", ".wxml"}
EXCLUDED_PARTS = {"docs", ".agent", "tests"}
FORBIDDEN_TERMS = (
    "卜卦",
    "占卜",
    "算命",
    "运势",
    "吉凶",
    "趋吉避凶",
    "摇卦",
    "问事",
    "求得一卦",
    "诚心摇卦",
)


def _iter_frontend_files():
    for path in WECHAT_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        yield path


def test_wechat_frontend_text_avoids_fortune_telling_terms():
    violations = []
    for file_path in _iter_frontend_files():
        content = file_path.read_text(encoding="utf-8")
        for term in FORBIDDEN_TERMS:
            if term in content:
                violations.append(f"{file_path.relative_to(PROJECT_ROOT)} -> {term}")

    assert not violations, "发现疑似审核风险词:\n" + "\n".join(violations[:50])
