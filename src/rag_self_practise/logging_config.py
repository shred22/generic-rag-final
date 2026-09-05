import logging
from pathlib import Path

_LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"

# Third-party libraries (HTTP clients, Chroma, etc.) log verbosely at DEBUG --
# raw request/response bodies, connection internals. Rather than naming each
# one (fragile -- library internals vary by version and some vendor their own
# copies of dependencies under different names), the root logger is kept at
# INFO and only our own package is dropped down to DEBUG.
_OUR_PACKAGE_LOGGER = "rag_self_practise"


def configure_logging(log_file: str = "logs/app.log") -> None:
    """Configures logging to write our own package's INFO+ to the console
    and DEBUG+ to a log file, so progress is visible live while full detail
    is kept for later troubleshooting -- without third-party library noise."""

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(_LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger(_OUR_PACKAGE_LOGGER).setLevel(logging.DEBUG)
