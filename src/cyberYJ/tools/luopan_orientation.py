"""
罗盘坐向分析工具

实现 luopan_orientation MCP 工具，提供：
- 坐向解析
- 宅卦计算
- 吉凶方位
- 飞星年盘
- 布局建议
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
import pytz

from cyberYJ.core.luopan_calculator import LuopanCalculator
from cyberYJ.core.flying_star_calculator import combine_flying_stars
from cyberYJ.utils.data_loader import get_data_loader
from cyberYJ.utils.authoritative_text_map import match_luopan_item


class LuopanOrientationTool:
    """罗盘坐向分析工具"""

    def __init__(self):
        """初始化工具"""
        self.luopan_calculator = LuopanCalculator()
        self.data_loader = get_data_loader()

    def execute(
        self,
        sitting_direction: str,
        building_type: str,
        owner_birth: Optional[str] = None,
        timestamp: Optional[str] = None,
        timezone: str = "Asia/Shanghai"
    ) -> Dict[str, Any]:
        """
        执行罗盘坐向分析

        Args:
            sitting_direction: 坐向（坐北朝南 / 坐340向160 / 坐亥向巳）
            building_type: 建筑类型（住宅/办公室/商铺/工厂）
            owner_birth: 公历生日（YYYY-MM-DD），可选
            timestamp: RFC3339 时间戳，可选（默认当前时间）
            timezone: IANA 时区名，默认 Asia/Shanghai

        Returns:
            包含罗盘分析结果的字典
        """
        trace = []  # 推导路径记录

        # 1. 解析时间
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    tz = pytz.timezone(timezone)
                    dt = tz.localize(dt)
                trace.append(f"使用指定时间: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            except Exception as e:
                raise ValueError(f"时间戳格式错误: {e}")
        else:
            tz = pytz.timezone(timezone)
            dt = datetime.now(tz)
            trace.append(f"使用当前时间: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # 2. 解析坐向
        try:
            direction_info = self.luopan_calculator.parse_sitting_direction(sitting_direction)
            trace.append(
                f"坐向解析: {sitting_direction} → "
                f"坐{direction_info['sitting_degree']:.1f}°（{direction_info['sitting_mountain']}山）"
            )
        except Exception as e:
            raise ValueError(f"坐向解析失败: {e}")

        # 3. 计算宅卦
        house_gua = self.luopan_calculator.calculate_house_gua(
            direction_info['sitting_degree']
        )
        trace.append(f"宅卦: {house_gua}")

        # 4. 获取吉凶方位
        positions = self.luopan_calculator.get_auspicious_positions(house_gua)
        trace.append(f"八宅吉位: {len(positions['auspicious'])} 个")
        trace.append(f"八宅凶位: {len(positions['inauspicious'])} 个")
        if positions.get("source_ref"):
            trace.append(f"八宅规则来源: {positions['source_ref']}")

        # 5. 命卦匹配（如果提供了生日）
        ming_gua_info = None
        if owner_birth:
            try:
                birth_date = datetime.strptime(owner_birth, '%Y-%m-%d')
                # 默认假设为男性，实际应用中可以添加性别参数
                ming_gua_result = self.luopan_calculator.calculate_ming_gua(birth_date, 'male')
                compatibility = self.luopan_calculator.check_house_compatibility(
                    house_gua,
                    ming_gua_result
                )

                ming_gua_info = {
                    "ming_gua": ming_gua_result.get('gua_name', ''),
                    "category": ming_gua_result.get('category', ''),
                    "compatible": compatibility.get('compatible', False),
                    "advice": compatibility.get('advice', '')
                }
                trace.append(
                    f"命卦: {ming_gua_info['ming_gua']}（{ming_gua_info['category']}）"
                )
                trace.append(f"宅命匹配: {'相配' if ming_gua_info['compatible'] else '不相配'}")
            except Exception as e:
                trace.append(f"命卦计算失败: {str(e)}")

        # 6. 获取流年飞星
        year = dt.year
        flying_stars = self.data_loader.get_flying_stars_by_year(year)
        if flying_stars:
            if flying_stars.get("computed"):
                trace.append(
                    f"流年飞星: {year}年 中宫{flying_stars['central_star']}星（按{flying_stars.get('base_year')}年规则推算）"
                )
            else:
                trace.append(f"流年飞星: {year}年 中宫{flying_stars['central_star']}星")
            if flying_stars.get("source_ref"):
                trace.append(f"飞星规则来源: {flying_stars['source_ref']}")
        else:
            trace.append(f"流年飞星: {year}年数据暂无")

        # 6.1 宅盘 + 流年叠加
        period_info = self.data_loader.get_flying_star_period_by_year(year)
        house_rule = None
        if period_info:
            house_rule = self.data_loader.get_flying_star_house_rule(
                period=period_info['period'],
                sitting_mountain=direction_info['sitting_mountain']
            )

        combined = None
        current_auspicious: List[str] = []
        current_inauspicious: List[str] = []

        scoring = self.data_loader.get_flying_star_scoring()
        thresholds = scoring.get("thresholds", {})
        fallback_cfg = scoring.get("fallback", {})
        missing_annual_star_strategy = fallback_cfg.get("missing_annual_star", "skip")
        if scoring.get("stars"):
            trace.append(
                f"飞星评分阈值: 吉>={thresholds.get('auspicious', 2)} "
                f"凶<={thresholds.get('inauspicious', -2)}"
            )
            trace.append(f"缺失年星策略: {missing_annual_star_strategy}")
        else:
            trace.append("飞星评分规则缺失: 使用默认中性评分（0）")

        if not period_info:
            trace.append(f"元运信息缺失: {year}年未匹配元运，降级为仅流年年盘")
        elif not house_rule:
            trace.append(
                f"宅盘规则缺失: 第{period_info['period']}运 "
                f"{direction_info['sitting_mountain']}山，降级为仅流年年盘"
            )
        elif not flying_stars:
            trace.append(f"流年飞星缺失: {year}年无年盘，降级为仅宅盘")
        else:
            combined, current_auspicious, current_inauspicious = combine_flying_stars(
                house_rule['palace_map'],
                flying_stars['palace_map'],
                scoring
            )
            trace.append(
                f"元运: 第{period_info['period']}运（{period_info['start_year']}-{period_info['end_year']}）"
            )
            trace.append(f"宅盘命中: {direction_info['sitting_mountain']}山")
            trace.append("飞星叠加: 宅盘 + 流年")

        # 7. 生成布局建议
        layout_tips = self._generate_layout_tips(
            house_gua,
            positions,
            building_type,
            ming_gua_info,
            flying_stars
        )

        # 8. 构建输出
        result = {
            "direction_class": f"{direction_info['sitting_mountain']}山 "
                             f"({direction_info['sitting_direction_group']}方)",
            "house_gua": house_gua,
            "sitting_degree": direction_info['sitting_degree'],
            "facing_degree": direction_info['facing_degree'],
            "auspicious_positions": positions['auspicious'],
            "inauspicious_positions": positions['inauspicious'],
            "layout_tips": layout_tips,
            "trace": trace
        }

        # 添加命卦匹配信息
        if ming_gua_info:
            result["ming_gua_match"] = (
                f"{ming_gua_info['ming_gua']}（{ming_gua_info['category']}）- "
                f"{'相配' if ming_gua_info['compatible'] else '不相配'}"
            )
            result["compatibility_advice"] = ming_gua_info['advice']

        # 添加流年飞星
        if flying_stars:
            result["annual_flying_stars"] = {
                "year": flying_stars['year'],
                "central_star": flying_stars['central_star'],
                "palace_map": flying_stars['palace_map']
            }

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

        # 权威映射替换（如有）
        mapped_sources = self._apply_authoritative_mappings(result, trace)

        # 添加来源信息
        result["sources"] = self._get_sources(extra_source_ids=mapped_sources)

        return result

    def _generate_layout_tips(
        self,
        house_gua: str,
        positions: Dict[str, List[str]],
        building_type: str,
        ming_gua_info: Optional[Dict[str, Any]],
        flying_stars: Optional[Dict[str, Any]]
    ) -> List[str]:
        """
        生成布局建议

        Args:
            house_gua: 宅卦
            positions: 吉凶方位
            building_type: 建筑类型
            ming_gua_info: 命卦信息
            flying_stars: 飞星信息

        Returns:
            布局建议列表
        """
        tips = []

        # 1. 根据建筑类型给出基础建议
        building_advice = {
            '住宅': [
                '主卧宜设在生气位或延年位，有利健康和夫妻关系',
                '书房宜设在文昌位（天医位），有利学业和事业',
                '厨房和卫生间宜设在凶位，以凶制凶'
            ],
            '办公室': [
                '办公桌宜设在生气位或延年位，有利事业发展',
                '会议室宜设在天医位，有利决策和合作',
                '财务室宜设在延年位，有利财运'
            ],
            '商铺': [
                '收银台宜设在延年位或生气位，有利财运',
                '入口宜朝向吉位，吸引客流',
                '仓库宜设在伏位，稳定库存'
            ],
            '工厂': [
                '办公区宜设在生气位，有利管理',
                '生产区宜设在延年位，有利效率',
                '仓储区宜设在伏位，稳定安全'
            ]
        }

        if building_type in building_advice:
            tips.extend(building_advice[building_type])

        # 2. 根据吉凶方位给出具体建议
        if positions['auspicious']:
            auspicious_str = '、'.join(positions['auspicious'][:2])
            tips.append(f'重要功能区（卧室、办公室、客厅）宜设在吉位：{auspicious_str}')

        if positions['inauspicious']:
            inauspicious_str = '、'.join(positions['inauspicious'][:2])
            tips.append(f'次要功能区（厨房、卫生间、储藏室）宜设在凶位：{inauspicious_str}')

        # 3. 命卦匹配建议
        if ming_gua_info and not ming_gua_info['compatible']:
            tips.append(
                f'宅命不相配，建议：{ming_gua_info["advice"]}'
            )

        # 4. 流年飞星建议
        if flying_stars:
            year = flying_stars['year']
            central_star = flying_stars['central_star']

            # 根据中宫星给出流年建议
            star_advice = {
                1: f'{year}年中宫一白星，利文昌和人际，宜多交流学习',
                4: f'{year}年中宫四绿星，利文昌和感情，宜发展事业和关系',
                6: f'{year}年中宫六白星，利官运和权威，宜把握机遇',
                8: f'{year}年中宫八白星，大利财运，宜投资和发展',
                9: f'{year}年中宫九紫星，利喜庆和名声，宜扩大影响力'
            }

            if central_star in star_advice:
                tips.append(star_advice[central_star])

        # 5. 通用建议
        tips.append('保持室内整洁明亮，有利气场流通')
        tips.append('避免横梁压顶、尖角冲射等不利格局')

        return tips[:8]  # 最多返回8条建议

    def _get_sources(self, extra_source_ids: Optional[List[str]] = None) -> List[str]:
        """
        获取数据来源信息

        Returns:
            来源列表
        """
        sources = []
        extra_source_ids = extra_source_ids or []

        # 获取主要来源
        qingnang = self.data_loader.get_source_by_id('qingnang_aoyu')
        if qingnang:
            sources.append(f"罗盘山向: {qingnang['title']}")

        bazhai = self.data_loader.get_source_by_id('cinii_bazhai_mingjing')
        if bazhai:
            sources.append(f"八宅规则: {bazhai['title']}")

        dili = self.data_loader.get_source_by_id('cinii_dili_bianzheng_shu')
        if dili:
            sources.append(f"玄空飞星: {dili['title']}")

        # 追加映射来源
        for sid in extra_source_ids:
            if sid in ("qingnang_aoyu", "cinii_bazhai_mingjing", "cinii_dili_bianzheng_shu"):
                continue
            src = self.data_loader.get_source_by_id(sid)
            if src:
                label = src.get("title", sid)
                sources.append(f"权威映射: {label}")

        return sources

    def _apply_authoritative_mappings(
        self,
        result: Dict[str, Any],
        trace: List[str]
    ) -> List[str]:
        mapping = self.data_loader.get_authoritative_text_map()
        items = mapping.get("items", [])
        if not items:
            return []

        applied_sources: List[str] = []

        for item in items:
            match = match_luopan_item(item)
            if not match:
                continue

            text_kind = item.get("text_kind")
            content = item.get("content")
            source_ref = item.get("source_ref", [])

            if text_kind == "citation_only":
                trace.append(f"权威映射: {match['field_path']} (citation_only)")
            elif content:
                # 作为布局建议补充（不替换核心计算结果）
                result.setdefault("layout_tips", [])
                result["layout_tips"].insert(0, f"权威补充: {content}")
                trace.append(f"权威补充: {match['field_path']}")

            for sid in source_ref:
                if sid not in applied_sources:
                    applied_sources.append(sid)

            if "convention" in source_ref:
                trace.append("注记: 权威映射仍含 convention 归纳规则")

        return applied_sources


def create_tool() -> LuopanOrientationTool:
    """创建罗盘坐向分析工具实例"""
    return LuopanOrientationTool()
