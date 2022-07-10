import pytest
from src.load_data import *


@pytest.mark.parametrize(
    "index,expected_key",
    [([0, "Activity"]), ([4, "delay(s)"]), ([-1, "delay(s)"]), ([-2, "Button"])],
)
def test_get_nth_key_with_valid_index(expected_headers, index, expected_key):
    key = get_nth_key(expected_headers, index)
    assert str(key) == str(expected_key)


def test_get_nth_key_with_invalid_index(expected_headers):
    # Given
    index = 10
    with pytest.raises(IndexError):
        key = get_nth_key(expected_headers, index)


def test_load_click_profile_from_file_path(
    filepath, expected_headers, expected_profile
):
    # Given
    profile, headers = get_click_profile(filepath)

    assert (
        headers == expected_headers
        and len(profile) == len(expected_profile)
        and isinstance(profile, list)
    )
