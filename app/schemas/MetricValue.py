from pydantic import BaseModel, Field
from typing import Generic, TypeVar


ValueType = TypeVar('ValueType', int, float, str)


class MetricValue(BaseModel, Generic[ValueType]):
    """
    A simple model to represent a value with its unit.
    """
    value: ValueType = Field(..., description="Value of the metric")
    unit: str = Field(..., description="Unit of the metric")
