"""
数据加载器模块

提供统一的数据访问接口，支持数据缓存和懒加载。
加载所有 JSON 数据文件：trigrams, hexagrams, solar_terms, luopan, ba_zhai, flying_stars, sources
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from functools import lru_cache


class DataLoader:
    """数据加载器，负责加载和缓存所有 JSON 数据文件"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化数据加载器

        Args:
            data_dir: 数据目录路径，默认为项目根目录下的 data 文件夹
        """
        if data_dir is None:
            # 默认数据目录：项目根目录/data
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent.parent
            data_dir = project_root / "data"

        self.data_dir = Path(data_dir)

        if not self.data_dir.exists():
            raise FileNotFoundError(f"数据目录不存在: {self.data_dir}")

        # 数据缓存
        self._cache: Dict[str, Any] = {}

    def _load_json(self, filename: str, subdir: Optional[str] = None) -> Any:
        """
        加载 JSON 文件

        Args:
            filename: JSON 文件名（不含路径）
            subdir: 子目录名称（如 'core', 'scenarios', 'fengshui'），可选

        Returns:
            解析后的 JSON 数据

        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON 格式错误
        """
        if subdir:
            file_path = self.data_dir / subdir / filename
        else:
            file_path = self.data_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"数据文件不存在: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"JSON 格式错误 ({filename}): {e.msg}",
                e.doc,
                e.pos
            )

    def get_trigrams(self) -> List[Dict[str, Any]]:
        """
        获取八卦数据

        Returns:
            八卦列表，每个元素包含: id, name, symbol, element, direction, source_ref
        """
        if 'trigrams' not in self._cache:
            self._cache['trigrams'] = self._load_json('trigrams.json', 'core')
        return self._cache['trigrams']

    def get_trigram_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据卦名获取八卦数据

        Args:
            name: 卦名（如"乾"、"坤"）

        Returns:
            八卦数据字典，未找到返回 None
        """
        name_variants = self._trigram_name_variants(name)
        trigrams = self.get_trigrams()
        for trigram in trigrams:
            if trigram['name'] in name_variants:
                return trigram
        return None

    def get_trigram_by_id(self, trigram_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取八卦数据

        Args:
            trigram_id: 八卦 ID（如"qian"、"kun"）

        Returns:
            八卦数据字典，未找到返回 None
        """
        trigrams = self.get_trigrams()
        for trigram in trigrams:
            if trigram['id'] == trigram_id:
                return trigram
        return None

    def get_hexagrams(self) -> List[Dict[str, Any]]:
        """
        获取六十四卦数据

        Returns:
            六十四卦列表，每个元素包含: id, name, upper_trigram, lower_trigram,
            judgment_summary, image_summary, element_relation, source_ref
        """
        if 'hexagrams' not in self._cache:
            self._cache['hexagrams'] = self._load_json('hexagrams.json', 'core')
        return self._cache['hexagrams']

    def get_hexagram_by_id(self, hexagram_id: int) -> Optional[Dict[str, Any]]:
        """
        根据卦序号获取六十四卦数据

        Args:
            hexagram_id: 卦序号（1-64）

        Returns:
            卦数据字典，未找到返回 None
        """
        hexagrams = self.get_hexagrams()
        for hexagram in hexagrams:
            if hexagram['id'] == hexagram_id:
                return hexagram
        return None

    def get_hexagram_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据卦名获取六十四卦数据

        Args:
            name: 卦名（如"乾"、"坤"）

        Returns:
            卦数据字典，未找到返回 None
        """
        hexagrams = self.get_hexagrams()
        for hexagram in hexagrams:
            if hexagram['name'] == name:
                return hexagram
        return None

    def get_hexagram_by_trigrams(
        self,
        upper_trigram: str,
        lower_trigram: str
    ) -> Optional[Dict[str, Any]]:
        """
        根据上下卦获取六十四卦数据

        Args:
            upper_trigram: 上卦名称（如"乾"）
            lower_trigram: 下卦名称（如"坤"）

        Returns:
            卦数据字典，未找到返回 None
        """
        upper_variants = self._trigram_name_variants(upper_trigram)
        lower_variants = self._trigram_name_variants(lower_trigram)
        hexagrams = self.get_hexagrams()
        for hexagram in hexagrams:
            if (hexagram['upper_trigram'] in upper_variants and
                hexagram['lower_trigram'] in lower_variants):
                return hexagram
        return None

    @staticmethod
    def _trigram_name_variants(name: str) -> set[str]:
        """返回八卦名的繁简体变体集合。"""
        variant_map = {
            "兑": {"兑", "兌"},
            "兌": {"兑", "兌"},
            "离": {"离", "離"},
            "離": {"离", "離"},
        }
        return variant_map.get(name, {name})

    def get_solar_terms(self) -> List[Dict[str, Any]]:
        """
        获取二十四节气数据

        Returns:
            节气列表，每个元素包含: id, name, solar_longitude_deg, source_ref
        """
        if 'solar_terms' not in self._cache:
            self._cache['solar_terms'] = self._load_json('solar_terms.json', 'core')
        return self._cache['solar_terms']

    def get_solar_term_by_longitude(
        self,
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        根据太阳黄经获取对应的节气

        Args:
            longitude: 太阳黄经（0-360度）

        Returns:
            节气数据字典，未找到返回 None
        """
        solar_terms = self.get_solar_terms()

        # 标准化黄经到 0-360 范围
        longitude = longitude % 360

        # 找到最接近的节气
        min_diff = 360
        closest_term = None

        for term in solar_terms:
            term_long = term['solar_longitude_deg']
            # 计算角度差（考虑循环）
            diff = abs(term_long - longitude)
            if diff > 180:
                diff = 360 - diff

            if diff < min_diff:
                min_diff = diff
                closest_term = term

        return closest_term

    def get_luopan(self) -> List[Dict[str, Any]]:
        """
        获取二十四山向数据

        Returns:
            山向列表，每个元素包含: id, name, start_deg, end_deg, direction_group, source_ref
        """
        if 'luopan' not in self._cache:
            self._cache['luopan'] = self._load_json('luopan.json', 'fengshui')
        return self._cache['luopan']

    def get_luopan_by_degree(self, degree: float) -> Optional[Dict[str, Any]]:
        """
        根据角度获取对应的山向

        Args:
            degree: 角度（0-360度，0度=正北）

        Returns:
            山向数据字典，未找到返回 None
        """
        luopan = self.get_luopan()

        # 标准化角度到 0-360 范围
        degree = degree % 360

        for mountain in luopan:
            start = mountain['start_deg']
            end = mountain['end_deg']

            # 处理跨越 0 度的情况（如 352.5-7.5）
            if start > end:
                if degree >= start or degree <= end:
                    return mountain
            else:
                if start <= degree <= end:
                    return mountain

        return None

    def get_luopan_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据山向名称获取数据

        Args:
            name: 山向名称（如"子"、"午"）

        Returns:
            山向数据字典，未找到返回 None
        """
        luopan = self.get_luopan()
        for mountain in luopan:
            if mountain['name'] == name:
                return mountain
        return None

    def get_ba_zhai(self) -> List[Dict[str, Any]]:
        """
        获取八宅规则数据

        Returns:
            八宅规则列表，每个元素包含: house_gua, auspicious_positions,
            inauspicious_positions, source_ref
        """
        if 'ba_zhai' not in self._cache:
            self._cache['ba_zhai'] = self._load_json('ba_zhai.json', 'fengshui')
        return self._cache['ba_zhai']

    def get_ba_zhai_by_gua(self, house_gua: str) -> Optional[Dict[str, Any]]:
        """
        根据宅卦获取八宅规则

        Args:
            house_gua: 宅卦名称（如"乾宅"、"坤宅"）

        Returns:
            八宅规则数据字典，未找到返回 None
        """
        ba_zhai = self.get_ba_zhai()
        for rule in ba_zhai:
            if rule['house_gua'] == house_gua:
                return rule
        return None

    def get_flying_stars(self) -> List[Dict[str, Any]]:
        """
        获取玄空飞星年盘数据

        Returns:
            飞星年盘列表，每个元素包含: year, central_star, palace_map, source_ref
        """
        if 'flying_stars' not in self._cache:
            self._cache['flying_stars'] = self._load_json('flying_stars.json', 'fengshui')
        return self._cache['flying_stars']

    def get_flying_stars_by_year(self, year: int) -> Optional[Dict[str, Any]]:
        """
        根据年份获取飞星年盘

        Args:
            year: 年份（如 2024）

        Returns:
            飞星年盘数据字典，未找到返回 None
        """
        flying_stars = self.get_flying_stars()
        for star_map in flying_stars:
            if star_map['year'] == year:
                return star_map
        return self._compute_flying_stars_by_year(year)

    def _compute_flying_stars_by_year(self, year: int) -> Optional[Dict[str, Any]]:
        """
        使用规则推算飞星年盘（基于最早年份的基准盘逐年递减）
        """
        flying_stars = self.get_flying_stars()
        if not flying_stars:
            return None

        base = min(flying_stars, key=lambda x: x['year'])
        base_year = base['year']
        delta = year - base_year

        def shift_star(star: int, delta_years: int) -> int:
            return ((star - 1 - delta_years) % 9) + 1

        base_map = base['palace_map']
        computed_map = {
            palace: shift_star(star, delta)
            for palace, star in base_map.items()
        }

        return {
            "year": year,
            "central_star": shift_star(base['central_star'], delta),
            "palace_map": computed_map,
            "source_ref": base.get("source_ref", "cinii_dili_bianzheng_shu"),
            "computed": True,
            "base_year": base_year
        }

    def get_flying_star_periods(self) -> List[Dict[str, Any]]:
        """
        获取玄空元运周期数据

        Returns:
            元运列表，每个元素包含: period, start_year, end_year, source_ref
        """
        if 'flying_star_periods' not in self._cache:
            self._cache['flying_star_periods'] = self._load_json(
                'flying_stars_periods.json',
                'fengshui'
            )
        return self._cache['flying_star_periods']

    def get_flying_star_period_by_year(self, year: int) -> Optional[Dict[str, Any]]:
        """
        根据年份获取元运信息

        Args:
            year: 年份

        Returns:
            元运数据字典，未找到返回 None
        """
        for period in self.get_flying_star_periods():
            if period['start_year'] <= year <= period['end_year']:
                return period
        return None

    def get_flying_star_house_rules(self) -> List[Dict[str, Any]]:
        """
        获取玄空飞星宅盘规则表

        Returns:
            宅盘规则列表
        """
        if 'flying_star_house' not in self._cache:
            self._cache['flying_star_house'] = self._load_json(
                'flying_stars_house.json',
                'fengshui'
            )
        return self._cache['flying_star_house']

    def get_flying_star_house_rule(
        self,
        period: int,
        sitting_mountain: str
    ) -> Optional[Dict[str, Any]]:
        """
        根据元运与坐山获取宅盘规则
        """
        for rule in self.get_flying_star_house_rules():
            if rule['period'] == period and rule['sitting_mountain'] == sitting_mountain:
                return rule
        return None

    def get_flying_star_scoring(self) -> Dict[str, Any]:
        """
        获取飞星评分规则
        """
        if 'flying_star_scoring' not in self._cache:
            self._cache['flying_star_scoring'] = self._load_json(
                'flying_stars_scoring.json',
                'fengshui'
            )
        return self._cache['flying_star_scoring']

    def validate_flying_star_house_rules(self) -> Dict[str, Any]:
        """
        校验宅盘规则表覆盖情况与数据结构完整性

        Returns:
            校验报告：
            - is_valid: 是否通过校验
            - rule_count: 实际规则条目数
            - expected_count: 期望条目数（24 山向 x 9 运）
            - missing_pairs: 缺失的 (period, mountain) 组合
            - duplicate_pairs: 重复的 (period, mountain) 组合
            - invalid_palace_entries: 九宫结构异常的规则键
        """
        periods = [p["period"] for p in self.get_flying_star_periods()]
        mountains = [m["name"] for m in self.get_luopan()]
        rules = self.get_flying_star_house_rules()

        expected_pairs = {(period, mountain) for period in periods for mountain in mountains}
        seen_pairs = set()
        duplicate_pairs = []
        invalid_palace_entries = []
        expected_palaces = {"中宫", "坎", "坤", "震", "巽", "乾", "兑", "艮", "离"}

        for rule in rules:
            pair = (rule.get("period"), rule.get("sitting_mountain"))
            if pair in seen_pairs:
                duplicate_pairs.append(pair)
            else:
                seen_pairs.add(pair)

            palace_map = rule.get("palace_map", {})
            palace_keys = set(palace_map.keys())
            if palace_keys != expected_palaces:
                invalid_palace_entries.append(pair)
                continue

            for palace, stars in palace_map.items():
                m_star = stars.get("mountain_star")
                f_star = stars.get("facing_star")
                if (
                    not isinstance(m_star, int) or
                    not isinstance(f_star, int) or
                    m_star < 1 or m_star > 9 or
                    f_star < 1 or f_star > 9
                ):
                    invalid_palace_entries.append((pair[0], f"{pair[1]}:{palace}"))
                    break

        missing_pairs = sorted(expected_pairs - seen_pairs)
        report = {
            "is_valid": not (missing_pairs or duplicate_pairs or invalid_palace_entries),
            "rule_count": len(rules),
            "expected_count": len(expected_pairs),
            "missing_pairs": missing_pairs,
            "duplicate_pairs": duplicate_pairs,
            "invalid_palace_entries": invalid_palace_entries,
        }
        return report

    def get_sources(self) -> List[Dict[str, Any]]:
        """
        获取数据来源索引

        Returns:
            来源列表，每个元素包含: source_id, title, edition, section,
            url_or_archive, license, notes
        """
        if 'sources' not in self._cache:
            self._cache['sources'] = self._load_json('sources.json', 'core')
        return self._cache['sources']

    def get_authoritative_text_map(self) -> Dict[str, Any]:
        """
        获取权威文本替换映射表
        """
        if 'authoritative_text_map' not in self._cache:
            self._cache['authoritative_text_map'] = self._load_json(
                'authoritative_text_map.json',
                'mappings'
            )
        return self._cache['authoritative_text_map']

    def get_source_by_id(self, source_id: str) -> Optional[Dict[str, Any]]:
        """
        根据来源 ID 获取来源信息

        Args:
            source_id: 来源 ID（如"ctext_yijing"）

        Returns:
            来源信息字典，未找到返回 None
        """
        sources = self.get_sources()
        for source in sources:
            if source['source_id'] == source_id:
                return source
        return None

    def get_hexagram_keywords(self) -> Dict[str, Any]:
        """
        获取卦辞关键词解析库

        Returns:
            关键词解析字典，包含 version, description, keywords, notes
        """
        if 'hexagram_keywords' not in self._cache:
            self._cache['hexagram_keywords'] = self._load_json('hexagram_keywords.json', 'core')
        return self._cache['hexagram_keywords']

    def get_keyword_by_name(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        根据关键词名称获取解析

        Args:
            keyword: 关键词（如"利西南"、"利见大人"）

        Returns:
            关键词解析字典，未找到返回 None
        """
        keywords_data = self.get_hexagram_keywords()
        keywords = keywords_data.get('keywords', {})
        return keywords.get(keyword)

    def get_keyword_application(self, keyword: str, scenario: str) -> Optional[str]:
        """
        获取关键词在特定场景下的应用

        Args:
            keyword: 关键词（如"利西南"）
            scenario: 场景（如"事业"、"感情"、"财运"）

        Returns:
            场景应用说明，未找到返回 None
        """
        keyword_data = self.get_keyword_by_name(keyword)
        if keyword_data:
            applications = keyword_data.get('scenario_applications', {})
            return applications.get(scenario)
        return None

    def get_scenario_data(self, scenario_code: str) -> Optional[Dict[str, Any]]:
        """
        获取场景数据

        Args:
            scenario_code: 场景代码（如"fortune"、"career"、"love"）

        Returns:
            场景数据字典，未找到返回 None
        """
        cache_key = f'scenario_{scenario_code}'
        if cache_key not in self._cache:
            try:
                self._cache[cache_key] = self._load_json(f'{scenario_code}.json', 'scenarios')
            except FileNotFoundError:
                return None
        return self._cache[cache_key]

    def get_scenario_hexagram(self, scenario_code: str, hexagram_id: int) -> Optional[Dict[str, Any]]:
        """
        获取特定场景下的卦象数据

        Args:
            scenario_code: 场景代码（如"fortune"、"career"、"love"）
            hexagram_id: 卦象ID（1-64）

        Returns:
            卦象在该场景下的数据，未找到返回 None
        """
        scenario_data = self.get_scenario_data(scenario_code)
        if scenario_data:
            hexagrams = scenario_data.get('hexagrams', {})
            return hexagrams.get(str(hexagram_id))
        return None

    def get_output_templates(self) -> Dict[str, Any]:
        """
        获取输出模板数据

        Returns:
            输出模板字典，包含 version, templates, rating_display
        """
        if 'output_templates' not in self._cache:
            self._cache['output_templates'] = self._load_json('output_structures.json', 'templates')
        return self._cache['output_templates']

    def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        根据模板ID获取输出模板

        Args:
            template_id: 模板ID（如"fortune_standard"、"career_standard"）

        Returns:
            模板数据字典，未找到返回 None
        """
        templates_data = self.get_output_templates()
        templates = templates_data.get('templates', {})
        return templates.get(template_id)

    def get_disclaimers(self) -> Dict[str, Any]:
        """
        获取免责声明数据

        Returns:
            免责声明字典，包含 version, disclaimers, scenario_mapping
        """
        if 'disclaimers' not in self._cache:
            self._cache['disclaimers'] = self._load_json('disclaimers.json', 'templates')
        return self._cache['disclaimers']

    def get_disclaimer_by_scenario(self, scenario: str) -> Optional[Dict[str, Any]]:
        """
        根据场景获取免责声明

        Args:
            scenario: 场景名称（如"健康"、"财运"、"诉讼"）

        Returns:
            免责声明数据字典，未找到返回通用免责声明
        """
        disclaimers_data = self.get_disclaimers()
        scenario_mapping = disclaimers_data.get('scenario_mapping', {})
        disclaimers = disclaimers_data.get('disclaimers', {})

        # 获取场景对应的免责声明类型
        disclaimer_type = scenario_mapping.get(scenario, 'general')
        return disclaimers.get(disclaimer_type)

    def clear_cache(self):
        """清空数据缓存"""
        self._cache.clear()

    def reload_all(self):
        """重新加载所有数据"""
        self.clear_cache()
        # 预加载所有数据
        self.get_trigrams()
        self.get_hexagrams()
        self.get_solar_terms()
        self.get_luopan()
        self.get_ba_zhai()
        self.get_flying_stars()
        self.get_flying_star_periods()
        self.get_flying_star_house_rules()
        self.get_flying_star_scoring()
        self.get_sources()


# 全局单例实例
_global_loader: Optional[DataLoader] = None


def get_data_loader(data_dir: Optional[Path] = None) -> DataLoader:
    """
    获取全局数据加载器实例（单例模式）

    Args:
        data_dir: 数据目录路径，仅在首次调用时有效

    Returns:
        DataLoader 实例
    """
    global _global_loader
    if _global_loader is None:
        _global_loader = DataLoader(data_dir)
    return _global_loader
