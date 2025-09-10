from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field


T = TypeVar("T", int, float, str)


class MetricValue(BaseModel, Generic[T]):
    """
    A simple model to represent a value with its unit.
    """

    value: T = Field(..., description="Value of the metric")
    unit: str = Field(..., description="Unit of the metric")


class MetricRangeValue(BaseModel, Generic[T]):
    """
    A min/max model to represent values with their unit.
    """

    max: Optional[T] = Field(default=None, description="Maximum value of the metric")
    min: Optional[T] = Field(default=None, description="Minimum value of the metric")
    unit: str = Field(..., description="Unit of the metric")
