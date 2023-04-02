import io
import queue
import re
from typing import Any, AnyStr

log_queue = queue.Queue


class Log:
    def __init__(
            self,
            format_string: str,
            date_format_string: str,
            filename: str
    ) -> None:
        """
        format_string:
         - $(message): The string to print
         - $(datetime): Current time on call
         - $(call.filename): Filename of the script
         - $(call.lineno): The call line
         - $(call.type): Call type
         - ! $(level): Level debugging !

        date_format_string:
            Uses the default datetime.now().strftime() function
        """

        self.format_string: str = str
        self.date_format_string: str = str
        self.enabled: bool = bool

        self.file = io.TextIOBase | io.BufferedIOBase
        self.ansi_escape = re.Pattern[AnyStr]

    def default_text_log(
            self,
            msg: list[str],
            caller: Any,
            join: str,
            end: str,
            force_flush: bool,
            log_color: str,
            log_type: str
    ) -> None: ...

    def nprint(
            self,
            *msg: list[str],
            join: str,
            end: str,
            force_flush: bool
    ) -> None: ...

    def request(
            self,
            *msg: list[str],
            join: str,
            end: str,
            force_flush: bool
    ) -> None: ...

    def warning(
            self,
            *msg: list[str],
            join: str,
            end: str,
            force_flush: bool
    ) -> None: ...

    def important_warning(
            self,
            *msg: list[str],
            join: str,
            end: str,
            force_flush: bool
    ) -> None: ...

    def error(
            self,
            *msg: list[str],
            join: str,
            end: str,
            force_flush: bool
    ) -> None: ...

    def fatal_error(
            self,
            *msg: list[str],
            join: str,
            end: str,
            force_flush: bool
    ) -> None: ...

    def wait_until_queue_empty(
            self
    ) -> None: ...
