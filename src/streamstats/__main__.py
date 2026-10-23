import sys

import typer

import streamstats.analysis as analysis
import streamstats.errors as errors
import streamstats.report as report

streamstats = typer.Typer()

@streamstats.callback()
def callback() -> None:
    pass

@streamstats.command("analyze")
def analyze(analyze_input: list[str] = typer.Argument(...),
            analyze_format: str = typer.Option(...,"--format"),
            analyze_output: str = typer.Option(...,"--output"),
            analyze_skip_invalid: bool = typer.Option(False,"--skip-invalid")) -> None:
    try:
        answer = analysis.analysis_function(analyze_input, analyze_format, analyze_output, analyze_skip_invalid)
    except (errors.ParserError, errors.AnalyzeError) as error:
        print(error, file = sys.stderr)
        raise SystemExit(2)
    report.report(*answer)

def main() -> None:
    streamstats()

if __name__ == "__main__":
    main()