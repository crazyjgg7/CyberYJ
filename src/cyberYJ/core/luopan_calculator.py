"""
罗盘坐向解析模块

提供坐向解析、宅卦计算和吉凶方位查询功能。
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..utils.data_loader import get_data_loader, DataLoader


class LuopanCalculator:
    """罗盘计算器，负责坐向解析、宅卦计算和吉凶方位查询"""

    # 方位映射（中文方位到角度）
    DIRECTION_MAP = {
        '北': 0,
        '东北': 45,
        '东': 90,
        '东南': 135,
        '南': 180,
        '西南': 225,
        '西': 270,
        '西北': 315,
    }

    # 八卦与方位组的映射
    GUA_DIRECTION_MAP = {
        '乾': '西北',
        '坤': '西南',
        '震': '东',
        '巽': '东南',
        '坎': '北',
        '离': '南',
        '艮': '东北',
        '兑': '西',
    }

    # 山向到八卦的映射（用于宅卦计算）
    MOUNTAIN_TO_GUA = {
        '戌': '乾', '乾': '乾', '亥': '乾',
        '未': '坤', '坤': '坤', '申': '坤',
        '甲': '震', '卯': '震', '乙': '震',
        '辰': '巽', '巽': '巽', '巳': '巽',
        '壬': '坎', '子': '坎', '癸': '坎',
        '丙': '离', '午': '离', '丁': '离',
        '丑': '艮', '艮': '艮', '寅': '艮',
        '庚': '兑', '酉': '兑', '辛': '兑',
    }

    def __init__(self, data_loader: Optional[DataLoader] = None):
        """
        初始化罗盘计算器

        Args:
            data_loader: 数据加载器实例，默认使用全局单例
        """
        self.data_loader = data_loader or get_data_loader()

    def parse_sitting_direction(self, direction_str: str) -> Dict[str, Any]:
        """
        解析坐向输入，支持多种格式

        支持的格式：
        - 中文描述："坐北朝南"、"坐西北向东南"
        - 角度格式："坐340向160"、"坐340度"
        - 干支格式："坐亥向巳"、"坐壬向丙"

        Args:
            direction_str: 坐向描述字符串

        Returns:
            包含以下字段的字典：
            - sitting_degree: 坐向角度（0-360）
            - facing_degree: 朝向角度（0-360）
            - sitting_mountain: 坐山名称
            - facing_mountain: 向山名称
            - sitting_direction_group: 坐向方位组（如"北"、"西北"）
            - facing_direction_group: 朝向方位组

        Raises:
            ValueError: 无法解析的坐向格式
        """
        direction_str = direction_str.strip()

        # 尝试解析中文方位描述（坐北朝南）
        match = re.match(r'坐([东西南北]+)(?:朝|向)([东西南北]+)', direction_str)
        if match:
            sitting_dir = match.group(1)
            facing_dir = match.group(2)

            if sitting_dir in self.DIRECTION_MAP and facing_dir in self.DIRECTION_MAP:
                sitting_degree = self.DIRECTION_MAP[sitting_dir]
                facing_degree = self.DIRECTION_MAP[facing_dir]

                return self._build_direction_result(sitting_degree, facing_degree)

        # 尝试解析角度格式（坐340向160 或 坐340度）
        match = re.match(r'坐(\d+(?:\.\d+)?)(?:度|向(\d+(?:\.\d+)?))?', direction_str)
        if match:
            sitting_degree = float(match.group(1))
            if match.group(2):
                facing_degree = float(match.group(2))
            else:
                # 只有坐向，计算朝向（相差180度）
                facing_degree = (sitting_degree + 180) % 360

            return self._build_direction_result(sitting_degree, facing_degree)

        # 尝试解析干支格式（坐亥向巳）
        match = re.match(r'坐([^向]+)(?:向(.+))?', direction_str)
        if match:
            sitting_mountain_name = match.group(1)
            facing_mountain_name = match.group(2) if match.group(2) else None

            # 查找坐山
            sitting_mountain = self.data_loader.get_luopan_by_name(sitting_mountain_name)
            if sitting_mountain:
                # 使用山向的中心角度
                sitting_degree = (sitting_mountain['start_deg'] + sitting_mountain['end_deg']) / 2
                # 处理跨越0度的情况
                if sitting_mountain['start_deg'] > sitting_mountain['end_deg']:
                    sitting_degree = (sitting_mountain['start_deg'] + sitting_mountain['end_deg'] + 360) / 2
                    sitting_degree = sitting_degree % 360

                # 如果指定了向山，使用向山的中心角度
                if facing_mountain_name:
                    facing_mountain = self.data_loader.get_luopan_by_name(facing_mountain_name)
                    if facing_mountain:
                        facing_degree = (facing_mountain['start_deg'] + facing_mountain['end_deg']) / 2
                        if facing_mountain['start_deg'] > facing_mountain['end_deg']:
                            facing_degree = (facing_mountain['start_deg'] + facing_mountain['end_deg'] + 360) / 2
                            facing_degree = facing_degree % 360
                    else:
                        facing_degree = (sitting_degree + 180) % 360
                else:
                    facing_degree = (sitting_degree + 180) % 360

                return self._build_direction_result(sitting_degree, facing_degree)

        raise ValueError(f"无法解析的坐向格式: {direction_str}")

    def _build_direction_result(
        self,
        sitting_degree: float,
        facing_degree: float
    ) -> Dict[str, Any]:
        """
        构建坐向解析结果

        Args:
            sitting_degree: 坐向角度
            facing_degree: 朝向角度

        Returns:
            坐向信息字典
        """
        # 标准化角度到 0-360 范围
        sitting_degree = sitting_degree % 360
        facing_degree = facing_degree % 360

        # 获取山向信息
        sitting_mountain = self.get_mountain_by_degree(sitting_degree)
        facing_mountain = self.get_mountain_by_degree(facing_degree)

        return {
            'sitting_degree': sitting_degree,
            'facing_degree': facing_degree,
            'sitting_mountain': sitting_mountain['name'] if sitting_mountain else None,
            'facing_mountain': facing_mountain['name'] if facing_mountain else None,
            'sitting_direction_group': sitting_mountain['direction_group'] if sitting_mountain else None,
            'facing_direction_group': facing_mountain['direction_group'] if facing_mountain else None,
        }

    def get_mountain_by_degree(self, degree: float) -> Optional[Dict[str, Any]]:
        """
        根据角度获取山向信息

        Args:
            degree: 角度（0-360度，0度=正北）

        Returns:
            山向数据字典，包含 id, name, start_deg, end_deg, direction_group
            未找到返回 None
        """
        return self.data_loader.get_luopan_by_degree(degree)

    def calculate_house_gua(self, sitting_degree: float) -> str:
        """
        根据坐向角度计算宅卦

        Args:
            sitting_degree: 坐向角度（0-360度）

        Returns:
            宅卦名称（如"乾宅"、"坤宅"）

        Raises:
            ValueError: 无法确定宅卦
        """
        # 获取坐山
        sitting_mountain = self.get_mountain_by_degree(sitting_degree)
        if not sitting_mountain:
            raise ValueError(f"无法找到角度 {sitting_degree} 对应的山向")

        mountain_name = sitting_mountain['name']

        # 根据山向确定八卦
        if mountain_name not in self.MOUNTAIN_TO_GUA:
            raise ValueError(f"未知的山向: {mountain_name}")

        gua_name = self.MOUNTAIN_TO_GUA[mountain_name]
        return f"{gua_name}宅"

    def get_auspicious_positions(self, house_gua: str) -> Dict[str, List[str]]:
        """
        获取指定宅卦的吉凶方位

        Args:
            house_gua: 宅卦名称（如"乾宅"、"坤宅"）

        Returns:
            包含吉位和凶位的字典：
            - auspicious: 吉位列表
            - inauspicious: 凶位列表

        Raises:
            ValueError: 未找到对应的宅卦数据
        """
        ba_zhai_data = self.data_loader.get_ba_zhai_by_gua(house_gua)
        if not ba_zhai_data:
            raise ValueError(f"未找到宅卦数据: {house_gua}")

        result = {
            'auspicious': ba_zhai_data['auspicious_positions'],
            'inauspicious': ba_zhai_data['inauspicious_positions'],
        }
        if 'source_ref' in ba_zhai_data:
            result['source_ref'] = ba_zhai_data['source_ref']
        return result

    def calculate_ming_gua(
        self,
        birth_date: datetime,
        gender: str = 'male'
    ) -> Dict[str, Any]:
        """
        根据出生日期计算命卦

        Args:
            birth_date: 出生日期
            gender: 性别，'male' 或 'female'

        Returns:
            包含以下字段的字典：
            - ming_gua: 命卦名称（如"乾"、"坤"）
            - ming_gua_house: 命卦对应的宅卦（如"乾宅"）
            - group: 东四命或西四命
            - birth_year: 出生年份

        Raises:
            ValueError: 性别参数错误
        """
        if gender not in ['male', 'female']:
            raise ValueError("性别必须是 'male' 或 'female'")

        year = birth_date.year

        # 计算命卦数字
        # 男命：(100 - 出生年份后两位) % 9
        # 女命：(出生年份后两位 - 4) % 9
        year_last_two = year % 100

        if gender == 'male':
            gua_number = (100 - year_last_two) % 9
        else:
            gua_number = (year_last_two - 4) % 9

        # 如果结果为0，则为9
        if gua_number == 0:
            gua_number = 9

        # 数字到八卦的映射（洛书九宫）
        number_to_gua = {
            1: '坎',
            2: '坤',
            3: '震',
            4: '巽',
            # 5 不存在，男为坤，女为艮
            6: '乾',
            7: '兑',
            8: '艮',
            9: '离',
        }

        # 处理5的特殊情况
        if gua_number == 5:
            ming_gua = '坤' if gender == 'male' else '艮'
        else:
            ming_gua = number_to_gua[gua_number]

        # 确定东四命还是西四命
        # 东四命：震、巽、离、坎
        # 西四命：乾、坤、艮、兑
        dong_si = ['震', '巽', '离', '坎']
        xi_si = ['乾', '坤', '艮', '兑']

        if ming_gua in dong_si:
            group = '东四命'
        else:
            group = '西四命'

        return {
            'ming_gua': ming_gua,
            'ming_gua_house': f"{ming_gua}宅",
            'group': group,
            'birth_year': year,
        }

    def check_house_compatibility(
        self,
        house_gua: str,
        ming_gua_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        检查宅卦与命卦的匹配度

        Args:
            house_gua: 宅卦名称（如"乾宅"）
            ming_gua_info: 命卦信息（由 calculate_ming_gua 返回）

        Returns:
            包含以下字段的字典：
            - compatible: 是否匹配（东四命配东四宅，西四命配西四宅）
            - house_group: 宅卦所属组（东四宅或西四宅）
            - ming_group: 命卦所属组（东四命或西四命）
            - recommendation: 建议
        """
        # 提取宅卦的八卦名称
        house_gua_name = house_gua.replace('宅', '')

        # 确定宅卦所属组
        dong_si_house = ['震', '巽', '离', '坎']
        xi_si_house = ['乾', '坤', '艮', '兑']

        if house_gua_name in dong_si_house:
            house_group = '东四宅'
        elif house_gua_name in xi_si_house:
            house_group = '西四宅'
        else:
            raise ValueError(f"未知的宅卦: {house_gua}")

        ming_group = ming_gua_info['group']

        # 判断是否匹配
        compatible = (
            (house_group == '东四宅' and ming_group == '东四命') or
            (house_group == '西四宅' and ming_group == '西四命')
        )

        if compatible:
            recommendation = "宅命相配，吉利"
        else:
            recommendation = "宅命不配，建议选择与命卦相配的宅卦"

        return {
            'compatible': compatible,
            'house_group': house_group,
            'ming_group': ming_group,
            'recommendation': recommendation,
        }
