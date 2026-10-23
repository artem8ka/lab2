import collections
from datetime import datetime


def report(analyze_output: str,
           analyze_input: str,
           event_count: int,
           levels_counter: collections.Counter,
           sources_counter: collections.Counter,
           error_top: collections.Counter,
           critical_top: collections.Counter,
           min_timestamp: datetime | None,
           max_timestamp: datetime | None,
           passed_events: int | None) -> None:
    with open(analyze_output, "w", encoding="utf-8") as report_file:
        report_file.write("Отчет\n")
        report_file.write(f"Файл(ы): {analyze_input}\n")
        report_file.write(f"Количество обработанных событий: {event_count}\n")
        report_file.write(f"Количество событий уровня DEBUG: {levels_counter['DEBUG']}\n")
        report_file.write(f"Количество событий уровня INFO: {levels_counter['INFO']}\n")
        report_file.write(f"Количество событий уровня WARNING: {levels_counter['WARNING']}\n")
        report_file.write(f"Количество событий уровня ERROR: {levels_counter['ERROR']}\n")
        report_file.write(f"Количество событий уровня CRITICAL: {levels_counter['CRITICAL']}\n")
        report_file.write("Количество событий по источникам:\n")
        report_file.writelines(f"{source}: {count}\n" for source, count in sources_counter.items())
        report_file.write("Top источников ошибок уровня ERROR:\n")
        report_file.writelines(f"{source}: {count}\n" for source, count in error_top.most_common(5))
        report_file.write("Top источников ошибок уровня CRITICAL:\n")
        report_file.writelines(f"{source}: {count}\n" for source, count in critical_top.most_common(5))
        report_file.write(f"Первая временная метка: {min_timestamp}\n")
        report_file.write(f"Последняя временная метка: {max_timestamp}\n")
        if not(passed_events is None):
            report_file.write(f"Число пропущенных строк: {passed_events}\n")