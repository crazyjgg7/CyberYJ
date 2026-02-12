"""
HTTP API request/response models.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class DivinationRequest(BaseModel):
    """POST /v1/divination/interpret request body."""

    coins: list[int] = Field(..., min_length=6, max_length=6)
    question: Optional[str] = None

    @field_validator("coins")
    @classmethod
    def validate_coins(cls, value: list[int]) -> list[int]:
        if any(v not in (6, 7, 8, 9) for v in value):
            raise ValueError("coins数组必须包含6个元素 (6/7/8/9)")
        return value
