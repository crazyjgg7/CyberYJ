# Xuan Kong Flying Stars V2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add “宅盘 + 流年叠加” to `luopan_orientation` so it can output current auspicious/inauspicious positions.

**Architecture:** Introduce three data tables (periods, house rules, scoring) loaded by `DataLoader`. A small calculator combines house base stars + annual stars using scoring rules to produce `combined_flying_stars` and current auspicious/inauspicious positions, with clear trace + sources.

**Tech Stack:** Python 3.9+, pytest, existing `DataLoader` + MCP tools.

---

### Task 1: Add 玄空“元运”数据与加载器

**Files:**
- Create: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/fengshui/flying_stars_periods.json`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/utils/data_loader.py`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/README.md`

**Step 1: Write the failing tests**

Add to `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py`:

```python
    def test_get_flying_star_periods(self):
        periods = self.loader.get_flying_star_periods()
        assert len(periods) >= 9
        assert all('period' in p for p in periods)
        assert all('start_year' in p for p in periods)
        assert all('end_year' in p for p in periods)

    def test_get_flying_star_period_by_year(self):
        p2024 = self.loader.get_flying_star_period_by_year(2024)
        assert p2024 is not None
        assert p2024['period'] == 9
```

**Step 2: Run test to verify it fails**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py::TestDataLoader::test_get_flying_star_periods -v`

Expected: FAIL with `AttributeError: 'DataLoader' object has no attribute 'get_flying_star_periods'`

**Step 3: Write minimal implementation**

Create `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/fengshui/flying_stars_periods.json`:

```json
[
  {"period": 1, "start_year": 1864, "end_year": 1883, "source_ref": "convention"},
  {"period": 2, "start_year": 1884, "end_year": 1903, "source_ref": "convention"},
  {"period": 3, "start_year": 1904, "end_year": 1923, "source_ref": "convention"},
  {"period": 4, "start_year": 1924, "end_year": 1943, "source_ref": "convention"},
  {"period": 5, "start_year": 1944, "end_year": 1963, "source_ref": "convention"},
  {"period": 6, "start_year": 1964, "end_year": 1983, "source_ref": "convention"},
  {"period": 7, "start_year": 1984, "end_year": 2003, "source_ref": "convention"},
  {"period": 8, "start_year": 2004, "end_year": 2023, "source_ref": "convention"},
  {"period": 9, "start_year": 2024, "end_year": 2043, "source_ref": "convention"}
]
```

Modify `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/utils/data_loader.py`:

```python
    def get_flying_star_periods(self) -> List[Dict[str, Any]]:
        if 'flying_star_periods' not in self._cache:
            self._cache['flying_star_periods'] = self._load_json(
                'flying_stars_periods.json', 'fengshui'
            )
        return self._cache['flying_star_periods']

    def get_flying_star_period_by_year(self, year: int) -> Optional[Dict[str, Any]]:
        for period in self.get_flying_star_periods():
            if period['start_year'] <= year <= period['end_year']:
                return period
        return None
```

Update `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/README.md` to add the new file description.

**Step 4: Run test to verify it passes**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py::TestDataLoader::test_get_flying_star_periods -v`

Expected: PASS

**Step 5: Commit**

```bash
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 add data/fengshui/flying_stars_periods.json src/cyberYJ/utils/data_loader.py tests/test_data_loader.py data/README.md
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 commit -m "feat: add flying star period data"
```

---

### Task 2: 添加宅盘规则表 + 评分表

**Files:**
- Create: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/fengshui/flying_stars_house.json`
- Create: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/fengshui/flying_stars_scoring.json`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/utils/data_loader.py`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/README.md`

**Step 1: Write the failing tests**

Add to `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py`:

```python
    def test_get_flying_star_house_rule(self):
        rule = self.loader.get_flying_star_house_rule(period=9, sitting_mountain='壬')
        assert rule is not None
        assert rule['period'] == 9
        assert rule['sitting_mountain'] == '壬'
        assert 'palace_map' in rule

    def test_get_flying_star_scoring(self):
        scoring = self.loader.get_flying_star_scoring()
        assert 'stars' in scoring
        assert '1' in scoring['stars']
        assert 'score' in scoring['stars']['1']
```

**Step 2: Run test to verify it fails**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py::TestDataLoader::test_get_flying_star_house_rule -v`

Expected: FAIL with `AttributeError: 'DataLoader' object has no attribute 'get_flying_star_house_rule'`

**Step 3: Write minimal implementation**

Create `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/fengshui/flying_stars_house.json` (MVP: 仅“壬山 + 九运”，后续可补全 24 山向)：

```json
[
  {
    "period": 9,
    "sitting_mountain": "壬",
    "palace_map": {
      "中宫": {"mountain_star": 9, "facing_star": 9},
      "坎": {"mountain_star": 8, "facing_star": 1},
      "坤": {"mountain_star": 2, "facing_star": 8},
      "震": {"mountain_star": 7, "facing_star": 2},
      "巽": {"mountain_star": 3, "facing_star": 7},
      "乾": {"mountain_star": 6, "facing_star": 4},
      "兑": {"mountain_star": 1, "facing_star": 6},
      "艮": {"mountain_star": 5, "facing_star": 3},
      "离": {"mountain_star": 4, "facing_star": 5}
    },
    "source_ref": "convention"
  }
]
```

Create `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/fengshui/flying_stars_scoring.json`:

```json
{
  "version": "v1",
  "stars": {
    "1": {"score": 2, "label": "吉"},
    "2": {"score": -2, "label": "凶"},
    "3": {"score": -2, "label": "凶"},
    "4": {"score": 2, "label": "吉"},
    "5": {"score": -3, "label": "凶"},
    "6": {"score": 2, "label": "吉"},
    "7": {"score": -1, "label": "凶"},
    "8": {"score": 3, "label": "吉"},
    "9": {"score": 2, "label": "吉"}
  },
  "source_ref": "convention"
}
```

Modify `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/utils/data_loader.py`:

```python
    def get_flying_star_house_rules(self) -> List[Dict[str, Any]]:
        if 'flying_star_house' not in self._cache:
            self._cache['flying_star_house'] = self._load_json(
                'flying_stars_house.json', 'fengshui'
            )
        return self._cache['flying_star_house']

    def get_flying_star_house_rule(self, period: int, sitting_mountain: str) -> Optional[Dict[str, Any]]:
        for rule in self.get_flying_star_house_rules():
            if rule['period'] == period and rule['sitting_mountain'] == sitting_mountain:
                return rule
        return None

    def get_flying_star_scoring(self) -> Dict[str, Any]:
        if 'flying_star_scoring' not in self._cache:
            self._cache['flying_star_scoring'] = self._load_json(
                'flying_stars_scoring.json', 'fengshui'
            )
        return self._cache['flying_star_scoring']
```

Update `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/data/README.md` to add new file descriptions.

**Step 4: Run test to verify it passes**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_data_loader.py::TestDataLoader::test_get_flying_star_house_rule -v`

Expected: PASS

**Step 5: Commit**

```bash
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 add data/fengshui/flying_stars_house.json data/fengshui/flying_stars_scoring.json src/cyberYJ/utils/data_loader.py tests/test_data_loader.py data/README.md
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 commit -m "feat: add house rules and scoring tables"
```

---

### Task 3: 叠加计算器（宅盘 + 流年）

**Files:**
- Create: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/core/flying_star_calculator.py`
- Test: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_flying_star_calculator.py`

**Step 1: Write the failing tests**

Create `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_flying_star_calculator.py`:

```python
from cyberYJ.core.flying_star_calculator import combine_flying_stars

def test_combine_flying_stars_basic():
    house_map = {
        "中宫": {"mountain_star": 9, "facing_star": 9},
        "坎": {"mountain_star": 8, "facing_star": 1}
    }
    annual_map = {"中宫": 2, "坎": 1}
    scoring = {
        "stars": {
            "1": {"score": 2},
            "2": {"score": -2},
            "8": {"score": 3},
            "9": {"score": 2}
        }
    }

    combined, auspicious, inauspicious = combine_flying_stars(house_map, annual_map, scoring)

    assert "中宫" in combined
    assert "坎" in combined
    assert combined["中宫"]["score"] == 2
    assert "坎" in auspicious
```

**Step 2: Run test to verify it fails**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_flying_star_calculator.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'cyberYJ.core.flying_star_calculator'`

**Step 3: Write minimal implementation**

Create `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/core/flying_star_calculator.py`:

```python
from typing import Dict, Tuple, List

def _score_star(scoring: Dict[str, Dict[str, int]], star: int) -> int:
    entry = scoring.get(str(star))
    if not entry:
        return 0
    return int(entry.get("score", 0))

def combine_flying_stars(
    house_map: Dict[str, Dict[str, int]],
    annual_map: Dict[str, int],
    scoring: Dict[str, Dict[str, int]],
    auspicious_threshold: int = 2,
    inauspicious_threshold: int = -2
) -> Tuple[Dict[str, Dict[str, int]], List[str], List[str]]:
    combined: Dict[str, Dict[str, int]] = {}
    auspicious: List[str] = []
    inauspicious: List[str] = []

    for palace, house_stars in house_map.items():
        annual_star = annual_map.get(palace)
        if annual_star is None:
            continue

        mountain_star = house_stars.get("mountain_star")
        facing_star = house_stars.get("facing_star")

        score = (
            _score_star(scoring, mountain_star) +
            _score_star(scoring, facing_star) +
            _score_star(scoring, annual_star)
        )

        level = "neutral"
        if score >= auspicious_threshold:
            level = "auspicious"
            auspicious.append(palace)
        elif score <= inauspicious_threshold:
            level = "inauspicious"
            inauspicious.append(palace)

        combined[palace] = {
            "mountain_star": mountain_star,
            "facing_star": facing_star,
            "annual_star": annual_star,
            "score": score,
            "level": level
        }

    return combined, auspicious, inauspicious
```

**Step 4: Run test to verify it passes**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_flying_star_calculator.py -v`

Expected: PASS

**Step 5: Commit**

```bash
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 add src/cyberYJ/core/flying_star_calculator.py tests/test_flying_star_calculator.py
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 commit -m "feat: add flying star combination calculator"
```

---

### Task 4: 接入 luopan_orientation 输出“当前吉凶位”

**Files:**
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/tools/luopan_orientation.py`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_luopan_orientation.py`

**Step 1: Write the failing tests**

Add to `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_luopan_orientation.py`:

```python
    def test_house_flying_stars_combined(self):
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            timestamp="2026-06-01T10:00:00+08:00"
        )

        assert 'house_flying_stars' in result
        assert 'combined_flying_stars' in result
        assert 'current_auspicious_positions' in result
        assert 'current_inauspicious_positions' in result
        assert isinstance(result['current_auspicious_positions'], list)
        assert isinstance(result['current_inauspicious_positions'], list)
```

**Step 2: Run test to verify it fails**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_luopan_orientation.py::TestLuopanOrientationTool::test_house_flying_stars_combined -v`

Expected: FAIL with assertion error (missing fields)

**Step 3: Write minimal implementation**

Modify `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/src/cyberYJ/tools/luopan_orientation.py`:

```python
from cyberYJ.core.flying_star_calculator import combine_flying_stars

# ... inside execute(), after annual_flying_stars is computed:
        period_info = self.data_loader.get_flying_star_period_by_year(year)
        house_rule = None
        if period_info:
            house_rule = self.data_loader.get_flying_star_house_rule(
                period=period_info['period'],
                sitting_mountain=direction_info['sitting_mountain']
            )

        combined = None
        current_auspicious = []
        current_inauspicious = []

        scoring = self.data_loader.get_flying_star_scoring()
        scoring_table = scoring.get('stars', {})

        if house_rule and flying_stars:
            combined, current_auspicious, current_inauspicious = combine_flying_stars(
                house_rule['palace_map'],
                flying_stars['palace_map'],
                scoring_table
            )
            trace.append(f"元运: 第{period_info['period']}运（{period_info['start_year']}-{period_info['end_year']}）")
            trace.append(f"宅盘命中: {direction_info['sitting_mountain']}山")
            trace.append("飞星叠加: 宅盘 + 流年")
        else:
            trace.append("飞星叠加: 缺少宅盘或流年数据，降级为仅流年年盘")

        if house_rule:
            result["house_flying_stars"] = {
                "period": period_info['period'] if period_info else None,
                "sitting_mountain": house_rule['sitting_mountain'],
                "palace_map": house_rule['palace_map']
            }

        if combined:
            result["combined_flying_stars"] = combined
            result["current_auspicious_positions"] = current_auspicious
            result["current_inauspicious_positions"] = current_inauspicious
```

**Step 4: Run test to verify it passes**

Run: `pytest /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests/test_luopan_orientation.py::TestLuopanOrientationTool::test_house_flying_stars_combined -v`

Expected: PASS

**Step 5: Commit**

```bash
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 add src/cyberYJ/tools/luopan_orientation.py tests/test_luopan_orientation.py
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 commit -m "feat: add house+annual flying stars to luopan"
```

---

### Task 5: 文档更新（V2 说明）

**Files:**
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/docs/requirements.md`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/docs/project-progress.md`
- Modify: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/docs/mcp-server-guide.md` (可选，输出字段说明)

**Step 1: Write the failing test**

No automated tests; skip.

**Step 2: Run doc lint (optional)**

Skip.

**Step 3: Update docs**

- `requirements.md`: V2 增加“宅盘 + 流年叠加”与输出字段
- `project-progress.md`: 标记 V2 已开始（或进行中）
- `mcp-server-guide.md`: 增加新输出字段示例

**Step 4: Verify changes**

Run: `rg -n "宅盘|叠加|combined_flying" /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/docs`

Expected: New references in docs.

**Step 5: Commit**

```bash
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 add docs/requirements.md docs/project-progress.md docs/mcp-server-guide.md
git -C /Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2 commit -m "docs: document flying star v2 output"
```

---

### Task 6: 回归测试

**Files:**
- Test: `/Users/apple/dev/CyberYJ/.worktrees/xc-feixing-v2/tests`

**Step 1: Run full test suite**

Run: `pytest -q`

Expected: PASS (195 passed, 2 skipped or updated count if new tests added)

**Step 2: Commit (if any fixes)**

Only if test fixes were needed.

---

**Notes:**
- 数据文件中的规则暂以 `convention` 作为来源标注，后续可替换为权威文本映射。
- 叠加评分阈值可在后续迭代中调整。
- If you need stricter precision, expand `flying_stars_house.json` to cover all 24 山向与全 9 运。
