"""
测试数据加载器模块
"""

import pytest
from pathlib import Path
from cyberYJ.utils.data_loader import DataLoader, get_data_loader


# 测试数据目录
DATA_DIR = Path(__file__).parent.parent / "data"


class TestDataLoader:
    """测试 DataLoader 类"""

    def setup_method(self):
        """每个测试方法前执行"""
        self.loader = DataLoader(DATA_DIR)

    def test_init(self):
        """测试初始化"""
        assert self.loader.data_dir == DATA_DIR
        assert self.loader.data_dir.exists()

    def test_get_trigrams(self):
        """测试获取八卦数据"""
        trigrams = self.loader.get_trigrams()
        assert len(trigrams) == 8
        assert all('id' in t for t in trigrams)
        assert all('name' in t for t in trigrams)
        assert all('element' in t for t in trigrams)

    def test_get_trigram_by_name(self):
        """测试根据名称获取八卦"""
        qian = self.loader.get_trigram_by_name('乾')
        assert qian is not None
        assert qian['name'] == '乾'
        assert qian['element'] == '金'
        assert qian['direction'] == '西北'

        # 测试不存在的卦
        none_trigram = self.loader.get_trigram_by_name('不存在')
        assert none_trigram is None

    def test_get_trigram_by_id(self):
        """测试根据 ID 获取八卦"""
        qian = self.loader.get_trigram_by_id('qian')
        assert qian is not None
        assert qian['id'] == 'qian'
        assert qian['name'] == '乾'

    def test_get_hexagrams(self):
        """测试获取六十四卦数据"""
        hexagrams = self.loader.get_hexagrams()
        assert len(hexagrams) == 64
        assert all('id' in h for h in hexagrams)
        assert all('name' in h for h in hexagrams)
        assert all('upper_trigram' in h for h in hexagrams)
        assert all('lower_trigram' in h for h in hexagrams)

    def test_get_hexagram_by_id(self):
        """测试根据 ID 获取卦"""
        qian = self.loader.get_hexagram_by_id(1)
        assert qian is not None
        assert qian['id'] == 1
        assert qian['name'] == '乾'
        assert qian['upper_trigram'] == '乾'
        assert qian['lower_trigram'] == '乾'

    def test_get_hexagram_by_name(self):
        """测试根据名称获取卦"""
        tai = self.loader.get_hexagram_by_name('泰')
        assert tai is not None
        assert tai['name'] == '泰'
        assert tai['id'] == 11

    def test_get_hexagram_by_trigrams(self):
        """测试根据上下卦获取卦"""
        # 乾卦：乾上乾下
        qian = self.loader.get_hexagram_by_trigrams('乾', '乾')
        assert qian is not None
        assert qian['name'] == '乾'

        # 泰卦：坤上乾下
        tai = self.loader.get_hexagram_by_trigrams('坤', '乾')
        assert tai is not None
        assert tai['name'] == '泰'

    def test_get_solar_terms(self):
        """测试获取节气数据"""
        solar_terms = self.loader.get_solar_terms()
        assert len(solar_terms) == 24
        assert all('name' in t for t in solar_terms)
        assert all('solar_longitude_deg' in t for t in solar_terms)

    def test_get_solar_term_by_longitude(self):
        """测试根据黄经获取节气"""
        # 立春：315度
        lichun = self.loader.get_solar_term_by_longitude(315)
        assert lichun is not None
        assert lichun['name'] == '立春'

        # 春分：0度
        chunfen = self.loader.get_solar_term_by_longitude(0)
        assert chunfen is not None
        assert chunfen['name'] == '春分'

    def test_get_luopan(self):
        """测试获取罗盘数据"""
        luopan = self.loader.get_luopan()
        assert len(luopan) == 24
        assert all('name' in m for m in luopan)
        assert all('start_deg' in m for m in luopan)
        assert all('end_deg' in m for m in luopan)

    def test_get_luopan_by_degree(self):
        """测试根据角度获取山向"""
        # 0度应该是壬山（壬山范围 352.5-7.5度，跨越0度）
        ren = self.loader.get_luopan_by_degree(0)
        assert ren is not None
        assert ren['name'] == '壬'
        assert ren['direction_group'] == '北'

        # 15度应该是子山
        zi = self.loader.get_luopan_by_degree(15)
        assert zi is not None
        assert zi['name'] == '子'
        assert zi['direction_group'] == '北'

    def test_get_luopan_by_name(self):
        """测试根据名称获取山向"""
        zi = self.loader.get_luopan_by_name('子')
        assert zi is not None
        assert zi['name'] == '子'

    def test_get_ba_zhai(self):
        """测试获取八宅规则"""
        ba_zhai = self.loader.get_ba_zhai()
        assert len(ba_zhai) == 8
        assert all('house_gua' in r for r in ba_zhai)
        assert all('auspicious_positions' in r for r in ba_zhai)
        assert all('inauspicious_positions' in r for r in ba_zhai)

    def test_get_ba_zhai_by_gua(self):
        """测试根据宅卦获取规则"""
        qian_zhai = self.loader.get_ba_zhai_by_gua('乾宅')
        assert qian_zhai is not None
        assert qian_zhai['house_gua'] == '乾宅'
        assert len(qian_zhai['auspicious_positions']) == 4
        assert len(qian_zhai['inauspicious_positions']) == 4

    def test_get_flying_stars(self):
        """测试获取飞星数据"""
        flying_stars = self.loader.get_flying_stars()
        assert len(flying_stars) == 7  # 2024-2030
        assert all('year' in s for s in flying_stars)
        assert all('central_star' in s for s in flying_stars)
        assert all('palace_map' in s for s in flying_stars)

    def test_get_flying_stars_by_year(self):
        """测试根据年份获取飞星"""
        stars_2024 = self.loader.get_flying_stars_by_year(2024)
        assert stars_2024 is not None
        assert stars_2024['year'] == 2024
        assert stars_2024['central_star'] == 4

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

    def test_get_sources(self):
        """测试获取来源数据"""
        sources = self.loader.get_sources()
        assert len(sources) >= 8
        assert all('source_id' in s for s in sources)
        assert all('title' in s for s in sources)

    def test_get_source_by_id(self):
        """测试根据 ID 获取来源"""
        ctext = self.loader.get_source_by_id('ctext_yijing')
        assert ctext is not None
        assert ctext['source_id'] == 'ctext_yijing'
        assert '周易' in ctext['title']

    def test_cache(self):
        """测试缓存机制"""
        # 第一次加载
        trigrams1 = self.loader.get_trigrams()
        # 第二次应该从缓存读取
        trigrams2 = self.loader.get_trigrams()
        assert trigrams1 is trigrams2  # 应该是同一个对象

    def test_clear_cache(self):
        """测试清空缓存"""
        self.loader.get_trigrams()
        assert 'trigrams' in self.loader._cache
        self.loader.clear_cache()
        assert 'trigrams' not in self.loader._cache

    def test_reload_all(self):
        """测试重新加载所有数据"""
        self.loader.reload_all()
        assert 'trigrams' in self.loader._cache
        assert 'hexagrams' in self.loader._cache
        assert 'solar_terms' in self.loader._cache
        assert 'luopan' in self.loader._cache
        assert 'ba_zhai' in self.loader._cache
        assert 'flying_stars' in self.loader._cache
        assert 'sources' in self.loader._cache

    def test_get_hexagram_keywords(self):
        """测试获取关键词解析库"""
        keywords_data = self.loader.get_hexagram_keywords()
        assert 'version' in keywords_data
        assert 'keywords' in keywords_data
        assert len(keywords_data['keywords']) > 0

    def test_get_keyword_by_name(self):
        """测试根据名称获取关键词"""
        keyword = self.loader.get_keyword_by_name('利西南')
        assert keyword is not None
        assert 'literal' in keyword
        assert 'symbolic' in keyword
        assert 'general_meaning' in keyword
        assert 'scenario_applications' in keyword

        # 测试不存在的关键词
        none_keyword = self.loader.get_keyword_by_name('不存在的关键词')
        assert none_keyword is None

    def test_get_keyword_application(self):
        """测试获取关键词的场景应用"""
        application = self.loader.get_keyword_application('利西南', '事业')
        assert application is not None
        assert isinstance(application, str)
        assert len(application) > 0

        # 测试不存在的场景
        none_app = self.loader.get_keyword_application('利西南', '不存在的场景')
        assert none_app is None

        # 测试不存在的关键词
        none_app2 = self.loader.get_keyword_application('不存在', '事业')
        assert none_app2 is None

    def test_get_scenario_data(self):
        """测试获取场景数据"""
        fortune_data = self.loader.get_scenario_data('fortune')
        assert fortune_data is not None
        assert 'scenario_info' in fortune_data
        assert 'analysis_framework' in fortune_data
        assert 'hexagrams' in fortune_data

        # 测试不存在的场景
        none_scenario = self.loader.get_scenario_data('nonexistent')
        assert none_scenario is None

    def test_get_scenario_hexagram(self):
        """测试获取特定场景下的卦象数据"""
        hexagram = self.loader.get_scenario_hexagram('fortune', 1)
        assert hexagram is not None
        assert 'name' in hexagram
        assert 'overall_tendency' in hexagram
        assert 'fortune_rating' in hexagram

        # 测试不存在的卦象
        none_hex = self.loader.get_scenario_hexagram('fortune', 999)
        assert none_hex is None

        # 测试不存在的场景
        none_hex2 = self.loader.get_scenario_hexagram('nonexistent', 1)
        assert none_hex2 is None

    def test_get_output_templates(self):
        """测试获取输出模板"""
        templates = self.loader.get_output_templates()
        assert templates is not None
        assert 'templates' in templates
        assert 'rating_display' in templates

    def test_get_template_by_id(self):
        """测试根据ID获取模板"""
        template = self.loader.get_template_by_id('fortune_standard')
        assert template is not None
        assert 'name' in template
        assert 'structure' in template

        # 测试不存在的模板
        none_template = self.loader.get_template_by_id('nonexistent')
        assert none_template is None

    def test_get_disclaimers(self):
        """测试获取免责声明"""
        disclaimers = self.loader.get_disclaimers()
        assert disclaimers is not None
        assert 'disclaimers' in disclaimers
        assert 'scenario_mapping' in disclaimers

    def test_get_disclaimer_by_scenario(self):
        """测试根据场景获取免责声明"""
        disclaimer = self.loader.get_disclaimer_by_scenario('健康')
        assert disclaimer is not None
        assert 'text' in disclaimer
        assert 'level' in disclaimer

        # 测试不存在的场景，应该返回通用免责声明
        general = self.loader.get_disclaimer_by_scenario('不存在的场景')
        assert general is not None
        assert general['scenario'] == '通用'


class TestGlobalLoader:
    """测试全局加载器"""

    def test_get_data_loader(self):
        """测试获取全局加载器"""
        loader1 = get_data_loader(DATA_DIR)
        loader2 = get_data_loader()
        assert loader1 is loader2  # 应该是同一个实例


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
