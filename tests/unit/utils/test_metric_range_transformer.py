from app.utils.metric_transformers import transform_maps_to_metric_range


class TestMetricRangeTransformUtils:
    """Test cases for the transform_maps_to_metric_range util"""

    def test_return_missing_args_success(self):
        """Test successful transform when inputs are missing"""

        result = transform_maps_to_metric_range()
        assert result == {}

    def test_return_empty_maps_success(self):
        """Test successful transform when inputs are empty"""
        mock_value_map = {}
        mock_unit_map = {}
        result = transform_maps_to_metric_range(mock_value_map, mock_unit_map)

        assert result == {}

    def test_return_valid_maps_success(self):
        """Test successful transform when inputs are valid"""
        mock_value_map = {
            "key_1_max": 20.0,
            "key_1_min": 12.5,
            "key_2_max": 18,
            "key_2_min": 12,
        }
        mock_unit_map = {
            "key_1_max": "1",
            "key_1_min": "1",
            "key_2_max": "2",
            "key_2_min": "2",
        }

        result = transform_maps_to_metric_range(mock_value_map, mock_unit_map)

        assert result == {
            "key_1": {"unit": "1", "max": 20.0, "min": 12.5},
            "key_2": {"unit": "2", "max": 18, "min": 12},
        }

    def test_handle_empty_unit_values(self):
        """Test successful transform when fields are not min/max"""
        mock_value_map = {
            "key_1_max": 20.0,
            "key_1_min": 12.5,
            "key_2": 18,
            "key_3": 12.7,
        }
        mock_unit_map = {"key_1_max": "1", "key_1_min": "1", "key_2": "2", "key_3": "3"}
        result = transform_maps_to_metric_range(mock_value_map, mock_unit_map)

        assert result == {
            "key_1": {"unit": "1", "max": 20.0, "min": 12.5},
            "key_2": {"unit": "2", "value": 18},
            "key_3": {"unit": "3", "value": 12.7},
        }

    def test_handle_missing_fields(self):
        """Test successful transform when min/max fields are missing"""
        mock_value_map = {
            "key_1_max": 20.0,
            "key_1_min": 12.5,
            "key_2_max": 18,
            "key_3_min": 12,
        }
        mock_unit_map = {
            "key_1_max": "1",
            "key_1_min": "1",
            "key_2_max": "2",
            "key_3_min": "2",
        }

        result = transform_maps_to_metric_range(mock_value_map, mock_unit_map)

        assert result == {
            "key_1": {"unit": "1", "max": 20.0, "min": 12.5},
            "key_2": {"unit": "2", "max": 18},
            "key_3": {"unit": "2", "min": 12},
        }
