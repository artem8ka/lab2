import logging

logging.basicConfig(
    filename="streamstats.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    encoding="utf-8"
    )

logger = logging.getLogger("streamstats")