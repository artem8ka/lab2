import json

from pydantic import ValidationError

import streamstats.errors as errors
from streamstats.models import Event


def parser(parser_headline: list, parser_input: str) -> Event:

    if parser_headline == "jsonl":
        parser_output = json.loads(parser_input)
    else:
        if not all(key in parser_headline for key in ["timestamp", "level", "source", "message"]):
            raise errors.InvalidEvent()
        if "," in parser_input:
            parser_input = parser_input.strip().split(",")
        elif ";" in parser_input:
            parser_input = parser_input.strip().split(";")
        parser_output = {"timestamp": next(parser_input[i] for i in range(len(parser_headline)) if parser_headline[i]=="timestamp"),
                         "level": next(parser_input[i] for i in range(len(parser_headline)) if parser_headline[i]=="level"),
                         "source": next(parser_input[i] for i in range(len(parser_headline)) if parser_headline[i]=="source"),
                         "message": next(parser_input[i] for i in range(len(parser_headline)) if parser_headline[i]=="message")}

    #Валидация обязательных полей
    try:
        event = Event(**parser_output)
    except ValidationError as error:
        for i in error.errors():
            if i["loc"] == ("timestamp",) and i["type"] in ("datetime_parsing", "datetime_from_date_parsing"):
                raise errors.InvalidTimestamp()
            else:
                raise errors.InvalidEvent()

    return event