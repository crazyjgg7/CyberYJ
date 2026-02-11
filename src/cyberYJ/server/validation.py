"""
参数校验与解析工具
"""

from datetime import datetime
from typing import Any, Dict, Optional, List

import pytz


def require_fields(arguments: Dict[str, Any], fields: List[str]) -> None:
    for field in fields:
        if field not in arguments:
            raise ValueError(f"{field} 为必填参数")


def get_timezone(tz_name: Optional[str]) -> str:
    if not tz_name:
        return "Asia/Shanghai"
    try:
        pytz.timezone(tz_name)
    except Exception as exc:
        raise ValueError(f"无效时区: {tz_name}") from exc
    return tz_name


def parse_timestamp(value: Optional[str], timezone: str) -> datetime:
    if not value:
        return datetime.now(pytz.timezone(timezone))

    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception as exc:
        raise ValueError("timestamp 必须是 RFC3339 格式") from exc

    if dt.tzinfo is None:
        dt = pytz.timezone(timezone).localize(dt)
    return dt


def require_type(value: Any, expected_type: type, field: str) -> None:
    if not isinstance(value, expected_type):
        raise ValueError(f"{field} 类型错误，期望 {expected_type.__name__}")


def optional_type(value: Any, expected_type: type, field: str) -> None:
    if value is None:
        return
    require_type(value, expected_type, field)


def validate_enum(value: Any, allowed: List[str], field: str) -> None:
    if value is None:
        return
    if value not in allowed:
        raise ValueError(f"{field} 不在允许范围: {allowed}")


def validate_int_range(value: Any, min_value: int, max_value: int, field: str) -> None:
    if value is None:
        return
    if not isinstance(value, int):
        raise ValueError(f"{field} 类型错误，期望 int")
    if value < min_value or value > max_value:
        raise ValueError(f"{field} 必须在 {min_value}-{max_value} 之间")
