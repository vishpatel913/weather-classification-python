from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field


ValueType = TypeVar("ValueType", int, float, str)


class MetricValue(BaseModel, Generic[ValueType]):
    """
    A simple model to represent a value with its unit.
    """

    value: ValueType = Field(..., description="Value of the metric")
    unit: str = Field(..., description="Unit of the metric")


class MetricRangeValue(BaseModel, Generic[ValueType]):
    """
    A min/max model to represent values with their unit.
    """

    max: Optional[ValueType] = Field(
        default=None, description="Maximum value of the metric"
    )
    min: Optional[ValueType] = Field(
        default=None, description="Minimum value of the metric"
    )
    unit: str = Field(..., description="Unit of the metric")
