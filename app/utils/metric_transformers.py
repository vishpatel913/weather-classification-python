

from typing import Dict, Union
from app.schemas.MetricValue import MetricValue, MetricRangeValue


def transform_maps_to_metric(
    value_map: Dict[str, Union[str, int, float]] = None,
    unit_map: Dict[str, str] = None
) -> Dict[str, MetricValue]:
    metric_map: dict(str, MetricValue) = {}
    value_map = value_map or {}
    unit_map = unit_map or {}

    for key, value in value_map.items():
        unit = ""
        if key in unit_map:
            unit = unit_map[key] or ""
        metric_map[key] = {"value": value, "unit": unit}

    return metric_map


MAX_SUFFIX = "max"
MIN_SUFFIX = "min"


def transform_maps_to_metric_range(
    value_map: Dict[str, Union[str, int, float]] = None,
    unit_map: Dict[str, str] = None
) -> Dict[str, MetricRangeValue | MetricValue]:
    metric_map: dict(str, MetricRangeValue | MetricValue) = {}
    value_map = value_map or {}
    unit_map = unit_map or {}

    for key, value in value_map.items():
        unit = ""
        if key in unit_map:
            unit = unit_map[key] or ""
        if key.endswith("_max"):
            key = key.removesuffix("_max")
            metric_map.setdefault(key, {"unit": unit}).update({"max": value})
        elif key.endswith("_min"):
            key = key.removesuffix("_min")
            metric_map.setdefault(key, {"unit": unit}).update({"min": value})
        else:
            metric_map[key] = {"unit": unit, "value": value, }

    return metric_map
