from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional


ValueType = TypeVar('ValueType', int, float, str)


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
    max: ValueType = Field(..., description="Maximum value of the metric")
    min: Optional[ValueType] = Field(...,
                                     description="Minimum value of the metric")
    unit: str = Field(..., description="Unit of the metric")
