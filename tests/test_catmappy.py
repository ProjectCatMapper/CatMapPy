import pandas as pd
import pytest

from catmappy import (
    CMIDinfo,
    build_key,
    build_key_from_columns,
    call_api,
    get_cmid_info,
    is_normalized_key,
    normalize_key,
)
from catmappy.core import CatMapPyError


def test_build_key_vectorization():
    assert build_key("Type", ["A", "B"]) == ["Type == A", "Type == B"]


def test_build_key_mismatched_lengths_raise():
    with pytest.raises(CatMapPyError):
        build_key(["a", "b"], ["1", "2", "3"])


def test_build_key_from_columns_and_drop():
    frame = pd.DataFrame([{"Type": "Adamana Brown", "Region": "Flagstaff"}])
    out = build_key_from_columns(frame, ["Type", "Region"], drop_source=True)
    assert list(out.columns) == ["Key"]
    assert out.loc[0, "Key"] == "Type == Adamana Brown && Region == Flagstaff"


def test_normalize_and_check_key():
    raw = " Key == Region==Flagstaff  && Type== Adamana Brown "
    normalized = normalize_key(raw)[0]
    assert normalized == "Region == Flagstaff && Type == Adamana Brown"
    assert is_normalized_key([normalized, raw]) == [True, False]


def test_aliases_match():
    assert CMIDinfo is get_cmid_info


def test_call_api_http_error(monkeypatch):
    class MockResponse:
        status_code = 500
        ok = False
        text = "boom"

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("catmappy.core.requests.get", mock_get)
    with pytest.raises(CatMapPyError, match="boom"):
        call_api("search", {}, request="GET", url="https://example.test")
