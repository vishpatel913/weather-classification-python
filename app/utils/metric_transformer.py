

from typing import Dict, Union
from app.schemas.MetricValue import MetricValue


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
