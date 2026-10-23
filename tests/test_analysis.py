import pytest

from streamstats.analysis import analysis_function
from streamstats.errors import DifferentFormats, InvalidTimestamp, UnsupportedFormat


def test_invalid_time(tmp_path) -> None:
    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp":"2026-10-20T12:00:00+03:00","level":"INFO","source":"Source_name","message":"Info_message"}\n'
        '{"timestamp":"52yo","level":"ERROR","source":"Source_name","message":"Error_message"}\n',
        encoding="utf-8")
    with pytest.raises(InvalidTimestamp):
        analysis_function([str(file)],"jsonl", str(tmp_path / "result.json"), False)


def test_skip_invalid_line(tmp_path) -> None:
    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp":"2026-10-20T11:00:00+03:00","level":"INFO","source":"Source_name","message":"Info_message"}\n'
        '{"timestamp":"52yo","level":"ERROR","source":"Source_name","message":"Error_message"}\n'
        '{"timestamp":"2026-11-20T12:00:00+03:00","level":"ERROR","source":"Source_name","message":"Error_message"}\n',
        encoding="utf-8")
    result = analysis_function([str(file)],"jsonl", str(tmp_path / "result.json"), True)
    assert result is not None


def test_empty_file(tmp_path) -> None:
    file = tmp_path / "events.jsonl"
    file.write_text("",encoding="utf-8")
    result = analysis_function([str(file)],"jsonl", str(tmp_path / "result.json"), False)
    assert result[2] == 0
    assert result[7] is None
    assert result[8] is None


def test_unsupported_format(tmp_path) -> None:
    file = tmp_path / "events.txt"
    file.write_text("",encoding="utf-8")
    with pytest.raises(UnsupportedFormat):
        analysis_function([str(file)],"jsonl", str(tmp_path / "result.json"), False)


def test_different_format(tmp_path) -> None:
    file = tmp_path / "events.jsonl"
    file.write_text("",encoding="utf-8")
    with pytest.raises(DifferentFormats):
        analysis_function([str(file)],"csv", str(tmp_path / "result.json"), False)


def test_two_files(tmp_path) -> None:
    file1 = tmp_path / "events1.jsonl"
    file2 = tmp_path / "events2.jsonl"
    file1.write_text(
        '{"timestamp":"2026-10-20T11:00:00+03:00","level":"INFO","source":"Source1","message":"Info_message"}\n',
        encoding="utf-8"
    )
    file2.write_text(
        '{"timestamp":"2026-10-20T12:00:00+03:00","level":"ERROR","source":"Source2","message":"Error_message"}\n',
        encoding="utf-8"
    )
    result = analysis_function([str(file1), str(file2)], "jsonl", str(tmp_path / "result.json"), False)
    assert result[2] == 2
    assert result[3]["INFO"] == 1
    assert result[3]["ERROR"] == 1
    assert result[4]["Source1"] == 1
    assert result[4]["Source2"] == 1


def test_unicode(tmp_path) -> None:
    file = tmp_path / "events.jsonl"
    file.write_text(
        '{"timestamp":"2026-10-20T11:00:00+03:00","level":"INFO","source":"ИСТОЧНИК","message":"Сообщение"}\n',
        encoding="utf-8"
    )

    result = analysis_function([str(file)], "jsonl", str(tmp_path / "result.json"), False)
    assert result[2] == 1
    assert result[4]["ИСТОЧНИК"] == 1