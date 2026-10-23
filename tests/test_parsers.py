import json

import pytest

from streamstats.errors import InvalidEvent, InvalidTimestamp
from streamstats.parsers import parser

csv_headline = ["timestamp", "level", "source", "message"]
valid_jsonl_event = {
    "timestamp": "2026-10-20T12:30:00+03:00",
    "level": "ERROR",
    "source": "Source_name",
    "message": "Error_message"
}
invalid_timestamp_jsonl_event = {
    "timestamp": "fjkdsjio2026-10-20T12:30:00+03:00",
    "level": "ERROR",
    "source": "Source_name",
    "message": "Error_message"
}
invalid_jsonl_event = {
    "timestamp": "2026-10-20T12:30:00+03:00",
    "level": "ERROR",
    "source": "   ",
    "message": "Error_message"
}

def test_valid_jsonl_event() -> None:
    event = parser("jsonl", json.dumps(valid_jsonl_event))
    assert event.level == "ERROR"
    assert event.source == "Source_name"
    assert event.message == "Error_message"


def test_valid_csv() -> None:
    csv_event = "2026-10-20T12:30:00+03:00,ERROR,Source_name,Error_message"
    event = parser(csv_headline, csv_event)
    assert event.level == "ERROR"
    assert event.source == "Source_name"
    assert event.message == "Error_message"


def test_invalid_timestamp_json_event() -> None:
    with pytest.raises(InvalidTimestamp):
        parser("jsonl", json.dumps(invalid_timestamp_jsonl_event))


def test_invalid_timestamp_csv() -> None:
    csv_event = "2gg026-10-fdhfdsdf,ERROR,Source_name,Error_message"
    with pytest.raises(InvalidTimestamp):
        parser(csv_headline, csv_event)


def test_invalid_json_event() -> None:
    with pytest.raises(InvalidEvent):
        parser("jsonl", json.dumps(invalid_jsonl_event))


def test_invalid_csv_event() -> None:
    csv_event = "2026-10-20T12:30:00+03:00;ERRRRROR;Source_name;Error_message"
    with pytest.raises(InvalidEvent):
        parser(csv_headline, csv_event)