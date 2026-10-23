from typer.testing import CliRunner

from streamstats.__main__ import streamstats as app

runner = CliRunner()

def test_cli_report(tmp_path) -> None:
    input_file = tmp_path / "events.jsonl"
    output_file = tmp_path / "result.json"

    input_file.write_text(
        '{"timestamp":"2026-10-20T11:00:00+03:00","level":"INFO","source":"ИСТОЧНИК","message":"Сообщение"}\n',
        encoding="utf-8"
    )

    result = runner.invoke(app, ["analyze", str(input_file), "--format", "jsonl", "--output", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()
