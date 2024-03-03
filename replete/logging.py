from __future__ import annotations

import logging
import sys
import traceback
import warnings
from typing import TYPE_CHECKING, Any

from coloredlogs import DEFAULT_FIELD_STYLES, DEFAULT_LEVEL_STYLES, ColoredFormatter

if TYPE_CHECKING:
    from pathlib import Path

ORIGINAL_SHOWWARNINGS = warnings.showwarning


def _warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file, "write") else sys.stderr
    traceback.print_stack(file=log)
    ORIGINAL_SHOWWARNINGS(message, category, filename, lineno, file, line)


class WarnWithTraceback:
    def __enter__(self) -> None:
        self._orig_show = warnings.showwarning
        warnings.showwarning = _warn_with_traceback

    def __exit__(self, *_):
        warnings.showwarning = ORIGINAL_SHOWWARNINGS


def assert_with_logging(status: bool, message: str):  # noqa: FBT001
    if not status:
        logging.critical(message)
    assert status, message  # noqa: S101


class ChangeLoggingLevel:
    def __init__(self, level: int):
        self._level = level
        self._original_level: int = None

    def __enter__(self) -> None:
        root_logger = logging.getLogger()
        self._original_level = root_logger.level
        root_logger.setLevel(self._level)

    def __exit__(self, *_):
        logging.getLogger().setLevel(self._original_level)
        self._original_level = None


def offset_logger_level(logger: logging.Logger, amount: int):
    def change_level(record: logging.LogRecord):
        record.levelno += amount
        record.levelname = logging.getLevelName(record.levelno)
        return record

    logger.addFilter(change_level)


def get_file_handler(log_file: Path, logging_level: int | str = logging.DEBUG, *, append=True, use_year=False):
    file_handler = logging.FileHandler(log_file, mode="a" if append else "w")
    formatter = get_logging_formatter(use_year=use_year)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging_level)
    return file_handler


StylesType = dict[str, dict[str, Any]]
CUSTOM_LEVEL_STYLES: StylesType = {
    **DEFAULT_LEVEL_STYLES,
    "debug": {"color": "black", "bright": True},
    "info": {"faint": True},
    "warning": {"color": "yellow", "bold": True},
    "error": {"color": "red", "bold": True},
    "critical": {"color": "magenta", "bold": True, "underline": True},
}
CUSTOM_FIELD_STYLES: StylesType = {**DEFAULT_FIELD_STYLES, "levelname": {"color": "white"}}
CUSTOM_FORMAT = "{asctime:^} [{levelname:^8s}]({name:>30s}+{lineno:>4d}): {message:<s}"


def get_logging_formatter(
    *,
    color=False,
    use_year=False,
    level_styles_update: StylesType = None,
    field_styles_update: StylesType = None,
):
    fmt = CUSTOM_FORMAT
    maybe_year = "%Y-" if use_year else ""
    date_fmt = f"{maybe_year}%m-%d %H:%M:%S"
    if not color:
        return logging.Formatter(fmt, style="{", datefmt=date_fmt)
    level_styles = {**CUSTOM_LEVEL_STYLES, **(level_styles_update or {})}
    field_styles = {**CUSTOM_FIELD_STYLES, **(field_styles_update or {})}
    return ColoredFormatter(fmt, style="{", datefmt=date_fmt, level_styles=level_styles, field_styles=field_styles)


# https://stackoverflow.com/a/16993115/2059584
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


class FilterWhitelist(logging.Filter):
    def __init__(self, allowed_modules: list[str]) -> None:
        super().__init__()
        allowed_modules.extend(["root", "__main__"])
        self._allowed_modules = allowed_modules

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        if record.levelno > logging.WARNING:
            return True
        return any(module == record.name[: len(module)] for module in self._allowed_modules)


def setup_logging(
    log_file: Path = None,
    print_level: int | str = logging.INFO,
    *,
    append=False,
    level_styles_update: dict[str, dict[str, Any]] = None,
    field_styles_update: dict[str, dict[str, Any]] = None,
    disable_colors=False,
    log_uncaught_exceptions=True,
    use_year=False,
    whitelist: list[str] = None,
):
    """
    Make logging nice

    :param log_file: in which file to write the log
    :param print_level: Level of logging to stdout
    :param append: Append to log file instead of overwriting
    :param level_styles_update: Update to color styles for stdout formatter
    :param disable_colors: Disable colors in stdout
    :param log_uncaught_exceptions: Add uncaught exceptions to the log, not guaranteed
    :param use_year: Add year to logs
    :param whitelist: Only log these modules
    """
    level_styles_update = level_styles_update or {}
    field_styles_update = field_styles_update or {}
    if isinstance(print_level, str):
        print_level = int(print_level) if print_level.isdigit() else getattr(logging, print_level)
    formatter = get_logging_formatter(use_year=use_year)
    colored_formatter = get_logging_formatter(
        color=True,
        level_styles_update=level_styles_update,
        field_styles_update=field_styles_update,
        use_year=use_year,
    )

    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter if disable_colors else colored_formatter)
    console_handler.setLevel(print_level)
    handlers.append(console_handler)
    if log_file is not None:
        handlers.append(get_file_handler(log_file, append=append, use_year=use_year))

    root_logger = logging.getLogger()
    root_logger.level = 0
    root_logger.handlers.extend(handlers)

    if whitelist:
        for handler in handlers:
            handler.addFilter(FilterWhitelist(whitelist))

    if log_uncaught_exceptions:
        sys.excepthook = handle_exception
