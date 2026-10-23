import collections

import streamstats.errors as errors
import streamstats.parsers as parsers
from streamstats.logger import logger


def analysis_function(analyze_input: list[str],
                      analyze_format: str,
                      analyze_output: str,
                      analyze_skip_invalid: bool) -> tuple:

    logger.info("Анализ начат.")

    #Счетчки
    event_count = 0
    error_counter = collections.Counter()
    critical_counter = collections.Counter()
    levels_counter = collections.Counter()
    sources_counter = collections.Counter()

    min_timestamp = None
    max_timestamp = None

    for file in analyze_input:
        #Проверка формата
        format_is_ok = False
        if len(file)>=5 and file[-4:]==".csv":
            format_is_ok = True
            file_format = "csv"
        if len(file)>=7 and file[-6:]==".jsonl":
            format_is_ok = True
            file_format = "jsonl"

        #Ошибки, связанные с форматом
        if len(file)<5 or format_is_ok==False:
            logger.error("Неподдерживаемый формат.")
            raise errors.UnsupportedFormat()
        if file_format!=analyze_format:
            logger.error("Несоответствие форматов.")
            raise errors.DifferentFormats()


    if analyze_skip_invalid == False:

        for file in analyze_input:

            with open(file, "r", encoding="utf-8") as input_file:

                event_number = 1

                if analyze_format == "csv":
                    if "," in input_file:
                        headline = input_file.readline().strip().split(",")
                    elif ";" in input_file:
                        headline = input_file.readline().strip().split(";")

                else:
                    headline = analyze_format

                for line in input_file:

                    if analyze_format == "csv":

                        event_number += 1

                    try:
                        parsed_line = parsers.parser(headline, line)
                    except errors.InvalidTimestamp:
                        logger.error("Неверная временная метка.")
                        raise errors.InvalidTimestamp(f"Файл: {file}, строка: {event_number}")
                    except errors.InvalidEvent:
                        logger.error("Неверное событие.")
                        raise errors.InvalidEvent(f"Файл: {file}, строка: {event_number}")

                    if (min_timestamp == None) or (parsed_line.timestamp < min_timestamp):
                        min_timestamp = parsed_line.timestamp
                    if (max_timestamp == None) or (parsed_line.timestamp > max_timestamp):
                        max_timestamp = parsed_line.timestamp

                    event_count += 1

                    if analyze_format == "jsonl":
                        event_number+=1
                    levels_counter[parsed_line.level] += 1
                    sources_counter[parsed_line.source] += 1

                    #счетчики источников ошибок уровня error/critical
                    if parsed_line.level=="ERROR":
                        error_counter[parsed_line.source] += 1
                    if parsed_line.level=="CRITICAL":
                        critical_counter[parsed_line.source] += 1

        report_info = (analyze_output, analyze_input,
                       event_count, levels_counter, sources_counter,
                       error_counter, critical_counter,
                       min_timestamp, max_timestamp, None)

    elif analyze_skip_invalid == True:

        warning_count = 0

        for file in analyze_input:

            with open(file, "r", encoding="utf-8") as input_file:

                if analyze_format == "csv":
                    headline = input_file.readline().strip().split(",")
                else:
                    headline = analyze_format

                for line in input_file:

                    try:
                        parsed_line = parsers.parser(headline, line)
                    except errors.ParserError:
                        logger.warning("Пропущена строка")
                        warning_count += 1
                        continue

                    if (min_timestamp == None) or (parsed_line.timestamp < min_timestamp):
                        min_timestamp = parsed_line.timestamp
                    if (max_timestamp == None) or (parsed_line.timestamp > max_timestamp):
                        max_timestamp = parsed_line.timestamp

                    event_count+=1
                    levels_counter[parsed_line.level] += 1
                    sources_counter[parsed_line.source] += 1

                    #счетчики источников ошибок уровня error/critical
                    if parsed_line.level=="ERROR":
                        error_counter[parsed_line.source] += 1
                    if parsed_line.level=="CRITICAL":
                        critical_counter[parsed_line.source] += 1

        report_info = (analyze_output, analyze_input,
                   event_count, levels_counter, sources_counter,
                   error_counter, critical_counter,
                   min_timestamp, max_timestamp, warning_count)
    logger.info("Анализ завершен.")
    return report_info