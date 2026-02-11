"""
节气天文算法模块

提供太阳黄经计算和节气查询功能。
使用 ephem 库进行天文计算。

安装依赖:
    pip install ephem pytz
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import pytz

try:
    import ephem
    EPHEM_AVAILABLE = True
except ImportError:
    EPHEM_AVAILABLE = False
    print("警告: ephem 库未安装，请运行: pip install ephem")

from ..utils.data_loader import get_data_loader, DataLoader


class SolarCalculator:
    """节气天文计算器"""

    # 节气影响描述
    SOLAR_TERM_INFLUENCES = {
        "立春": "立春，万物复苏，阳气上升。天地间生机萌动，宜顺应天时，开启新的计划。",
        "雨水": "雨水，春雨润物，草木萌动。天地间水气渐盛，宜养生调息，顺应自然。",
        "惊蛰": "惊蛰，春雷惊醒蛰虫，万物生长。阳气渐盛，宜积极进取，开拓新局。",
        "春分": "春分，昼夜平分，阴阳平衡。天地间和谐共生，宜保持中正，平衡发展。",
        "清明": "清明，天清地明，万物皆洁。阳气旺盛，宜清理旧物，迎接新生。",
        "谷雨": "谷雨，雨生百谷，万物生长。天地间生机勃勃，宜播种耕耘，收获在望。",
        "立夏": "立夏，夏季开始，阳气鼎盛。天地间热力充沛，宜积极行动，把握时机。",
        "小满": "小满，麦粒渐满，物候丰盈。阳气充盈，宜稳步推进，积累成果。",
        "芒种": "芒种，麦收稻种，农事繁忙。天地间收获与播种并行，宜勤勉努力。",
        "夏至": "夏至，日照最长，阳气极盛。天地间阳极阴生，宜适度收敛，防止过度。",
        "小暑": "小暑，暑气渐盛，炎热将至。阳气旺盛，宜静心养性，避免急躁。",
        "大暑": "大暑，酷暑炎热，阳气最盛。天地间热力达到顶点，宜以静制动，保持冷静。",
        "立秋": "立秋，秋季开始，阴气渐生。天地间由热转凉，宜收敛心神，准备收获。",
        "处暑": "处暑，暑气消退，秋意渐浓。阴阳转换，宜调整状态，适应变化。",
        "白露": "白露，露凝而白，秋意渐深。天地间阴气渐重，宜保养身心，顺应天时。",
        "秋分": "秋分，昼夜平分，阴阳平衡。天地间收获时节，宜总结经验，平衡发展。",
        "寒露": "寒露，露气寒冷，秋意更浓。阴气渐盛，宜收敛精神，准备过冬。",
        "霜降": "霜降，霜始降临，秋季将尽。天地间肃杀之气渐重，宜收藏储备。",
        "立冬": "立冬，冬季开始，阴气渐盛。天地间万物收藏，宜休养生息，积蓄力量。",
        "小雪": "小雪，初雪飘落，寒意渐浓。阴气渐重，宜静心修养，保持温暖。",
        "大雪": "大雪，雪量增大，严冬将至。天地间阴气鼎盛，宜深藏不露，等待时机。",
        "冬至": "冬至，日照最短，阴气极盛。天地间阴极阳生，宜静待转机，孕育希望。",
        "小寒": "小寒，寒气渐盛，严寒将至。阴气旺盛，宜保持温暖，坚守本心。",
        "大寒": "大寒，严寒酷冷，阴气最盛。天地间寒冷达到顶点，宜坚持到底，春天不远。"
    }

    def __init__(self, data_loader: Optional[DataLoader] = None):
        """
        初始化太阳计算器

        Args:
            data_loader: 数据加载器实例，默认使用全局单例
        """
        if not EPHEM_AVAILABLE:
            raise ImportError(
                "ephem 库未安装，请运行: pip install ephem\n"
                "或者: pip install ephem pytz"
            )

        self.data_loader = data_loader or get_data_loader()
        self.solar_terms = self.data_loader.get_solar_terms()

        # 创建节气名称到黄经的映射
        self.term_name_to_longitude = {
            term['name']: term['solar_longitude_deg']
            for term in self.solar_terms
        }

    def get_solar_longitude(
        self,
        dt: datetime,
        timezone: str = 'Asia/Shanghai'
    ) -> float:
        """
        计算指定时间的太阳黄经

        Args:
            dt: 日期时间
            timezone: 时区，默认 Asia/Shanghai

        Returns:
            太阳黄经（0-360度）
        """
        # 确保 datetime 有时区信息
        if dt.tzinfo is None:
            tz = pytz.timezone(timezone)
            dt = tz.localize(dt)
        else:
            # 转换到指定时区
            tz = pytz.timezone(timezone)
            dt = dt.astimezone(tz)

        # 转换为 UTC
        dt_utc = dt.astimezone(pytz.UTC)

        # 创建太阳对象并计算位置
        sun = ephem.Sun()
        sun.compute(dt_utc)

        # 获取太阳的日心黄经（弧度）
        # hlon 是从地球看太阳的方向（日心黄经）
        # 需要加180度得到从地心看太阳的黄经（地心黄经）
        longitude_rad = sun.hlon

        # 转换为角度
        longitude_deg = float(longitude_rad) * 180.0 / ephem.pi

        # 加180度转换为地心黄经（太阳黄经）
        longitude_deg = (longitude_deg + 180.0) % 360

        return round(longitude_deg, 2)

    def get_current_solar_term(
        self,
        dt: datetime,
        timezone: str = 'Asia/Shanghai'
    ) -> Dict[str, Any]:
        """
        获取指定时间的当前节气信息

        Args:
            dt: 日期时间
            timezone: 时区，默认 Asia/Shanghai

        Returns:
            节气信息字典，包含:
            - name: 节气名称
            - longitude: 节气黄经
            - solar_longitude: 当前太阳黄经
            - days_to_next: 距离下一节气的天数（估算）
            - next_term: 下一节气名称
        """
        # 获取当前太阳黄经
        current_longitude = self.get_solar_longitude(dt, timezone)

        # 使用 data_loader 的方法找到当前节气
        current_term = self.data_loader.get_solar_term_by_longitude(current_longitude)

        if not current_term:
            raise ValueError(f"无法找到黄经 {current_longitude} 对应的节气")

        # 找到下一个节气
        current_index = self.solar_terms.index(current_term)
        next_index = (current_index + 1) % len(self.solar_terms)
        next_term = self.solar_terms[next_index]

        # 计算到下一节气的黄经差
        next_longitude = next_term['solar_longitude_deg']
        if next_longitude <= current_longitude:
            next_longitude += 360

        longitude_diff = next_longitude - current_longitude

        # 估算天数（太阳每天移动约 1 度）
        days_to_next = round(longitude_diff)

        return {
            'name': current_term['name'],
            'longitude': current_term['solar_longitude_deg'],
            'solar_longitude': current_longitude,
            'days_to_next': days_to_next,
            'next_term': next_term['name']
        }

    def calculate_solar_term_time(
        self,
        year: int,
        term_name: str,
        timezone: str = 'Asia/Shanghai'
    ) -> datetime:
        """
        计算指定年份的节气精确时间

        Args:
            year: 年份
            term_name: 节气名称（如"春分"、"夏至"）
            timezone: 时区，默认 Asia/Shanghai

        Returns:
            节气发生的精确时间

        Raises:
            ValueError: 节气名称不存在
        """
        if term_name not in self.term_name_to_longitude:
            raise ValueError(f"未知的节气名称: {term_name}")

        target_longitude = self.term_name_to_longitude[term_name]

        # 估算节气大致时间（基于节气黄经）
        # 春分（黄经0度）大约在3月20日
        # 每15度约15天
        days_from_spring = target_longitude / 360 * 365.25
        if target_longitude >= 315:  # 立春之后的节气
            days_from_spring = (target_longitude - 360) / 360 * 365.25

        # 从春分开始估算
        spring_equinox_approx = datetime(year, 3, 20, 12, 0, 0)
        tz = pytz.timezone(timezone)
        spring_equinox_approx = tz.localize(spring_equinox_approx)

        estimated_time = spring_equinox_approx + timedelta(days=days_from_spring)

        # 使用二分法精确查找节气时间
        # 搜索范围：估算时间前后各5天
        start_time = estimated_time - timedelta(days=5)
        end_time = estimated_time + timedelta(days=5)

        # 二分查找，精度到分钟
        while (end_time - start_time).total_seconds() > 60:
            mid_time = start_time + (end_time - start_time) / 2
            mid_longitude = self.get_solar_longitude(mid_time, timezone)

            # 计算与目标黄经的差距（考虑循环）
            diff = mid_longitude - target_longitude
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360

            if abs(diff) < 0.01:  # 精度达到0.01度
                return mid_time

            if diff < 0:
                start_time = mid_time
            else:
                end_time = mid_time

        return start_time + (end_time - start_time) / 2

    def get_solar_term_influence(
        self,
        dt: datetime,
        timezone: str = 'Asia/Shanghai'
    ) -> str:
        """
        获取当前节气对卦象的影响描述

        Args:
            dt: 日期时间
            timezone: 时区，默认 Asia/Shanghai

        Returns:
            节气影响描述文本
        """
        term_info = self.get_current_solar_term(dt, timezone)
        term_name = term_info['name']

        # 获取节气影响描述
        influence = self.SOLAR_TERM_INFLUENCES.get(
            term_name,
            f"当前节气为{term_name}，天地运行，顺应自然。"
        )

        # 添加距离下一节气的信息
        days_to_next = term_info['days_to_next']
        next_term = term_info['next_term']

        full_description = (
            f"{influence}\n"
            f"距离下一节气【{next_term}】还有约 {days_to_next} 天。"
        )

        return full_description

    def get_all_solar_terms_for_year(
        self,
        year: int,
        timezone: str = 'Asia/Shanghai'
    ) -> Dict[str, datetime]:
        """
        计算指定年份的所有节气时间

        Args:
            year: 年份
            timezone: 时区，默认 Asia/Shanghai

        Returns:
            节气名称到时间的字典
        """
        result = {}
        for term in self.solar_terms:
            term_name = term['name']
            try:
                term_time = self.calculate_solar_term_time(year, term_name, timezone)
                result[term_name] = term_time
            except Exception as e:
                print(f"警告: 计算节气 {term_name} 时出错: {e}")
                continue

        return result
