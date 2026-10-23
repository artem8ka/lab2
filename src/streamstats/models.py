from typing import Literal, Annotated

from pydantic import AwareDatetime, BaseModel, StringConstraints


non_empty_source = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class Event(BaseModel):
    timestamp: AwareDatetime
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    source: non_empty_source
    message: str