from app.utils.metric_transformer import transform_maps_to_metric


class TestMetricTransformUtils:
    """Test cases for the transform_maps_to_metric util"""

    def test_return_missing_args_success(self):
        """Test successful transform when inputs are missing"""

        result = transform_maps_to_metric()
        assert result == {}

    def test_return_empty_maps_success(self):
        """Test successful transform when inputs are empty"""
        mock_value_map = {}
        mock_unit_map = {}
        result = transform_maps_to_metric(mock_value_map, mock_unit_map)

        assert result == {}

    def test_return_valid_maps_success(self):
        """Test successful transform when inputs are valid"""
        mock_value_map = {"key1": 7.12, "key2": 1995}
        mock_unit_map = {"key1": "d.m", "key2": 'y'}
        result = transform_maps_to_metric(mock_value_map, mock_unit_map)

        assert result == {"key1": {"units": "d.m", "value": 7.12},
                          "key2": {"units": "y", "value": 1995}}

    def test_return_handle_empty_unit_values_success(self):
        """Test successful transform when unit fields are empty or missing"""
        mock_value_map = {"key1": 7.12, "key2": 1995}
        mock_unit_map = {"key1": ""}
        result = transform_maps_to_metric(mock_value_map, mock_unit_map)

        assert result == {"key1": {"units": "", "value": 7.12},
                          "key2": {"units": "", "value": 1995}}

    def test_return_handle_incompatible_fields_success(self):
        """Test successful transform when fields are incompatible"""
        mock_value_map = {"key1": 7.12, "key2": 1995}
        mock_unit_map = {"key3": "d.m", "key4": 'y'}

        result = transform_maps_to_metric(mock_value_map, mock_unit_map)

        assert result == {"key1": {"units": "", "value": 7.12},
                          "key2": {"units": "", "value": 1995}}
